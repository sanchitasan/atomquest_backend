from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.auth.role_checker import verify_role
from app.models.auditlog import AuditLog

router = APIRouter()


@router.get("/audit-logs")
def get_audit_logs(
        db: Session = Depends(get_db),
        user=Depends(verify_role("admin")),
        page: int = Query(1, ge=1, description="Page number (starting from 1)"),
        limit: int = Query(10, ge=1, le=100, description="Items per page (max 100)")
):
    # Calculate offset
    offset = (page - 1) * limit

    # Get total count of logs
    total_count = db.query(AuditLog).count()

    # Get paginated logs
    logs = db.query(AuditLog).order_by(
        AuditLog.timestamp.desc()
    ).offset(offset).limit(limit).all()

    # Calculate total pages
    total_pages = (total_count + limit - 1) // limit

    return {
        "data": logs,
        "pagination": {
            "page": page,
            "limit": limit,
            "total_count": total_count,
            "total_pages": total_pages,
            "has_next": page < total_pages,
            "has_prev": page > 1
        }
    }
