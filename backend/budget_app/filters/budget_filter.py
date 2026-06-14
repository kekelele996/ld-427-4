import django_filters

from budget_app.models import BudgetSheet


class BudgetSheetFilter(django_filters.FilterSet):
    min_total = django_filters.NumberFilter(field_name="total_amount", lookup_expr="gte")
    max_total = django_filters.NumberFilter(field_name="total_amount", lookup_expr="lte")

    class Meta:
        model = BudgetSheet
        fields = ["project_id", "status", "created_by_id", "approved_by_id"]
