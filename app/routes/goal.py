from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.role_checker import verify_role
from app.database import get_db
from app.models.goal import Goal
from app.schemas.goal import GoalCreate

from app.utils.audit import create_audit_log

router = APIRouter()

@router.post("/goals")
def create_goal(goal: GoalCreate, db: Session = Depends(get_db), user=Depends(verify_role("employee"))):


    # Rule 1: Minimum weightage
    if goal.weightage < 10:
        raise HTTPException(
            status_code=400,
            detail="Minimum weightage is 10"
        )

    # Rule 2: Maximum 8 goals
    existing_goals = db.query(Goal).filter(
        Goal.employee_id == goal.employee_id
    ).count()

    if existing_goals >= 8:
        raise HTTPException(
            status_code=400,
            detail="Maximum 8 goals allowed"
        )

    # Rule 3: Total weightage <= 100
    total_weightage = db.query(Goal).filter(
        Goal.employee_id == goal.employee_id
    ).all()

    current_total = sum(
        g.weightage for g in total_weightage
    )

    if current_total + goal.weightage > 100:
        raise HTTPException(
            status_code=400,
            detail="Total weightage cannot exceed 100"
        )

    new_goal = Goal(
        title=goal.title,
        description=goal.description,
        uom=goal.uom,
        target_value=goal.target_value,
        weightage=goal.weightage,
        employee_id=goal.employee_id
    )

    db.add(new_goal)

    db.commit()

    db.refresh(new_goal)

    return {
        "message": "Goal created successfully",
        "goal_id": new_goal.id
    }

@router.put("/goals/{goal_id}/approve")
def approve_goal(goal_id: int,db: Session = Depends(get_db),user=Depends(verify_role("manager"))):

    goal = db.query(Goal).filter(
        Goal.id == goal_id
    ).first()

    if not goal:
        raise HTTPException(
            status_code=404,
            detail="Goal not found"
        )

    goal.status = "approved"

    db.commit()
    create_audit_log(
        db=db,
        action="Goal Approved",
        performed_by="manager@gmail.com",
        entity="Goal"
    )

    return {
        "message": "Goal approved successfully"
    }

@router.put("/goals/{goal_id}/reject")
def reject_goal(goal_id: int,db: Session = Depends(get_db),user=Depends(verify_role("manager"))):

    goal = db.query(Goal).filter(
        Goal.id == goal_id
    ).first()

    if not goal:
        raise HTTPException(
            status_code=404,
            detail="Goal not found"
        )

    goal.status = "rejected"

    db.commit()

    create_audit_log(
        db=db,
        action="Goal Rejected",
        performed_by="manager@gmail.com",
        entity="Goal"
    )

    return {
        "message": "Goal rejected successfully"
    }

@router.get("/goals")
def get_goals(db: Session = Depends(get_db)):
    goals = db.query(Goal).all()
    return goals