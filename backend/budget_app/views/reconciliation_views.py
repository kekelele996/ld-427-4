from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from budget_app.models import Reconciliation
from budget_app.permissions import BudgetRBACPermission
from budget_app.serializers.reconciliation_serializer import ReconciliationSerializer
from budget_app.services.reconciliation_service import ReconciliationService


class ReconciliationViewSet(viewsets.ModelViewSet):
    queryset = Reconciliation.objects.select_related("supplier").all().order_by("-period_month")
    serializer_class = ReconciliationSerializer
    permission_classes = [BudgetRBACPermission]
    filterset_fields = ["project_id", "period_month", "supplier", "status"]

    @action(detail=True, methods=["post"])
    def confirm(self, request, pk=None):
        self.approval_action = True
        reconciliation = ReconciliationService().confirm(self.get_object(), str(request.user.id or "system"))
        return Response(self.get_serializer(reconciliation).data, status=status.HTTP_200_OK)
