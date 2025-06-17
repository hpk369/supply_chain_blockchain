# Blockchain-based Supply Chain Tracker

A full-stack web application that leverages blockchain principles to track, transfer, and verify supply chain batch records with **admin approval**, **tamper-proof history**, and **role-based access**.

---

## Features

- Immutable ledger using blockchain data structures
- User-initiated batch transfers with admin approval workflow
- View detailed batch history: created, transferred, flagged
- Raise and manage concerns as an admin
- Flask-Login authentication for User/Admin roles
- Tested with unit tests for blockchain logic and user workflows
- Dockerized for easy deployment

---

## Tech Stack

- **Python 3.11**, **Flask**, **Flask-Login**
- **HTML**, **CSS**, **Vanilla JS**
- **Docker**, **Docker Compose**
- **Jinja2 Templates**
- **Python unittest**

---

## Project Structure

```bash
supply_chain_blockchain/
├── app/
│   ├── admin/
│   ├── user/
│   ├── templates/
│   ├── static/
│   ├── utils.py
│   └── auth.py
├── blockchain/
│   ├── block.py
│   └── blockchain.py
├── data/
│   ├── ledger.json
│   └── concerns.json
├── tests/
│   ├── test_blockchain.py
│   ├── test_user_actions.py
│   └── test_admin_actions.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── main.py
```

---

## Getting Started

### Run Locally

1. **Clone the repo**

```bash
git clone https://github.com/hpk369/supply_chain_blockchain.git
cd supply_chain_blockchain
```

2. **Install dependencies**

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. **Run the app**

```bash
python main.py
```

Open your browser at [http://127.0.0.1:9567](http://127.0.0.1:9567)

---

### Run with Docker

```bash
docker-compose build
docker-compose up
```

---

## Running Tests

```bash
python -m unittest discover tests
```

---

## How it Works

1. **User** creates a new batch
2. **User** initiates a transfer → saved as a **pending block**
3. **Admin** can approve/deny the transfer from dashboard
4. All actions are recorded in **ledger.json** with full traceability
5. **Concerns** can be raised by Admin and viewed in history

---

## Use Case

This app is ideal for demonstrating:
- Understanding of blockchain principles
- Role-based authorization and state handling
- Clean architecture and secure web design
- Real-world logistics and auditing simulation