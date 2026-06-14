from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from budget_app.filters.budget_filter import BudgetSheetFilter
from budget_app.models import BudgetSheet
from budget_app.permissions import BudgetRBACPermission
from budget_app.serializers.budget_serializer import BudgetSheetSerializer
from budget_app.services.budget_service import BudgetService


class BudgetSheetViewSet(viewsets.ModelViewSet):
    queryset = BudgetSheet.objects.all().order_by("-updated_at")
    serializer_class = BudgetSheetSerializer
    permission_classes = [BudgetRBACPermission]
    filterset_class = BudgetSheetFilter

    @action(detail=True, methods=["post"])
    def activate(self, request, pk=None):
        self.approval_action = True
        budget = BudgetService().activate_budget(self.get_object(), str(request.user.id or "system"))
        return Response(self.get_serializer(budget).data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def recalculate(self, request, pk=None):
        budget = BudgetService().recalculate(self.get_object(), str(request.user.id or "system"))
        return Response(self.get_serializer(budget).data, status=status.HTTP_200_OK)
