from rest_framework.routers import DefaultRouter

from budget_app.views.budget_views import BudgetSheetViewSet
from budget_app.views.expense_views import ExpenseRecordViewSet
from budget_app.views.item_views import BudgetItemViewSet
from budget_app.views.reconciliation_views import ReconciliationViewSet
from budget_app.views.supplier_views import SupplierViewSet


router = DefaultRouter()
router.register("budgets", BudgetSheetViewSet, basename="budget")
router.register("items", BudgetItemViewSet, basename="budget-item")
router.register("expenses", ExpenseRecordViewSet, basename="expense")
router.register("suppliers", SupplierViewSet, basename="supplier")
router.register("reconciliations", ReconciliationViewSet, basename="reconciliation")

urlpatterns = router.urls
