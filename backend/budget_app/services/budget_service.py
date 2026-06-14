from django.db import transaction

from budget_app.models import AuditLog, BudgetItem, BudgetSheet
from budget_app.services.balance_calculator import BalanceCalculator


class BudgetService:
    def __init__(self) -> None:
        self.calculator = BalanceCalculator()

    @transaction.atomic
    def activate_budget(self, budget: BudgetSheet, actor_id: str) -> BudgetSheet:
        before = {"status": budget.status, "version": budget.version}
        budget.status = "Active"
        budget.version += 1
        budget.save(update_fields=["status", "version", "updated_at"])
        AuditLog.objects.create(
            actor_id=actor_id,
            action="budget.activate",
            entity_type="BudgetSheet",
            entity_id=str(budget.id),
            before=before,
            after={"status": budget.status, "version": budget.version},
        )
        return budget

    @transaction.atomic
    def recalculate(self, budget: BudgetSheet, actor_id: str) -> BudgetSheet:
        for item in BudgetItem.objects.filter(budget_sheet=budget):
            self.calculator.recalculate_item(item)
        updated = self.calculator.recalculate_sheet(budget)
        AuditLog.objects.create(
            actor_id=actor_id,
            action="budget.recalculate",
            entity_type="BudgetSheet",
            entity_id=str(updated.id),
            after={"spent_amount": str(updated.spent_amount), "frozen_amount": str(updated.frozen_amount)},
        )
        return updated
