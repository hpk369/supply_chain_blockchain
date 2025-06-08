import hashlib
import json
from typing import Any, Dict

class Block:
  def __init__(self, index: int, timestamp: str, data: Dict[str, Any], previous_hash: str, status: str = "confirmed"):
    self.index = index
    self.timestamp = timestamp
    self.data = data
    self.previous_hash = previous_hash
    self.status = status # "pending", "confirmed", or "denied"
    self.hash = self.calculate_hash()

  def calculate_hash(self) -> str:
     
    '''
    Calculate SHA-256 hash based on block content.
    We convert the index, timestamp, data, and previous_hash into a JSON string, then hash it.
    '''
    
    block_content = {
      "index": self.index,
      "timestamp": self.timestamp,
      "data": self.data,
      "previous_hash": self.previous_hash,
      "status": self.status
    }
    block_string = json.dumps(block_content, sort_keys=True).encode()
    return hashlib.sha256(block_string).hexdigest()
  
  def to_dict(self) -> Dict[str, Any]:
    # Convert the block into a dictionary for saving or printing.
    return {
      "index": self.index,
      "timestamp": self.timestamp,
      "data": self.data,
      "previous_hash": self.previous_hash,
      "status": self.status,
      "hash": self.hash
    }