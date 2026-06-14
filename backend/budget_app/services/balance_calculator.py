from decimal import Decimal

from django.db.models import Sum

from budget_app.models import BudgetItem, BudgetSheet, ExpenseRecord, ExpenseStatus


class BalanceCalculator:
    def recalculate_item(self, item: BudgetItem) -> BudgetItem:
        approved_total = (
            ExpenseRecord.objects.filter(budget_item=item, status__in=[ExpenseStatus.APPROVED, ExpenseStatus.PAID])
            .aggregate(total=Sum("amount"))
            .get("total")
            or Decimal("0.00")
        )
        item.spent_amount = approved_total
        item.recalculate_variance()
        item.save(update_fields=["spent_amount", "variance_amount", "updated_at"])
        return item

    def recalculate_sheet(self, sheet: BudgetSheet) -> BudgetSheet:
        spent_total = sheet.items.aggregate(total=Sum("spent_amount")).get("total") or Decimal("0.00")
        frozen_total = (
            ExpenseRecord.objects.filter(budget_item__budget_sheet=sheet, status=ExpenseStatus.SUBMITTED)
            .aggregate(total=Sum("amount"))
            .get("total")
            or Decimal("0.00")
        )
        sheet.spent_amount = spent_total
        sheet.frozen_amount = frozen_total
        sheet.version += 1
        sheet.save(update_fields=["spent_amount", "frozen_amount", "version", "updated_at"])
        return sheet
