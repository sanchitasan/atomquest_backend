from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import get_db
from app.auth.role_checker import verify_role
from app.models.checkin import CheckIn
from app.models.goal import Goal
from app.schemas.checkin import CheckInCreate
from app.utils.audit import create_audit_log
from app.utils.progress import (
    calculate_progress,
    calculate_status
)


DEMO_MODE = True
router = APIRouter()


@router.post("/checkins")
def create_checkin(
    checkin: CheckInCreate,
    db: Session = Depends(get_db),
    user=Depends(verify_role("employee"))
):

    goal = db.query(Goal).filter(
        Goal.id == checkin.goal_id,
        Goal.employee_id == user["user_id"]
    ).first()

    if not goal:

        raise HTTPException(
            status_code=404,
            detail="Goal not found"
        )

    if goal.status != "approved":

        raise HTTPException(
            status_code=400,
            detail="Goal must be approved before check-in"
        )

    existing_checkin = db.query(CheckIn).filter(
        CheckIn.goal_id == checkin.goal_id,
        CheckIn.quarter == checkin.quarter
    ).first()

    if existing_checkin:

        raise HTTPException(
            status_code=400,
            detail="Check-in already submitted for this quarter"
        )

    allowed_windows = {
        "Q1": [7],
        "Q2": [10],
        "Q3": [1],
        "Q4": [3, 4]
    }

    current_month = datetime.now().month

    if not DEMO_MODE:

        if current_month not in allowed_windows[checkin.quarter]:
            raise HTTPException(
                status_code=400,
                detail="Window is closed"
            )

    progress_score = calculate_progress(
        goal,
        checkin.actual_value
    )

    status = calculate_status(
        progress_score
    )

    new_checkin = CheckIn(

        quarter=checkin.quarter,

        planned_value=checkin.planned_value,

        actual_value=checkin.actual_value,

        progress_score=progress_score,

        status=status,

        employee_comment=checkin.employee_comment,

        goal_id=checkin.goal_id
    )

    db.add(new_checkin)

    create_audit_log(
        db=db,
        action="Quarterly Check-In Submitted",
        performed_by=user["email"],
        entity="CheckIn",
        role=user.get("role"),
        entity_id=new_checkin.id,

        old_value=None,

        new_value=f"""
    Quarter: {checkin.quarter}
    Planned: {checkin.planned_value}
    Actual: {checkin.actual_value}
    Progress Score: {progress_score}
    Status: {status}
    """,

        details=f"""
    Employee submitted {checkin.quarter} check-in
    for goal '{goal.title}'
    """
    )

    db.commit()

    db.refresh(new_checkin)

    return {

        "message": "Check-in submitted successfully"
    }


@router.get("/checkins")
def get_checkins(
    db: Session = Depends(get_db),
    user=Depends(verify_role("employee"))
):

    checkins = db.query(CheckIn).join(Goal).filter(
        Goal.employee_id == user["user_id"]
    ).all()

    response = []

    for checkin in checkins:
        response.append({

            "id": checkin.id,

            "quarter": checkin.quarter,

            "planned_value": checkin.planned_value,

            "actual_value": checkin.actual_value,

            "progress_score": checkin.progress_score,

            "status": checkin.status,

            "employee_comment": checkin.employee_comment,

            "manager_comment": checkin.manager_comment,

            "goal_id": checkin.goal_id,

            "created_at": checkin.created_at
        })

    return response