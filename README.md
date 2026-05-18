# 🚀 AtomQuest Backend

AtomQuest Backend is the core API service powering the **AtomQuest Goal & KPI Management Platform**.  
It provides secure, scalable, and role-based APIs for Employees, Managers, and Admins to manage goals, quarterly check-ins, approvals, analytics, and audit workflows.

Built with **FastAPI**, the backend follows a modular architecture focused on performance, maintainability, and enterprise workflow management.

---

# 🌐 Live System Overview

The backend integrates with the AtomQuest frontend and database layer to provide:

- Goal Creation & Approval Workflow
- Quarterly KPI Tracking
- Shared Goal Management
- Manager Review System
- Audit Logging
- Role-Based Access Control (RBAC)
- Reporting & Dashboard Analytics

---

# 🏗️ System Architecture

```mermaid
graph TD

    subgraph Frontend
        FE[React + Vite Frontend]
    end

    subgraph Backend["atomquest_backend (FastAPI API)"]

        Router[FastAPI Router /api]

        subgraph Endpoints
            Auth[/login /users]
            Goals[/goals /goals/my /goals/submit]
            Manager[/manager/team-progress]
            Checkins[/checkins]
            Reports[/dashboard/stats]
            Audit[/audit-logs]
        end

        subgraph Services
            AuthService[JWT Authentication]
            GoalService[Goal & KPI Engine]
            RBAC[Role-Based Middleware]
            AuditService[Audit Logger]
        end
    end

    subgraph Database
        DB[(MySQL / PostgreSQL)]
    end

    FE --> Router

    Router --> Auth
    Router --> Goals
    Router --> Manager
    Router --> Checkins
    Router --> Reports
    Router --> Audit

    Auth --> AuthService
    Goals --> GoalService
    Manager --> GoalService
    Checkins --> GoalService

    GoalService --> RBAC
    Reports --> RBAC
    Audit --> AuditService

    AuthService --> DB
    GoalService --> DB
    AuditService --> DB
```

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

```mermaid
sequenceDiagram

    participant FE as Frontend
    participant API as FastAPI Backend
    participant SEC as JWT/RBAC Middleware
    participant SVC as Service Layer
    participant DB as Database

    FE->>API: API Request

    API->>SEC: Validate JWT Token

    alt Unauthorized
        SEC-->>FE: 401 Unauthorized

    else Authorized

        API->>SEC: Verify User Role

        alt Forbidden
            SEC-->>FE: 403 Forbidden

        else Access Granted

            API->>SVC: Execute Business Logic

            SVC->>DB: SQL Transaction

            DB-->>SVC: Success Response

            SVC-->>FE: 200 OK + Data

        end
    end
```

---

# 📈 Goal Lifecycle Workflow

The backend maintains strict workflow states to ensure organizational KPI consistency and auditability.

```mermaid
stateDiagram-v2

    [*] --> Draft : Create Goal

    Draft --> Pending : Submit Goal

    state "Manager Review" as Review {

        Pending --> Approved : Approve Goal
        Pending --> Rejected : Reject Goal

    }

    Rejected --> Draft : Edit & Resubmit

    Approved --> InProgress : Quarterly Check-ins

    InProgress --> Completed : Target Achieved

    Completed --> Locked : Finalized

    Locked --> Draft : Unlock by Admin
```

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
git clone https://github.com/sanchitasan/atomquest_backend.git
cd atomquest_backend
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
✅ Exportable Reporting APIs  

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

Team Members:
- Shruti
- Sanchita
- AtomQuest Team

---

# 📄 License

This project is licensed under the MIT License.

---

# 🔗 Related Repositories

## Frontend
https://github.com/sanchitasan/atomquest_frontend

## Backend
https://github.com/sanchitasan/atomquest_backend

---
