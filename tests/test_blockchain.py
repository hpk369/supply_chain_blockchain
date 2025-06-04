import os
import json
import unittest

from blockchain.block import Block
from blockchain.blockchain import Blockchain

class TestBlockchain(unittest.TestCase):
  def setUp(self):
    # Before each test, remove any existing ledger file so that we start with a clean chain (onlt genesis block)
    try:
      os.remove("data/ledger.json")
    except FileNotFoundError:
      pass

    # Initialize a fresh Blockchain instance
    self.bc = Blockchain()

  def test_genesis_block(self):
    '''
    Ensure that upon initialization (with non prior ledger.json), the
    chain contains exactly one genesis block, with index 0 and previous_hash="0".
    '''
    self.assertEqual(len(self.bc.chain), 1)
    genesis = self.bc.chain[0]
    self.assertEqual(genesis.index, 0)
    self.assertEqual(genesis.previous_hash, "0")
    self.assertIsInstance(genesis.hash, str)
    self.assertTrue(len(genesis.hash) > 0)

  def test_add_block(self):
    '''
    After adding a new block with some dummy data, the chain should increase by 1,
    the new block's data should match, previous_hash should link to the last block's
    hash, and the overall chain should remain valid.
    '''
    data = {"actor": "testActor", "action": "Performed test action"}
    prev_length = len(self.bc.chain)

    self.bc.add_block(data)

    # Chain length has increased by 1
    self.assertEqual(len(self.bc.chain), prev_length + 1)

    new_block = self.bc.chain[-1]
    # Data is stored correctly
    self.assertDictEqual(new_block.data, data)
    # previous_hash matches the hash of the block before it
    self.assertEqual(new_block.previous_hash, self.bc.chain[-2].hash)
    # Chain validation still remains True
    self.assertTrue(self.bc.is_chain_valid())

  def test_chain_persistance(self):
    '''
    Verify that after adding a block and saving, creating a new Blockchain instance
    reloads the same data from data/ledger.json. The last block's data on the reload
    chain should match what was added
    '''
    data = {"actor": "PersistActor", "action": "Persistance test"}
    self.bc.add_block(data)

    # Create a second instance to load from disk
    bc2 = Blockchain()

    # The new instance should have atleast 2 block now
    self.assertGreaterEqual(len(bc2.chain), 2)

    last_block = bc2.chain[-1]
    # The data added from disk should match what we added
    self.assertDictEqual(last_block.data, data)

  def test_chain_validity_with_tampering(self):
    '''
    Simulating tampering: after adding a block, change its data in memory and confirm
    that is_chain_valid() returns False.
    '''
    self.bc.add_block({"actor": "Original", "action": "Legit action"})

    # Tamper with block 1's data
    self.bc.chain[1].data = {"actor": "EvilActor", "action": "Tampered action"}

    # Tha hash stored in the block no longer matches the recalculated hash
    self.assertFalse(self.bc.is_chain_valid())


if __name__ == "__main__":
  unittest.main()