from budget_app.models import AuditLog, Supplier


class SupplierService:
    def update_status(self, supplier: Supplier, status: str, actor_id: str) -> Supplier:
        before = {"status": supplier.status}
        supplier.status = status
        supplier.save(update_fields=["status", "updated_at"])
        AuditLog.objects.create(
            actor_id=actor_id,
            action="supplier.status_update",
            entity_type="Supplier",
            entity_id=str(supplier.id),
            before=before,
            after={"status": supplier.status},
        )
        return supplier
