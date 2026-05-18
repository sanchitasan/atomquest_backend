# 🚀 AlignIQ Backend

AAlignIQ Backend is the core API service powering the **AlignIQ Goal & Shared goal Management Platform**.  
It provides secure, scalable, and role-based APIs for Employees, Managers, and Admins to manage goals, quarterly check-ins, approvals, analytics, and audit workflows.

Built with **FastAPI**, the backend follows a modular architecture focused on performance, maintainability, and enterprise workflow management.

---

# 🌐 Live System Overview

The backend integrates with the AtomQuest frontend and database layer to provide:

- Goal Creation & Approval Workflow
- Quarterly goal Tracking
- Shared Goal Management
- Manager Review System
- Audit Logging
- Role-Based Access Control (RBAC)
- Reporting & Dashboard Analytics

---

# 🏗️ System Architecture

---

# ⚙️ Tech Stack

| Layer | Technology |
|---|---|
| Backend Framework | FastAPI |
| Language | Python |
| ORM | SQLAlchemy |
| Database | MySQL / PostgreSQL |
| Authentication | JWT |
| Password Hashing | Passlib (bcrypt) |
| Validation | Pydantic |
| Server | Uvicorn |
| Environment Config | python-dotenv |

---

# 📦 Key Dependencies

## Core Packages

```bash
fastapi
uvicorn
sqlalchemy
pydantic
python-dotenv
psycopg2-binary
```

## Security Packages

```bash
python-jose[cryptography]
passlib[bcrypt]
python-multipart
```

---

# 🔄 API Request Lifecycle

Every request from the frontend passes through authentication, RBAC validation, business logic processing, and database transactions.


---

# 📈 Goal Lifecycle Workflow

The backend maintains strict workflow states to ensure organizational Shared goal consistency and auditability.


---

# 👥 Role-Based Access Control (RBAC)

| Role | Capabilities |
|---|---|
| Employee | Create goals, submit check-ins, track own KPIs |
| Manager | Approve/reject goals, monitor teams, assign shared goals |
| Admin | Manage users, unlock goals, view reports, access audit logs |

---

# 🧩 Core Modules

## 🔐 Authentication Module
- JWT-based login system
- Secure password hashing
- Token validation middleware
- Protected route access

---

## 🎯 Goal Management Module
- Goal creation & submission
- KPI target tracking
- Shared goal support
- Weightage validation
- Goal locking workflow

---

## 📊 Quarterly Check-ins
- Progress tracking
- Planned vs Actual updates
- Manager feedback system
- Goal status monitoring

---

## 🧾 Audit Logging
Tracks:
- Goal edits
- Status changes
- Approval history
- Admin unlock actions

---

## 📈 Reporting & Analytics
- Dashboard statistics
- KPI summaries
- Completion tracking
- Employee performance insights

---

# 🗂️ Backend Folder Structure

```bash
atomquest_backend/
│
├── app/
│   ├── models/
│   ├── routes/
│   ├── schemas/
│   ├── services/
│   ├── middleware/
│   ├── database/
│   └── utils/
│
├── main.py
├── requirements.txt
├── .env
└── README.md
```

---

# 🚀 Setup & Installation

## 1️⃣ Clone Repository

```bash
git clone https://github.com/sanchitasan/AlignIQ_backend.git
cd AlignIQ_backend
```

---

## 2️⃣ Create Virtual Environment

### Linux / Mac

```bash
python -m venv venv
source venv/bin/activate
```

### Windows

```bash
venv\Scripts\activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Configure Environment Variables

Create a `.env` file:

```env
DATABASE_URL=postgresql://user:password@localhost/atomquest
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

---

## 5️⃣ Run Development Server

```bash
uvicorn main:app --reload
```

Server will run at:

```bash
http://localhost:8000
```

Interactive API Docs:

```bash
http://localhost:8000/docs
```

---

# 🔐 Security Features

- JWT Authentication
- Password Hashing (bcrypt)
- Role-Based Route Protection
- Token Expiry Validation
- Secure API Middleware
- Protected Database Transactions

---

# 📌 Major Features Implemented

✅ Goal Approval Workflow  
✅ Shared Departmental Goals  
✅ Quarterly KPI Check-ins  
✅ Role-Based Dashboards  
✅ Audit Trail Logging  
✅ Manager Team Tracking  
✅ Real-Time Dashboard Stats  
✅ Goal Lock / Unlock System  
✅ Exportable Report in CSV and Excel Format

---

# 🌍 Deployment

| Service | Platform |
|---|---|
| Frontend | Vercel |
| Backend | Render |
| Database | MySQL / PostgreSQL |

---

# 📜 API Documentation

FastAPI automatically generates Swagger documentation.

Access:

```bash
/api/docs
```

or

```bash
/docs
```

---

# 🤝 Contributors

Developed for **AtomQuest Hackathon 1.0**

---

# 📄 License

This project is licensed under the MIT License.

---

# 🔗 Related Repositories

## Frontend
https://github.com/sanchitasan/AlignIQ_frontend

## Backend
https://github.com/sanchitasan/AlignIQ_backend

---
