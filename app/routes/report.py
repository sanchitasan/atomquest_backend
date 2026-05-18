from fastapi.responses import StreamingResponse
from io import BytesIO
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

    total_users = db.query(User).count()

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

    total_admins = db.query(User).filter(
        User.role == "admin"
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
        "total_admins": total_admins,
        "total_users": total_users,
    }
def build_report_dataframe(db: Session):

    checkins = db.query(CheckIn).all()

    report_data = []

    for checkin in checkins:

        goal = db.query(Goal).filter(
            Goal.id == checkin.goal_id
        ).first()

        if not goal:
            continue

        employee = db.query(User).filter(
            User.id == goal.employee_id
        ).first()

        report_data.append({

            "Employee Email":
                employee.email if employee else "N/A",

            "Goal Title":
                goal.title,

            "Quarter":
                checkin.quarter,

            "Planned Target":
                checkin.planned_value,

            "Actual Achievement":
                checkin.actual_value,

            "Progress Score":
                checkin.progress_score,

            "Goal Status":
                goal.status,

            "Checkin Status":
                checkin.status,

            "Manager Comment":
                checkin.manager_comment,

            "Employee Comment":
                checkin.employee_comment,
        })

    return pd.DataFrame(report_data)



@router.get("/reports/export/csv")
def export_csv_report(
    db: Session = Depends(get_db)
):

    df = build_report_dataframe(db)

    stream = BytesIO()

    df.to_csv(stream, index=False)

    stream.seek(0)

    return StreamingResponse(

        iter([stream.getvalue()]),

        media_type="text/csv",

        headers={
            "Content-Disposition":
                "attachment; filename=governance_report.csv"
        }
    )


@router.get("/reports/export/excel")
def export_excel_report(
    db: Session = Depends(get_db)
):

    df = build_report_dataframe(db)

    stream = BytesIO()

    with pd.ExcelWriter(
        stream,
        engine="openpyxl"
    ) as writer:

        df.to_excel(
            writer,
            index=False,
            sheet_name="Governance Report"
        )

    stream.seek(0)

    return StreamingResponse(

        iter([stream.getvalue()]),

        media_type=(
            "application/vnd.openxmlformats-"
            "officedocument.spreadsheetml.sheet"
        ),

        headers={
            "Content-Disposition":
                "attachment; filename=governance_report.xlsx"
        }
    )