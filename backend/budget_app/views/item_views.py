from rest_framework import viewsets

from budget_app.models import BudgetItem
from budget_app.permissions import BudgetRBACPermission
from budget_app.serializers.item_serializer import BudgetItemSerializer


class BudgetItemViewSet(viewsets.ModelViewSet):
    queryset = BudgetItem.objects.select_related("budget_sheet").all()
    serializer_class = BudgetItemSerializer
    permission_classes = [BudgetRBACPermission]
    filterset_fields = ["budget_sheet", "category"]
