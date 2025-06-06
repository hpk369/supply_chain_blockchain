import json
import time
from pathlib import Path

from flask import Blueprint, render_template, jsonify, request, abort
from flask_login import login_required, current_user

from ..utils import roles_required
from blockchain.blockchain import Blockchain

admin_bp = Blueprint("admin", __name__, url_prefix="/admin", template_folder="templates")

LEDGER_PATH = Path("data/ledger.json")
CONCERNS_PATH = Path("data/concerns.json")

# Load or create global Blockchain instance
BC = Blockchain()

def load_concerns():
  # Load concerns.json if it exists, otherwise return an empty list
  if not CONCERNS_PATH.exists():
    return []
  try:
    return json.loads(CONCERNS_PATH.read_text())
  except json.JSONDecodeError:
    return []
  
def save_concerns(concerns_list):
  # Persist the list of concerns to data/concerns.json
  CONCERNS_PATH.write_text(json.dumps(concerns_list, indent=4))

@admin_bp.route("/dashboard")
@login_required
@roles_required("admin")
def admin_dashboard():
  '''
  Render a simple Admin Dashboard HTML page with links to:
  - View full chain
  - View/raise/resolved concerns
  '''
  print(f"DEBUG: {current_user.id}, role={current_user.role}")
  concerns = load_concerns()
  return render_template("admin_dashboard.html", username=current_user.id, concerns=concerns)

@admin_bp.route("/chain", methods=["GET"])
@login_required
@roles_required("admin")
def view_chain():
  # Return the entire blockchain (JSON)
  # Read the ledger.json file directly for the latest data
  try:
    chain_data = json.loads(LEDGER_PATH.read_text())
  except Exception:
    chain_data = []
  return jsonify(chain_data), 200

@admin_bp.route("/concerns", methods=["GET"])
@login_required
@roles_required("admin")
def view_concerns():
  # Returns the list of all concerns (JSON)
  concerns = load_concerns()
  return jsonify(concerns), 200

@admin_bp.route("/concerns", methods=["POST"])
@login_required
@roles_required("admin")
def raise_concern():
  # Admin posts a new concern. Expects JSON: { "block_index": int, "issue": str }
  payload = request.get_json() or {}
  block_index = payload.get("block_index")
  issue = payload.get("issue", "").strip()

  if block_index is None or issue == "":
    return abort(400, "Must provide block_index and issue text")
  
  new_concern = {
    "id": int(time.time() * 1000),  # millisecond-precision unique ID
    "block_index": block_index,
    "issue": issue,
    "raised_by": current_user.id,
    "raised_at": time.ctime(),
    "resolved": False
  }
  concerns = load_concerns()
  concerns.append(new_concern)
  save_concerns(concerns)
  return jsonify(new_concern), 201

@admin_bp.route("/concerns/<int:concern_id>", methods=["DELETE"])
@login_required
@roles_required("admin")
def resolve_concern(concern_id):
  # Mark a conern as resolved. Adds "resolved": TRUE and "resolved_at" timestamp
  concerns = load_concerns()
  for c in concerns:
    if c["id"] == concern_id:
      c["resolved"] = True
      c["resolved_at"] = time.ctime()
      save_concerns(concerns)
      return jsonify(c), 200
  return abort(404, "Concern not found")