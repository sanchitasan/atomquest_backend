from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models.goal import Goal
from app.models.checkin import CheckIn

router = APIRouter()

@router.get("/dashboard-stats")
def dashboard_stats(
    db: Session = Depends(get_db)
):

    total_goals = db.query(Goal).count()

    approved_goals = db.query(Goal).filter(
        Goal.status == "approved"
    ).count()

    pending_goals = db.query(Goal).filter(
        Goal.status == "pending"
    ).count()

    rejected_goals = db.query(Goal).filter(
        Goal.status == "rejected"
    ).count()

    average_progress = db.query(
        func.avg(CheckIn.progress)
    ).scalar()

    return {
        "total_goals": total_goals,
        "approved_goals": approved_goals,
        "pending_goals": pending_goals,
        "rejected_goals": rejected_goals,
        "average_progress": average_progress
    }