from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.auth.role_checker import verify_role
from app.models.checkin import CheckIn
from app.models.goal import Goal
from app.schemas.checkin import CheckInCreate
from app.utils.audit import create_audit_log

router = APIRouter()

@router.post("/checkins")
def create_checkin(checkin: CheckInCreate,db: Session = Depends(get_db),user=Depends(verify_role("employee"))):

    goal = db.query(Goal).filter(
        Goal.id == checkin.goal_id
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

    if checkin.progress > 100:
        raise HTTPException(
            status_code=400,
            detail="Progress cannot exceed 100%"
        )

    new_checkin = CheckIn(
        quarter=checkin.quarter,
        progress=checkin.progress,
        remarks=checkin.remarks,
        goal_id=checkin.goal_id
    )

    db.add(new_checkin)

    db.commit()

    create_audit_log(
        db=db,
        action="Quarterly Check-In Submitted",
        performed_by="employee@gmail.com",
        entity="CheckIn"
    )

    db.refresh(new_checkin)

    return {
        "message": "Check-in submitted successfully"
    }

@router.get("/checkins")
def get_checkins(db: Session = Depends(get_db)):

    checkins = db.query(CheckIn).all()

    return checkins