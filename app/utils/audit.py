from app.models.auditlog import AuditLog


def create_audit_log(
    db,
    action,
    performed_by,
    entity,
    role=None,
    entity_id=None,
    employee_email=None,
    old_value=None,
    new_value=None,
    details=None,
):

    log = AuditLog(
        action=action,
        performed_by=performed_by,
        role=role,
        entity=entity,
        entity_id=entity_id,
        employee_email=employee_email,
        old_value=old_value,
        new_value=new_value,
        details=details,
    )

    db.add(log)