from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from budget_app.filters.expense_filter import ExpenseRecordFilter
from budget_app.models import ExpenseRecord
from budget_app.permissions import BudgetRBACPermission
from budget_app.serializers.expense_serializer import ExpenseRecordSerializer
from budget_app.services.expense_service import ExpenseService


class ExpenseRecordViewSet(viewsets.ModelViewSet):
    queryset = ExpenseRecord.objects.select_related("budget_item", "supplier").all()
    serializer_class = ExpenseRecordSerializer
    permission_classes = [BudgetRBACPermission]
    filterset_class = ExpenseRecordFilter

    @action(detail=True, methods=["post"])
    def submit(self, request, pk=None):
        expense = ExpenseService().submit(self.get_object(), str(request.user.id or "system"))
        return Response(self.get_serializer(expense).data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def approve(self, request, pk=None):
        self.approval_action = True
        expense = ExpenseService().approve(
            self.get_object(),
            str(request.user.id or "system"),
            request.data.get("approval_comment", ""),
        )
        return Response(self.get_serializer(expense).data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def pay(self, request, pk=None):
        self.accounting_action = True
        expense = ExpenseService().pay(self.get_object(), str(request.user.id or "system"))
        return Response(self.get_serializer(expense).data, status=status.HTTP_200_OK)
