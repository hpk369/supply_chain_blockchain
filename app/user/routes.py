import time

from flask import Blueprint, render_template, jsonify, request, abort
from flask_login import login_required, current_user

from ..utils import roles_required
from blockchain.blockchain import Blockchain
from blockchain import BC
from app.admin.routes import load_concerns

user_bp = Blueprint("user", __name__, url_prefix="/user", template_folder="templates")

@user_bp.route("/dashboard")
@login_required
@roles_required("user")
def user_dashboard():
  '''
  Render a simple user dashboard HTMl page with:
  - From to create a new batch
  - Form to transfer a batch
  - Form to view history of a batch
  '''
  print(f"DEBUG: {current_user.id}, role={current_user.role}")
  return render_template("user_dashboard.html", username=current_user.id)

@user_bp.route("/create", methods=["POST"])
@login_required
@roles_required("user")
def create_batch():
  '''
  Accept JSON: { "batch_id": str, "details": {...} }
  Creates a new block in the blockchain
    data = {
      "actor": <username>,
      "action": f"Created batch {batch_id}",
      "bactch_id": <batch_id>,
      "details": <optional dict>,
      "timestamp": time.ctime()
    }
  '''

  # BC = Blockchain()
  # bc.add_block(new_data)
  # return jsonify({ "block_index": bc.chain[-1].index }), 201

  payload = request.get_json() or {}
  batch_id = payload.get("batch_id","").strip()
  details = payload.get("details", {})

  if not batch_id:
    abort(400, "batch_id is required")
  
  new_data = {
    "actor": current_user.id,
    "action": f"Created batch {batch_id}",
    "batch_id": batch_id,
    "details": details,
    "timestamp": time.ctime()
  }
  BC.add_block(new_data)

  return jsonify({"message": "Batch Created", "block_index": BC.chain[-1].index}), 201

@user_bp.route("/transfer", methods=["POST"])
@login_required
@roles_required("user")
def transfer_batch():
  '''
  Accept JSON: { "batch_id": str, "to": str }
  Adds a new block recording the transfer
  '''
  # BC = Blockchain()

  payload = request.get_json() or {}
  batch_id = payload.get("batch_id", "").strip()
  to_actor = payload.get("to", "").strip()

  if not batch_id or not to_actor:
    return abort(400, "batch_id and to (next actor) are required")
  
  new_data = {
    "actor": current_user.id,
    "action": f"Transferred batch {batch_id} to {to_actor}",
    "batch_id": batch_id,
    "time_stamp": time.ctime()
  }
  BC.add_block(new_data)

  return jsonify({"message": "Batch transferred", "block_index": BC.chain[-1].index}), 201

@user_bp.route("/history/<string:batch_id>", methods=["GET"])
@login_required
@roles_required("user")
def batch_history(batch_id):
  '''
  Returns a combined timeline of block events and admin concerns for the given batch_id
  '''
  # 1. Gather all blocks for this batch
  block_events = []
  for blk in BC.chain:
    data = blk.data
    if data.get("batch_id") == batch_id:
      block_events.append({
        "type": "block",
        "index": blk.index,
        "timestamp": blk.timestamp,
        "data": data
      })
    if not block_events:
      return jsonify({"message": f"No history found for batch {batch_id}"}), 404
    
  # 2. Load concerns and filter those on our block indices
  concerns = load_concerns()
  concern_events = []
  batch_indices = {ev["index"] for ev in block_events}
  for c in concerns:
    idx = c.get("block_index")
    if idx in batch_indices:
      concern_events.append({
        "type": "concern",
        "block_index": idx,
        "issue": c.get("issue"),
        "raised_by": c.get("raised_by"),
        "raised_at": c.get("raised_at")
      })

  # 3. Combine & sort by (index, then block before concern)
  def sort_key(ev):
    idx = ev["index"] if ev["type"] == "block" else ev["block_index"]
    order = 0 if ev["type"] == "block" else 1
    return (idx, order)
  
  timeline = sorted(block_events + concern_events, key=sort_key)

  return jsonify(timeline), 200
