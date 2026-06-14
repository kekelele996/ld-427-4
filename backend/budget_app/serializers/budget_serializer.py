from rest_framework import serializers

from budget_app.models import BudgetSheet


class BudgetSheetSerializer(serializers.ModelSerializer):
    available_balance = serializers.DecimalField(max_digits=14, decimal_places=2, read_only=True)

    class Meta:
        model = BudgetSheet
        fields = [
            "id",
            "project_id",
            "name",
            "total_amount",
            "spent_amount",
            "frozen_amount",
            "available_balance",
            "status",
            "created_by_id",
            "approved_by_id",
            "version",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["spent_amount", "frozen_amount", "available_balance", "version", "created_at", "updated_at"]
