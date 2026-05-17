from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.role_checker import verify_role
from app.database import get_db
from app.models.goal import Goal
from app.models.user import User
from app.schemas.goal import GoalCreate
from app.schemas.manager_goal import (ManagerBulkGoalUpdate)
from app.utils.audit import create_audit_log
from app.schemas.shared_goal import SharedGoalCreate
import time

router = APIRouter()


def current_user_id(user: dict) -> int:
    return int(user["user_id"])


def get_manager_by_email(db: Session, manager_email: str) -> User:
    manager = db.query(User).filter(User.email == manager_email).first()

    if not manager:
        raise HTTPException(
            status_code=404,
            detail="Manager not found with this email"
        )

    if manager.role != "manager":
        raise HTTPException(
            status_code=400,
            detail="Selected user is not a manager"
        )

    return manager


@router.post("/goals")
def create_goal(
    goal: GoalCreate,
    db: Session = Depends(get_db),
    user=Depends(verify_role("employee")),
):
    employee_id = user["user_id"]
    manager = get_manager_by_email(db, goal.manager_email)

    if goal.weightage < 10:
        raise HTTPException(
            status_code=400,
            detail="Minimum weightage is 10"
        )

    existing_goals = db.query(Goal).filter(
        Goal.employee_id == employee_id
    ).count()

    if existing_goals >= 8:
        raise HTTPException(
            status_code=400,
            detail="Maximum 8 goals allowed"
        )

    employee_goals = db.query(Goal).filter(
        Goal.employee_id == employee_id
    ).all()

    current_total = sum(g.weightage for g in employee_goals)

    if current_total + goal.weightage > 100:
        raise HTTPException(
            status_code=400,
            detail="Total weightage cannot exceed 100"
        )

    new_goal = Goal(
        title=goal.title,
        description=goal.description,
        thrust_area=goal.thrust_area,
        uom=goal.uom,
        target_value=goal.target_value,
        weightage=goal.weightage,
        employee_id=employee_id,
        manager_id=manager.id,
        status="draft",
    )

    db.add(new_goal)
    db.commit()

    db.refresh(new_goal)
    create_audit_log(
        db=db,
        action="Goal Created",
        performed_by=user["email"],
        role=user.get("role"),
        entity="Goal",
        entity_id=new_goal.id,
        employee_email=user["email"],
        new_value=f"""
    Title: {new_goal.title}
    Weightage: {new_goal.weightage}
    Target: {new_goal.target_value}
    Status: {new_goal.status}
    """,
        details=f"Employee created goal '{new_goal.title}'"
    )

    db.commit()

    return {
        "message": "Goal submitted to manager for approval",
        "goal_id": new_goal.id,
        "manager_email": manager.email,
        "status": new_goal.status,
    }


@router.get("/goals/my")
def get_my_goals(
    db: Session = Depends(get_db),
    user=Depends(verify_role("employee")),
):
    goals = db.query(Goal).filter(
        Goal.employee_id == user["user_id"]
    ).all()

    response = []

    for goal in goals:

        manager = db.query(User).filter(
            User.id == goal.manager_id
        ).first()

        response.append({
            "id": goal.id,
            "title": goal.title,
            "description": goal.description,
            "thrust_area": goal.thrust_area,
            "uom": goal.uom,
            "target_value": goal.target_value,
            "weightage": goal.weightage,
            "status": goal.status,
            "is_shared": goal.is_shared,
            "shared_goal_id": goal.shared_goal_id,
            "primary_owner_id": goal.primary_owner_id,
            "manager_email": manager.email if manager else None
        })

    return response


@router.put("/goals/{goal_id}")
def edit_goal(
    goal_id: int,
    updated_goal: GoalCreate,
    db: Session = Depends(get_db),
    user=Depends(verify_role("employee")),
):

    goal = db.query(Goal).filter(
        Goal.id == goal_id,
        Goal.employee_id == user["user_id"]
    ).first()

    if goal.is_shared:
        goal.weightage = updated_goal.weightage

        db.commit()

        return {
            "message": "Shared goal weightage updated"
        }

    if not goal:

        raise HTTPException(
            status_code=404,
            detail="Goal not found"
        )

    if goal.is_locked:

        raise HTTPException(
            status_code=400,
            detail="Approved goals are locked"
        )

    if goal.status == "submitted":

        raise HTTPException(
            status_code=400,
            detail="Submitted goals cannot be edited"
        )


    old_title = goal.title
    old_description = goal.description
    old_weightage = goal.weightage
    old_target = goal.target_value
    old_uom = goal.uom
    old_manager_id = goal.manager_id

    manager = get_manager_by_email(
        db,
        updated_goal.manager_email
    )
    goal.title = updated_goal.title
    goal.description = updated_goal.description
    goal.thrust_area = updated_goal.thrust_area
    goal.uom = updated_goal.uom
    goal.target_value = updated_goal.target_value
    goal.weightage = updated_goal.weightage
    goal.manager_id = manager.id


    create_audit_log(
        db=db,
        action="Goal Updated",
        performed_by=user["email"],
        entity="Goal",
        role=user.get("role"),

        old_value=f"""
    Title: {old_title}
    Description: {old_description}
    Weightage: {old_weightage}
    Target: {old_target}
    UOM: {old_uom}
    Manager ID: {old_manager_id}
    """,

        new_value=f"""
    Title: {updated_goal.title}
    Description: {updated_goal.description}
    Weightage: {updated_goal.weightage}
    Target: {updated_goal.target_value}
    UOM: {updated_goal.uom}
    Manager ID: {manager.id}
    """,

        details=f"Employee updated goal '{old_title}'"
    )

    db.commit()

    return {
        "message": "Goal updated successfully"
    }
@router.post("/goals/submit")
def submit_goals(
    db: Session = Depends(get_db),
    user=Depends(verify_role("employee")),
):

    employee_id = user["user_id"]

    employee_goals = db.query(Goal).filter(
        Goal.employee_id == employee_id
    ).all()

    if not employee_goals:

        raise HTTPException(
            status_code=400,
            detail="No goals available for submission"
        )

    total_weightage = sum(
        goal.weightage for goal in employee_goals
    )

    if total_weightage != 100:

        raise HTTPException(
            status_code=400,
            detail="Total goal weightage must equal 100 before submission"
        )

    for goal in employee_goals:

        if goal.status == "approved":

            raise HTTPException(
                status_code=400,
                detail="Approved goals cannot be resubmitted"
            )

        goal.status = "submitted"

    create_audit_log(
        db=db,
        action="Goals Submitted",
        performed_by=user["email"],
        role=user.get("role"),
        entity="Goal",
        employee_email=user["email"],
        old_value="draft",
        new_value="submitted",
        details="Employee submitted goals for manager review"
    )

    db.commit()

    return {
        "message": "Goals submitted successfully for manager review"
    }

@router.put("/goals/{goal_id}/resubmit")
def resubmit_goal(
    goal_id: int,
    db: Session = Depends(get_db),
    user=Depends(verify_role("employee")),
):

    goal = db.query(Goal).filter(
        Goal.id == goal_id,
        Goal.employee_id == user["user_id"]
    ).first()

    if not goal:

        raise HTTPException(
            status_code=404,
            detail="Goal not found"
        )

    if goal.status != "rejected":

        raise HTTPException(
            status_code=400,
            detail="Only rejected goals can be resubmitted"
        )

    employee_goals = db.query(Goal).filter(
        Goal.employee_id == user["user_id"]
    ).all()

    total_weightage = sum(
        g.weightage for g in employee_goals
    )

    if total_weightage != 100:

        raise HTTPException(
            status_code=400,
            detail="Total goal weightage must equal 100"
        )

    goal.status = "submitted"

    create_audit_log(
        db=db,
        action="Goal Resubmitted",
        performed_by=user["email"],
        role=user.get("role"),
        entity="Goal",
        entity_id=goal.id,
        employee_email=user["email"],
        old_value="rejected",
        new_value="submitted",
        details=f"""
Employee resubmitted goal '{goal.title}'
"""
    )

    db.commit()

    return {
        "message": "Goal resubmitted successfully"
    }


@router.get("/goals/pending")
def get_pending_goals_for_manager(
    db: Session = Depends(get_db),
    user=Depends(verify_role("manager")),
):
    manager_id = current_user_id(user)

    goals = db.query(Goal).filter(
        Goal.manager_id == manager_id,
        Goal.status == "submitted",
    ).all()

    response = []

    for goal in goals:
        employee = db.query(User).filter(
            User.id == goal.employee_id
        ).first()

        response.append({
            "id": goal.id,
            "title": goal.title,
            "description": goal.description,
            "thrust_area": goal.thrust_area,
            "uom": goal.uom,
            "target_value": goal.target_value,
            "weightage": goal.weightage,
            "status": goal.status,
            "employee_id": goal.employee_id,
            "employee_email": employee.email if employee else None,
            "manager_id": goal.manager_id,
        })

    return response

@router.put("/manager/goals/bulk-update")
def manager_bulk_update_goals(
    updated_data: ManagerBulkGoalUpdate,
    db: Session = Depends(get_db),
    user=Depends(verify_role("manager")),
):

    manager_id = current_user_id(user)

    employee = db.query(User).filter(
        User.id == updated_data.employee_id
    ).first()

    if not employee:

        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    total_weightage = sum(
        item.weightage
        for item in updated_data.goals
    )

    if total_weightage != 100:

        raise HTTPException(
            status_code=400,
            detail="Total goal weightage must equal 100"
        )

    for item in updated_data.goals:

        if item.weightage < 10:

            raise HTTPException(
                status_code=400,
                detail="Minimum weightage is 10"
            )

        goal = db.query(Goal).filter(
            Goal.id == item.goal_id
        ).first()

        if not goal:

            raise HTTPException(
                status_code=404,
                detail=f"Goal {item.goal_id} not found"
            )

        if goal.manager_id != manager_id:

            raise HTTPException(
                status_code=403,
                detail="You are not assigned to this goal"
            )

        if goal.status != "submitted":

            raise HTTPException(
                status_code=400,
                detail="Only submitted goals can be edited"
            )

        old_target = goal.target_value
        old_weightage = goal.weightage

        goal.target_value = item.target_value

        goal.weightage = item.weightage

        create_audit_log(
            db=db,
            action="Manager Updated Goal",
            performed_by=user["email"],
            role=user.get("role"),
            entity="Goal",
            entity_id=goal.id,
            employee_email=employee.email,

            old_value=f"""
Target: {old_target}
Weightage: {old_weightage}
""",

            new_value=f"""
Target: {item.target_value}
Weightage: {item.weightage}
""",

            details=f"""
Manager updated goal '{goal.title}'
before approval
"""
        )

    db.commit()

    return {
        "message": "Goals updated successfully"
    }

@router.put("/goals/{goal_id}/approve")
@router.post("/goals/{goal_id}/approve")
def approve_goal(
    goal_id: int,
    db: Session = Depends(get_db),
    user=Depends(verify_role("manager")),
):
    manager_id = current_user_id(user)

    goal = db.query(Goal).filter(Goal.id == goal_id).first()

    if not goal:
        raise HTTPException(
            status_code=404,
            detail="Goal not found"
        )

    if goal.manager_id is None:
        raise HTTPException(
            status_code=400,
            detail="Goal has no assigned manager. Create a new goal with manager_email."
        )

    if goal.manager_id != manager_id:
        raise HTTPException(
            status_code=403,
            detail="This goal was not assigned to you for approval"
        )

    if goal.status != "submitted":
        raise HTTPException(
            status_code=400,
            detail="Only pending goals can be approved"
        )

    goal.status = "approved"
    goal.is_locked = True
    goal.approved_by = manager_id
    employee = db.query(User).filter(
        User.id == goal.employee_id
    ).first()

    create_audit_log(
        db=db,
        action="Goal Approved",
        performed_by=user["email"],
        role=user.get("role"),
        entity="Goal",
        entity_id=goal.id,
        employee_email=employee.email if employee else None,
        old_value="submitted",
        new_value="approved",
        details=f"Manager approved goal '{goal.title}'"
    )

    db.commit()

    return {
        "message": "Goal approved successfully"
    }


@router.put("/goals/{goal_id}/reject")
@router.post("/goals/{goal_id}/reject")
def reject_goal(
    goal_id: int,
    db: Session = Depends(get_db),
    user=Depends(verify_role("manager")),
):
    manager_id = current_user_id(user)

    goal = db.query(Goal).filter(Goal.id == goal_id).first()

    if not goal:
        raise HTTPException(
            status_code=404,
            detail="Goal not found"
        )

    if goal.manager_id is None:
        raise HTTPException(
            status_code=400,
            detail="Goal has no assigned manager. Create a new goal with manager_email."
        )

    if goal.manager_id != manager_id:
        raise HTTPException(
            status_code=403,
            detail="This goal was not assigned to you for approval"
        )

    if goal.status != "submitted":
        raise HTTPException(
            status_code=400,
            detail="Only pending goals can be rejected"
        )

    goal.status = "rejected"
    goal.is_locked = False
    goal.approved_by = manager_id
    employee = db.query(User).filter(
        User.id == goal.employee_id
    ).first()

    create_audit_log(
        db=db,
        action="Goal Rejected",
        performed_by=user["email"],
        role=user.get("role"),
        entity="Goal",
        entity_id=goal.id,
        employee_email=employee.email if employee else None,
        old_value="submitted",
        new_value="rejected",
        details=f"Manager rejected goal '{goal.title}'"
    )

    db.commit()

    return {
        "message": "Goal rejected successfully"
    }

@router.post("/shared-goals")
def create_shared_goal(
    shared_goal: SharedGoalCreate,
    db: Session = Depends(get_db),
    user=Depends(verify_role("manager"))
):

    shared_goal_id = int(time.time())

    for employee_id in shared_goal.employee_ids:

        employee = db.query(User).filter(
            User.id == employee_id
        ).first()

        if not employee:

            raise HTTPException(
                status_code=404,
                detail=f"Employee {employee_id} not found"
            )

        goal = Goal(

            title=shared_goal.title,

            description=shared_goal.description,

            thrust_area=shared_goal.thrust_area,

            uom=shared_goal.uom,

            target_value=shared_goal.target_value,

            weightage=10,

            employee_id=employee_id,

            manager_id=user["user_id"],

            status="draft",

            is_shared=True,

            shared_goal_id=shared_goal_id,

            primary_owner_id=shared_goal.primary_owner_id
        )

        db.add(goal)

    db.commit()

    return {
        "message": "Shared departmental KPI assigned successfully"
    }


@router.get("/goals")
def get_goals(
    db: Session = Depends(get_db),
    user=Depends(verify_role("admin")),
):

    goals = db.query(Goal).all()

    response = []

    for goal in goals:

        employee = db.query(User).filter(
            User.id == goal.employee_id
        ).first()

        manager = db.query(User).filter(
            User.id == goal.manager_id
        ).first()

        response.append({

            "id": goal.id,
            "title": goal.title,
            "description": goal.description,
            "thrust_area": goal.thrust_area,
            "uom": goal.uom,
            "target_value": goal.target_value,
            "weightage": goal.weightage,
            "status": goal.status,

            "employee_email": (
                employee.email if employee else None
            ),

            "manager_email": (
                manager.email if manager else None
            )
        })

    return response