from app.models.auditlog import AuditLog

def create_audit_log(
    db,
    action,
    performed_by,
    entity
):

    log = AuditLog(
        action=action,
        performed_by=performed_by,
        entity=entity
    )

    db.add(log)
    db.commit()