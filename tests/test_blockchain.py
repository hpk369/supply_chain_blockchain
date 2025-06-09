import unittest
import time

from blockchain.block import Block
from blockchain.blockchain import Blockchain

class BlockchainTestCase(unittest.TestCase):
  
  def setUp(self):
    self.blockchain = Blockchain()

  def test_genesis_block(self):
    genesis = self.blockchain.chain[0]
    self.assertEqual(genesis.index, 0)
    self.assertEqual(genesis.data["message"], "Genesis Block")

  def test_add_blok(self):
    block_data = {
      "actor": "userA",
      "action": "Created batch B-001",
      "batch_id": "B-001",
      "details": {"info": "Initial batch"},
      "timestamp": time.ctime()
    }
    self.blockchain.add_block(block_data)
    self.assertEqual(len(self.blockchain.chain), 2)
    self.assertEqual(self.blockchain.chain[1].data["batch_id"], "B-001")

  def test_get_chain(self):
    chain = self.blockchain.get_chain()
    self.assertTrue(isinstance(chain, list))
    self.assertGreaterEqual(len(chain), 1)

  def test_is_valid(self):
    block_data = {
      "actor": "userA",
      "action": "Created batch B-002",
      "batch_id": "B-002",
      "details": {"info": "Some info"},
      "timestamp": time.ctime()
    }
    self.blockchain.and_block(block_data)
    self.assertTrue(self.blockchain.is_chain_valid())

  def test_invalid_chain(self):
    block_data = {
      "actor": "UserB",
      "action": "Created batch B-003",
      "batch_id": "B-003",
      "details": {"info": "Invalid test"},
      "timestamp": time.ctime()
    }
    self.blockchain.add_block(block_data)
    self.blockchain.chain[1].data["actor"] = "tampered"
    self.assertFalse(self.blockchain.is_chain_valid())

if __name__ == '__main__':
  unittest.main()