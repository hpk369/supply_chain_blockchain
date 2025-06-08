import json
import time
from pathlib import Path
from typing import List, Dict, Any

from .block import Block

class Blockchain:
  def __init__(self, ledger_path: str = "data/ledger.json"):
    self.ledger_path = Path(ledger_path)
    self.chain: List[Block] = []
    self.batch_index_map: Dict[str, int] = {}
    self.batch_events_map: Dict[str, List[int]] = {}
    self.load_chain_or_create_genesis()

  def create_genesis_block(self) -> None:
    # Create the first block (genesis) with index 0 and previous_hash "0".
    genesis = Block (
      index = 0,
      timestamp = time.ctime(),
      data = {"message": "Genesis Block"},
      previous_hash = "0",
      status="confirmed"
    )
    self.chain.append(genesis)
    self._update_batch_maps(genesis)

  def add_block(self, data: Dict[str, Any], status: str = "confirmed") -> Block:
    # Add a new block with the given data, at the end of the chain
    last_block = self.chain[-1]
    new_block = Block(
      index = len(self.chain),
      timestamp = time.ctime(),
      data = data,
      previous_hash = last_block.hash,
      status = status
    )
    self.chain.append(new_block)
    self._update_batch_maps(new_block)
    self.save_chain()
    return new_block
  
  def _update_batch_maps(self, block: Block) -> None:
    batch_id = block.data.get("batch_id")
    if batch_id:
      self.batch_index_map[batch_id] = block.index
      self.batch_events_map.setdefault(batch_id, []).append(block.index)

  def save_chain(self) -> None:
    # Dump the entire chain to a JSON file
    with open(self.ledger_path, "w") as f:
      json.dump([blk.to_dict() for blk in self.chain], f, indent=4)

  def is_chain_valid(self) -> bool:
    '''
    Verify chain integrity by:
    1. Recalculating each block's hash and comparing to stored hash.
    2. Ensuring previous_hash of each block matches the hash of the block before it.
    '''
    for i in range(1, len(self.chain)):
      current = self.chain[i]
      previous = self.chain[i - 1]

      # Recalculate and compare hash
      if current.hash != current.calculate_hash():
        return False
      
      # Check link consistency
      if current.previous_hash != previous.hash:
        return False
      
    return True
  
  def load_chain_or_create_genesis(self) -> None:
    '''
    Attempt to load the chain from ledger_path
    If the file doesn't exist or is invalid JSON, create a genesis block and save.
    '''
    try:
      raw = json.loads(self.ledger_path.read_text())
      for blk_data in raw:
        blk = Block(
          index=blk_data["index"],
          timestamp=blk_data["timestamp"],
          data=blk_data["data"],
          previous_hash=blk_data["previous_hash"],
          status=blk_data.get("status", "confirmed")
        )
        blk.hash = blk_data["hash"]
        self.chain.append(blk)
        self._update_batch_maps(blk)
    except(FileNotFoundError, json.JSONDecodeError):
      self.create_genesis_block()
      self.save_chain()

  def print_chain(self) -> None:
    # Print all block in the chain for debugging or demonstration.
    for blk in self.chain:
      print(blk.to_dict())

# if __name__ == "__main__":
#   bc = Blockchain()

#   dummy_events = [
#     {"actor": "Manufacturer A", "action": "Created batch #001"},
#     {"actor": "Distributor B", "action": "Received batch #001"},
#     {"actor": "Retailer C", "action": "Stocked batch #001"},
#   ]

#   for event in dummy_events:
#     bc.add_block(event)

#   bc.print_chain()