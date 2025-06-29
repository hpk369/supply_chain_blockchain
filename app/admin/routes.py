import json
import time
from pathlib import Path

from flask import Blueprint, render_template, jsonify, request, abort
from flask_login import login_required, current_user

from ..utils import roles_required
from blockchain import BC

admin_bp = Blueprint("admin", __name__, url_prefix="/admin", template_folder="templates")

LEDGER_PATH = Path("data/ledger.json")
CONCERNS_PATH = Path("data/concerns.json")

# Load or create global Blockchain instance
# BC = Blockchain()

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
  # print(f"DEBUG: {current_user.id}, role={current_user.role}")
  concerns = load_concerns()
  # Gather all pending transfers
  pending_transfers = [blk for blk in BC.chain if blk.status == "pending"]
  print(f"DEBUG: Found {len(pending_transfers)} pending transfers")
  return render_template("admin_dashboard.html", username=current_user.id, concerns=concerns, pending_transfers=pending_transfers)

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

@admin_bp.route("/approve_transfer/<int:block_index>", methods=["POST"])
@login_required
@roles_required("admin")
def approve_transfer(block_index):
  try:
    blk = BC.chain[block_index]
  except IndexError:
    abort(404, "Block not found")
  if blk.status != "pending":
    abort(400, "Block is not pending approval")
  blk.status = "confirmed"
  blk.hash = blk.calculate_hash()
  BC.save_chain()
  return jsonify(blk.to_dict()), 200

@admin_bp.route("/deny_transfer/<int:block_index>", methods=["POST"])
@login_required
@roles_required("admin")
def deny_transfer(block_index):
  try:
      blk = BC.chain[block_index]
  except IndexError:
      abort(404, "Block not found")
  if blk.status != "pending":
      abort(400, "Block is not pending approval")

  batch_id = blk.data.get("batch_id")
  previous_owner = blk.data.get("previous_owner")

  # Mark block as denied (do NOT mutate actor)
  blk.status = "denied"
  blk.hash = blk.calculate_hash()

  # Append new block reverting ownership
  revert_data = {
      "actor": previous_owner,
      "action": f"Transfer denied - ownership reverted to {previous_owner}",
      "batch_id": batch_id
  }
  revert_block = BC.add_block(revert_data, status="confirmed")

  BC.save_chain()

  return jsonify({
      "denied_block": blk.to_dict(),
      "revert_block": revert_block.to_dict()
  }), 200


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
  '''
  Admin posts a new concern. Supports both JSON payloads and form submission.
  Expects:
    - JSON:   { "block_index": 5, "issue": "Timestamp mismatch" }
    - Form:   block_index=5, issue=Tumestamp+mismatch
  '''
  # Try JSON first
  data = request.get_json(silent=True) or {}
  block_index = data.get("block_index")
  issue = data.get("issue", "").strip()
  # Fallback to form data if JSON not provided
  if block_index is None or not issue:
    try:
      block_index = int(request.form.get("block_index", ""))
    except (TypeError, ValueError):
      block_index = None
    issue = request.form.get("issue", "").strip()
  # Validate inputs
  if block_index is None or issue == "":
    abort(400, "Must provide a valid block_index and non-empty issue")
  # Build and persist the new concern
  new_concern = {
    "id": int(time.time() * 1000),
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

@admin_bp.route("/concerns/<int:concern_id>", methods=["POST","DELETE"])
@login_required
@roles_required("admin")
def resolve_concern(concern_id):
  # Mark a concern as resolved. Adds "resolved": TRUE and "resolved_at" timestamp
  concerns = load_concerns()
  for c in concerns:
    if c["id"] == concern_id:
      c["resolved"] = True
      c["resolved_at"] = time.ctime()
      save_concerns(concerns)
      return jsonify(c), 200
  return abort(404, "Concern not found")