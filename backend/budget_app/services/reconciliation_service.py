from django.db import transaction

from budget_app.models import AuditLog, Reconciliation, ReconciliationStatus


class ReconciliationService:
    @transaction.atomic
    def confirm(self, reconciliation: Reconciliation, actor_id: str) -> Reconciliation:
        before = {"status": reconciliation.status}
        reconciliation.status = ReconciliationStatus.CONFIRMED
        reconciliation.confirmed_by_id = actor_id
        reconciliation.save(update_fields=["status", "confirmed_by_id", "unpaid_amount", "updated_at"])
        AuditLog.objects.create(
            actor_id=actor_id,
            action="reconciliation.confirm",
            entity_type="Reconciliation",
            entity_id=str(reconciliation.id),
            before=before,
            after={"status": reconciliation.status},
        )
        return reconciliation
