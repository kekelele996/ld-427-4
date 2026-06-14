from rest_framework import serializers

from budget_app.models import BudgetItem


class BudgetItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BudgetItem
        fields = [
            "id",
            "budget_sheet",
            "category",
            "subcategory_name",
            "budget_amount",
            "spent_amount",
            "variance_amount",
            "sort_order",
            "note",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["spent_amount", "variance_amount", "created_at", "updated_at"]
