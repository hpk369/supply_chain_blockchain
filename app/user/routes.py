import time

from flask import Blueprint, render_template, jsonify, request, abort
from flask_login import login_required, current_user

from ..utils import roles_required
from blockchain.blockchain import Blockchain

user_bp = Blueprint("user", __name__, url_prefix="/user")

# Reuse the same Blockchain instance from admin (so they share ledger.json)
BC = Blockchain()

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
  payload = request.get_json() or {}
  batch_id = payload.get("batch_id","").strip()
  details = payload.get("details", {})

  if not batch_id:
    return abort(400, "batch_id is required")
  
  new_data = {
    "actor": current_user.id,
    "action": f"Created batch {batch_id}",
    "bactch_id": batch_id,
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
  Returns the histiry (all blocks) for a given batch_id
  '''
  chain = BC.chain  # List[Block]
  matches = [blk.to_dict() for blk in chain if blk.data.get("batch_id") == batch_id]

  if not matches:
    return jsonify({"message": f"No history found for batch {batch_id}"}), 404
  
  return jsonify(matches), 200