from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from app.database import engine, Base
from app.models.user import User
from app.models.goal import Goal
from app.models.checkin import CheckIn
from app.models.auditlog import AuditLog
from app.routes.user import router as user_router
from app.routes.goal import router as goal_router
from app.routes.checkin import router as checkin_router
from app.routes.audit import router as audit_router
from app.routes.report import router as report_router


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173","https://atomquest-backend-anqi.onrender.com","http://localhost:5174"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router, prefix="/api")
app.include_router(goal_router, prefix="/api")
app.include_router(checkin_router, prefix="/api")
app.include_router(audit_router, prefix="/api")
app.include_router(report_router, prefix="/api")

@app.get("/")
def root():
    return {"message": "AtomQuest Backend Running Successfully"}

@app.get("/api")
def api_root():
    return {"message": "AtomQuest API v1.0", "status": "operational"}