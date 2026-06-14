from decimal import Decimal

from django.db import transaction
from rest_framework.exceptions import ValidationError

from budget_app.models import (
    AuditLog,
    BudgetChangeRequest,
    BudgetChangeRequestItem,
    BudgetChangeStatus,
    BudgetItem,
    BudgetSheet,
    BudgetStatus,
)
from budget_app.services.balance_calculator import BalanceCalculator


class BudgetChangeService:
    def __init__(self) -> None:
        self.calculator = BalanceCalculator()

    @transaction.atomic
    def submit(self, budget_sheet: BudgetSheet, actor_id: str, reason: str, item_changes: list[dict]) -> BudgetChangeRequest:
        if budget_sheet.status != BudgetStatus.ACTIVE:
            raise ValidationError("只有已启用的预算可以提交金额调整申请。")

        total_amount_after = Decimal("0.00")
        change_items = []
        for entry in item_changes:
            item_id = entry["budget_item"]
            requested = Decimal(str(entry["requested_amount"]))
            try:
                budget_item = BudgetItem.objects.get(id=item_id, budget_sheet=budget_sheet)
            except BudgetItem.DoesNotExist:
                raise ValidationError(f"预算项 {item_id} 不属于该预算表。")
            change_items.append((budget_item, requested))
            total_amount_after += requested

        existing_items = BudgetItem.objects.filter(budget_sheet=budget_sheet)
        unchanged_total = Decimal("0.00")
        changed_item_ids = {ci[0].id for ci in change_items}
        for item in existing_items:
            if item.id not in changed_item_ids:
                unchanged_total += item.budget_amount

        total_amount_after += unchanged_total

        change_request = BudgetChangeRequest.objects.create(
            budget_sheet=budget_sheet,
            reason=reason,
            total_amount_before=budget_sheet.total_amount,
            total_amount_after=total_amount_after,
            status=BudgetChangeStatus.PENDING,
            applicant_id=actor_id,
        )

        for budget_item, requested in change_items:
            BudgetChangeRequestItem.objects.create(
                change_request=change_request,
                budget_item=budget_item,
                original_amount=budget_item.budget_amount,
                requested_amount=requested,
            )

        AuditLog.objects.create(
            actor_id=actor_id,
            action="budget_change.submit",
            entity_type="BudgetChangeRequest",
            entity_id=str(change_request.id),
            before={"budget_sheet_id": str(budget_sheet.id), "total_amount_before": str(budget_sheet.total_amount)},
            after={"total_amount_after": str(total_amount_after), "item_count": len(change_items)},
        )

        return change_request

    @transaction.atomic
    def approve(self, change_request: BudgetChangeRequest, actor_id: str, comment: str = "") -> BudgetChangeRequest:
        if change_request.status != BudgetChangeStatus.PENDING:
            raise ValidationError("只有待审批的变更申请可以审批。")

        before = {
            "status": change_request.status,
            "total_amount_before": str(change_request.total_amount_before),
        }

        change_request.status = BudgetChangeStatus.APPROVED
        change_request.approver_id = actor_id
        change_request.approval_comment = comment
        change_request.save(update_fields=["status", "approver_id", "approval_comment", "updated_at"])

        budget_sheet = change_request.budget_sheet
        budget_sheet.total_amount = change_request.total_amount_after
        budget_sheet.version += 1
        budget_sheet.save(update_fields=["total_amount", "version", "updated_at"])

        for item_change in change_request.item_changes.select_related("budget_item"):
            budget_item = item_change.budget_item
            budget_item.budget_amount = item_change.requested_amount
            budget_item.recalculate_variance()
            budget_item.save(update_fields=["budget_amount", "variance_amount", "updated_at"])

        self.calculator.recalculate_sheet(budget_sheet)

        AuditLog.objects.create(
            actor_id=actor_id,
            action="budget_change.approve",
            entity_type="BudgetChangeRequest",
            entity_id=str(change_request.id),
            before=before,
            after={
                "status": change_request.status,
                "total_amount_after": str(change_request.total_amount_after),
                "approver_id": actor_id,
            },
        )

        return change_request

    @transaction.atomic
    def reject(self, change_request: BudgetChangeRequest, actor_id: str, comment: str = "") -> BudgetChangeRequest:
        if change_request.status != BudgetChangeStatus.PENDING:
            raise ValidationError("只有待审批的变更申请可以驳回。")

        change_request.status = BudgetChangeStatus.REJECTED
        change_request.approver_id = actor_id
        change_request.approval_comment = comment
        change_request.save(update_fields=["status", "approver_id", "approval_comment", "updated_at"])

        AuditLog.objects.create(
            actor_id=actor_id,
            action="budget_change.reject",
            entity_type="BudgetChangeRequest",
            entity_id=str(change_request.id),
            before={"status": BudgetChangeStatus.PENDING},
            after={"status": BudgetChangeStatus.REJECTED, "approver_id": actor_id},
        )

        return change_request
