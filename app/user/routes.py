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
  if not batch_id:
    abort(400, "batch_id is required")
  if batch_id in BC.batch_index_map:
    abort(400, "Batch ID already exists")
  
  data = {
    "actor": current_user.id,
    "action": f"Created batch {batch_id}",
    "batch_id": batch_id,
    "details": payload.get("details", {}),
    "timestamp": time.ctime()
  }
  new_block = BC.add_block(data, status="confirmed")
  return jsonify({"message": "Block created", "block_index": new_block.index}), 201

@user_bp.route("/transfer", methods=["POST"])
@login_required
@roles_required("user")
def transfer_batch():
  '''
  Accept JSON: { "batch_id": str, "to": str }
  Adds a new block recording the transfer
  '''
  payload = request.get_json() or {}
  batch_id = payload.get("batch_id", "").strip()
  to_actor = payload.get("to", "").strip()
  if not batch_id or not to_actor:
    abort(400, "batch_id and to are required")

  # Ensure batch exists and actor matches current owner
  if batch_id not in BC.batch_index_map:
    abort(404, f"Batch {batch_id} not found")
  current_index = BC.batch_index_map[batch_id]
  owner = BC.chain[current_index].data.get("actor")
  if current_user.id != owner:
    abort(403, "Only the current owner can transfer this batch")

  data = {
    "actor": to_actor,
    "action": f"Transferred batch {batch_id} to {to_actor}",
    "batch_id": batch_id
  }
  new_block = BC.add_block(data, status="pending")
  return jsonify({"message": "Transfer pending approval", "block_index": new_block.index}), 202

@user_bp.route("/history/<string:batch_id>", methods=["GET"])
@login_required
@roles_required("user")
def batch_history(batch_id):
  '''
  Returns a combined timeline of block events and admin concerns for the given batch_id
  '''
  # Ensure batch exists
  if batch_id not in BC.batch_index_map:
      return jsonify({"message": f"No history found for batch {batch_id}"}), 404

  # Check ownership
  current_index = BC.batch_index_map[batch_id]
  owner = BC.chain[current_index].data.get("actor")
  if current_user.id != owner:
      abort(403, "You are not authorized to view this batch history")

  # Scan entire chain for this batch_id
  blocks = [
      blk.to_dict()
      for blk in BC.chain
      if "batch_id" in blk.data and blk.data["batch_id"] == batch_id
  ]

  if not blocks:
      return jsonify({"message": f"No history found for batch {batch_id}"}), 404

  # Load concerns
  from app.admin.routes import load_concerns
  concerns = load_concerns()
  batch_concerns = [c for c in concerns if c.get("batch_id") == batch_id]

  return jsonify({
      "blocks": blocks,
      "concerns": batch_concerns
  }), 200