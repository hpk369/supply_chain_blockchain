import json
import unittest
from main import app
from blockchain.blockchain import Blockchain

class UserActionsTestCase(unittest.TestCase):
  def setUp(self):
    self.client = app.test_client()
    # Ensure a fresh ledger.json for each test
    try:
      import os
      os.remove("data/ledger.json")
    except FileNotFoundError:
      pass
    self.bc = Blockchain()  # Recreate with only genesis block

  def login_as_user(self):
    return self.client.post("/login", data={
      "username": "userA",
      "password": "userApass"
    }, follow_redirects=True)
  
  def test_create_and_history(self):
    # Log in as userA
    res = self.login_as_user()
    self.assertEqual(res.status_code, 200)

    # Create batch B-TEST
    payload = {"batch_id": "B-TEST", "details": {"info": "test"}}
    res = self.client.post("/user/create", json=payload, follow_redirects=True)
    self.assertEqual(res.status_code, 201)
    obj = json.loads(res.data)
    self.assertIn("block_index", obj)

    # Fetch history of B-TEST
    res = self.client.get("/user/history/B-TEST")
    self.assertEqual(res.status_code, 200)
    history = json.loads(res.data)
    self.assertEqual(len(history), 1)
    self.assertEqual(history[0]["data"]["batch_id"], "B-TEST")

if __name__ == "__main__":
  unittest.main()