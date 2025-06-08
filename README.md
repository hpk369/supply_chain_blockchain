Phase: Blockchain setup
1. Define a Block class with key blockchain componenets
2. Define a Blockchain class to manage the chain
3. Add methods to: Add new blocks, Validate the chain, and Print the chain
4. Save/load the blockchain from a JSON file
5. Include dummy supply chain data for testing

RESPONSIBILITY:
1. block.py -> Everything related tp a single block (its fields, hash calculations, and serialization).
2. blockchain.py -> Manages the list of blocks, handles add new blocks, verifies integrity, and persists the chain

Phase: Adding admin panel, user panel and dummy_script
1. Admin Panel:
   1. View all new entries in the blockchain:
      Endpoint - GET /admin/chain
      Action - Read data/ledger.json, return the entire chain history
   2. Raise Concerns/Flags on Specific Blocks:
      Endpoint - POST /admin/concern
      Input - { block_index: 5, issue: "Timestamp mismatch"}
      Action - Append to data/concerns.json (a simple list of objects: {block_index, issue, timestamp, raised_by})
   3. View all concerns:
      Endpoint - Get /adming/concerns
      Action - Read data/concerns.json and return a list
   4. Resolve or Clear a Concern
2. User Panel:
   1. Creating a New Product Batch:
      Endpoint: POST /user/create
      Input: { "actor": "Manufacturer A", "batch_id": "BATCH-001", "details": {...} }
      Action: Call blockchain.add_block(...) with data={"actor","action":"Created batch BATCH-001","details":{...}}
   2. Transfer a Batch to Next Actor:
      Endpoint: POST /user/transfer
      Input: { "actor": "Distributor B", "batch_id": "BATCH-001", "from": "Manufacturer A", "to": "Distributor B"}
      Action: Add a block: {"actor": actor, "action": f"Batch {batch_id} transferred from {from} to {to}", ...}
   3. View One's Own Product History:
      Endpoint: GET /user/history/<batch_id>
      Action: Load data/ledger.json, filter block["data"]["batch_id"] == batch_id, return a list of events for that batch.
   4. View All Products You've Created:
      Endpoint: GET /user/my_batches
      Action: From the chain, return all blocks where block["data"]["actor"] == <username> AND action contains "batch"


Revamp
1. Add status in each block for transfer approval. Status has three values: "pending", "confirmed", or "denied"
2. Only the rightful owner can initiate a transfer and view history of the batch
3. Added Approve and Deny buttons for admin panel
4. Once the transfer is Approved the actor also changes
5. Simple "Pending -> Approve" flow as consensus
6. In-memory map for fast lookups. History lookups become constant-time for the "current" owner. Transfer operations don't have to scan the ledger to find the block to update or to check existence
