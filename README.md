# Blockchain-based Supply Chain Tracker Web Application

A lightweight **Blockchain-powered Supply Chain Tracker Web App** built using Python and Flask.

Tracks **batch ownership**, **transfers**, **concerns**, and maintains an **immutable append-only ledger** with full auditability and role-based access control.

---

## Features

-> Create and manage supply chain batches  
-> User-initiated **transfer requests** with **Admin approval/denial flow**  
-> Admin can **raise concerns** on any batch  
-> Full **batch history view** — immutable ledger of all actions  
-> **Ownership validation** — only current owner can transfer/view  
-> Blockchain **integrity validation** — detects tampering  
-> Role-based access — User & Admin dashboards  
-> **Dockerized deployment** — ready for demo or production  
-> Comprehensive **unit tests** for blockchain, user, and admin actions

---

## Technologies Used

- **Python 3.11**
- **Flask** + Flask-Login
- Custom **Blockchain** implementation (Block + Blockchain classes)
- HTML / CSS / JS (Jinja templates)
- **Docker**, Docker Compose
- **Python unittest** for testing

---

## Project Structure

```plaintext
├── app/                # Flask app (auth, utils, user/admin routes)
├── blockchain/         # Blockchain and Block classes
├── data/               # Ledger and Concerns (persisted)
├── tests/              # Test files for Blockchain, User, Admin
├── requirements.txt    # Python dependencies
├── Dockerfile          # Build container image
├── docker-compose.yml  # Run with Docker
├── main.py             # Flask app entrypoint
└── README.md           # This file
