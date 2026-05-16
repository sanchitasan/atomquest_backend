from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.auth.role_checker import verify_role
from app.models.auditlog import AuditLog

router = APIRouter()

@router.get("/audit-logs")
def get_audit_logs(
    db: Session = Depends(get_db),user=Depends(verify_role("admin"))
):

    logs = db.query(AuditLog).all()

    return logs