import json
import os
import unittest
from main import app
from blockchain.blockchain import Blockchain

class AdminActionsTestCase(unittest.TestCase):
  def setUp(self):
    # Reset ledger and concerns
    try:
      os.remove("data/ledger.json")
    except FileNotFoundError:
      pass
    try:
      os.remove("data/concersn.json")
    except FileNotFoundError:
      pass
    self.bc = Blockchain()
    self.client = app.test_client()

  def login_as_admin(self):
    return self.client.post("/login", data={
      "username": "admin1",
      "password": "adminpass"
    }, follow_redirects=True)
  
  def test_view_chain_and_raise_concern(self):
    # Log in as admin
    res = self.login_as_admin()
    self.assertEqual(res.status_code, 200)

    # View chain: should return at least the genesis block
    res = self.client.get("/admin/chain")
    self.assertEqual(res.status_code, 200)
    chain_data = json.loads(res.data)
    self.assertIsInstance(chain_data, list)
    self.assertGreaterEqual(len(chain_data), 1)

    # Raise a concern on block 0
    payload = {"block_index": 0, "issue": "Test issue on genesis"}
    res = self.client.post("/admin/concerns", json=payload, follow_redirects=True)
    self.assertEqual(res.status_code, 201)
    c = json.loads(res.data)
    self.assertEqual(c["block_index"], 0)
    self.assertEqual(c["issue"], "Test issue on genesis")

    # Verify concerns list
    res = self.client.get("/admin/concerns")
    self.assertEqual(res.status_code, 200)
    concerns = json.loads(res.data)
    self.assertTrue(any(con["issue"] == "Test issue on genesis" for con in concerns))  
    
if __name__ == "__main__":
  unittest.main()