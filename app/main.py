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

app.include_router(user_router)
app.include_router(goal_router)
app.include_router(checkin_router)
app.include_router(audit_router)
app.include_router(report_router)

@app.get("/")
def root():
    return {"message": "Backend Running Successfully"}