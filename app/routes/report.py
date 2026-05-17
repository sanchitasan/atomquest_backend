from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models.goal import Goal
from app.models.user import User
from app.models.checkin import CheckIn
from app.models.auditlog import AuditLog
from fastapi.responses import FileResponse
import pandas as pd

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
        Goal.status == "submitted"
    ).count()

    rejected_goals = db.query(Goal).filter(
        Goal.status == "rejected"
    ).count()

    average_progress = db.query(
        func.avg(CheckIn.progress_score)
    ).scalar() or 0

    total_employees = db.query(User).filter(
        User.role == "employee"
    ).count()

    employees_with_checkins = db.query(
        CheckIn.goal_id
    ).distinct().count()

    total_managers = db.query(User).filter(
        User.role == "manager"
    ).count()

    return {
        "total_goals": total_goals,
        "approved_goals": approved_goals,
        "pending_goals": pending_goals,
        "rejected_goals": rejected_goals,
        "average_progress": average_progress,
        "total_employees": total_employees,
        "employees_completed_checkins":employees_with_checkins,
        "total_managers": total_managers,
    }

@router.get("/achievement-report")
def achievement_report(
    db: Session = Depends(get_db)
):

    checkins = db.query(CheckIn).all()

    report_data = []

    for checkin in checkins:

        goal = db.query(Goal).filter(
            Goal.id == checkin.goal_id
        ).first()

        employee = db.query(User).filter(
            User.id == goal.employee_id
        ).first()

        report_data.append({

            "Employee": employee.email,

            "Goal": goal.title,

            "Quarter": checkin.quarter,

            "Planned Target": checkin.planned_value,

            "Actual Achievement": checkin.actual_value,

            "Progress Score": checkin.progress_score,

            "Status": checkin.status
        })

    df = pd.DataFrame(report_data)

    file_path = "achievement_report.csv"

    df.to_csv(file_path, index=False)

    return FileResponse(

        path=file_path,

        filename="achievement_report.csv",

        media_type="text/csv"
    )
