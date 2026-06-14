import django_filters

from budget_app.models import ExpenseRecord


class ExpenseRecordFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(field_name="expense_date", lookup_expr="gte")
    end_date = django_filters.DateFilter(field_name="expense_date", lookup_expr="lte")

    class Meta:
        model = ExpenseRecord
        fields = ["budget_item", "supplier", "status", "payment_method"]
