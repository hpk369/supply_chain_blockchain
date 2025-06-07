import requests
import time
import json

BASE_URL = 'https://localhost:9567'

def simulate():
  # userA creates a batch
  print("\n[1] userA creates batch BATCH-ABC")
  headers_userA = {
    "Authorization": "userA:userApass",
    "Content-Type": "application/json"
  }
  payload_create = {"batch_id": "BATCH-ABC"}
  resp = requests.post(f"{BASE_URL}/user/create", headers=headers_userA, json=payload_create)
  print("Response:", resp.status_code, resp.json())

  # userB transfers it
  print("\n[2] userB transfers BATCH-ABC to userC")
  headers_userB = {
    "Authorization": "userB:userBpass",
    "Content-Type": "application/json"
  }
  payload_transfer = {"batch_id": "BATCH-ABC", "to": "userC"}
  resp = requests.post(f"{BASE_URL}/user/transfer", headers=headers_userB, json=payload_transfer)
  print("Response:", resp.status_code, resp.json())

  # Admins views chain
  print("\n[3] admin1 views the blockchain")
  headers_admin = {
    "Authorization": "admin1:adminpass"
  }
  resp = requests.get(f"{BASE_URL}/admin/chain", headers=headers_admin)
  print("Chain data:", json.dumps(resp.json(), index=2))

  # Admin raises a concern on block index 2
  print("\n[4] admin1 raises a concern on block index 2")
  headers_admin["Content-Type"] = "application/json"
  payload_concern = {"block_index": 2, "issue": "Suspicious transfer time"}
  resp = requests.post(f"{BASE_URL}/admin/concern", headers=headers_admin, json=payload_concern)
  print("Conern Response:", resp.status_code, resp.json())

  # Admin views concerns
  print("\n[5] admin1 views all concerns")
  resp = requests.get(f"{BASE_URL}/admin/concerns", headers=headers_admin)
  print("Concerns:", json.dumps(resp.json(), indent=2))

if __name__ == "__main__":
  print("Please make sure flask server is running at https://localhost:9567 before proceeding ahead.")
  simulate()