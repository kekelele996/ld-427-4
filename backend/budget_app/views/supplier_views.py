from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from budget_app.models import Supplier
from budget_app.permissions import BudgetRBACPermission
from budget_app.serializers.supplier_serializer import SupplierSerializer
from budget_app.services.supplier_service import SupplierService


class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all().order_by("name")
    serializer_class = SupplierSerializer
    permission_classes = [BudgetRBACPermission]
    filterset_fields = ["category", "status", "rating"]

    @action(detail=True, methods=["post"])
    def status(self, request, pk=None):
        supplier = SupplierService().update_status(
            self.get_object(),
            request.data.get("status"),
            str(request.user.id or "system"),
        )
        return Response(self.get_serializer(supplier).data, status=status.HTTP_200_OK)
