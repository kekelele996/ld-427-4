from rest_framework import serializers

from budget_app.models import ExpenseRecord


class ExpenseRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseRecord
        fields = [
            "id",
            "budget_item",
            "amount",
            "expense_date",
            "payment_method",
            "supplier",
            "invoice_no",
            "description",
            "attachment_url",
            "status",
            "applicant_id",
            "approver_id",
            "approval_comment",
            "paid_at",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["approver_id", "approval_comment", "paid_at", "created_at", "updated_at"]
