from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from budget_app.models import BudgetChangeRequest
from budget_app.permissions import BudgetRBACPermission
from budget_app.serializers.budget_change_serializer import (
    BudgetChangeApproveSerializer,
    BudgetChangeRequestCreateSerializer,
    BudgetChangeRequestSerializer,
)
from budget_app.services.budget_change_service import BudgetChangeService


class BudgetChangeRequestViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BudgetChangeRequest.objects.select_related("budget_sheet").prefetch_related("item_changes").all()
    serializer_class = BudgetChangeRequestSerializer
    permission_classes = [BudgetRBACPermission]
    filterset_fields = ["budget_sheet", "status", "applicant_id"]

    @action(detail=False, methods=["post"])
    def submit(self, request):
        create_ser = BudgetChangeRequestCreateSerializer(data=request.data)
        create_ser.is_valid(raise_exception=True)

        change_request = BudgetChangeService().submit(
            budget_sheet=create_ser.validated_data["budget_sheet"],
            actor_id=str(request.user.id or "system"),
            reason=create_ser.validated_data["reason"],
            item_changes=create_ser.validated_data["item_changes"],
        )
        return Response(
            BudgetChangeRequestSerializer(change_request).data,
            status=status.HTTP_201_CREATED,
        )

    @action(detail=True, methods=["post"])
    def approve(self, request, pk=None):
        self.finance_approval_action = True
        approve_ser = BudgetChangeApproveSerializer(data=request.data)
        approve_ser.is_valid(raise_exception=True)

        change_request = BudgetChangeService().approve(
            change_request=self.get_object(),
            actor_id=str(request.user.id or "system"),
            comment=approve_ser.validated_data.get("approval_comment", ""),
        )
        return Response(BudgetChangeRequestSerializer(change_request).data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def reject(self, request, pk=None):
        self.finance_approval_action = True
        approve_ser = BudgetChangeApproveSerializer(data=request.data)
        approve_ser.is_valid(raise_exception=True)

        change_request = BudgetChangeService().reject(
            change_request=self.get_object(),
            actor_id=str(request.user.id or "system"),
            comment=approve_ser.validated_data.get("approval_comment", ""),
        )
        return Response(BudgetChangeRequestSerializer(change_request).data, status=status.HTTP_200_OK)
