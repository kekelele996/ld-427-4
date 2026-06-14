from rest_framework import serializers

from budget_app.models import Supplier


class SupplierSerializer(serializers.ModelSerializer):
    def validate_rating(self, value: int) -> int:
        if not 1 <= value <= 5:
            raise serializers.ValidationError("供应商评分必须在 1 到 5 之间。")
        return value

    class Meta:
        model = Supplier
        fields = [
            "id",
            "name",
            "category",
            "contact_name",
            "phone",
            "address",
            "bank_name",
            "bank_account",
            "status",
            "rating",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]
