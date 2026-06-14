from rest_framework import serializers

from budget_app.models import BudgetChangeRequest, BudgetChangeRequestItem, BudgetSheet


class BudgetChangeRequestItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BudgetChangeRequestItem
        fields = [
            "id",
            "budget_item",
            "original_amount",
            "requested_amount",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["original_amount", "created_at", "updated_at"]


class BudgetChangeRequestSerializer(serializers.ModelSerializer):
    item_changes = BudgetChangeRequestItemSerializer(many=True, read_only=True)

    class Meta:
        model = BudgetChangeRequest
        fields = [
            "id",
            "budget_sheet",
            "reason",
            "total_amount_before",
            "total_amount_after",
            "status",
            "applicant_id",
            "approver_id",
            "approval_comment",
            "item_changes",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "total_amount_before",
            "total_amount_after",
            "status",
            "approver_id",
            "approval_comment",
            "created_at",
            "updated_at",
        ]


class BudgetChangeRequestCreateSerializer(serializers.Serializer):
    budget_sheet = serializers.PrimaryKeyRelatedField(queryset=BudgetSheet.objects.all())
    reason = serializers.CharField()
    item_changes = serializers.ListField(child=serializers.DictField(), write_only=True)

    def validate_item_changes(self, value):
        if not value:
            raise serializers.ValidationError("至少包含一项预算项调整。")
        for entry in value:
            if "budget_item" not in entry or "requested_amount" not in entry:
                raise serializers.ValidationError("每项调整须包含 budget_item 和 requested_amount。")
        return value


class BudgetChangeApproveSerializer(serializers.Serializer):
    approval_comment = serializers.CharField(required=False, default="")
