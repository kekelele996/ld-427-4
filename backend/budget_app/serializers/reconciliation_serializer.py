from rest_framework import serializers

from budget_app.models import Reconciliation


class ReconciliationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reconciliation
        fields = [
            "id",
            "project_id",
            "period_month",
            "supplier",
            "payable_amount",
            "paid_amount",
            "unpaid_amount",
            "status",
            "confirmed_by_id",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["unpaid_amount", "confirmed_by_id", "created_at", "updated_at"]
