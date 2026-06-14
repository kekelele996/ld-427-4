from django.contrib import admin

from budget_app.models import AuditLog, BudgetItem, BudgetSheet, ExpenseRecord, Reconciliation, Supplier, UserRole


@admin.register(BudgetSheet)
class BudgetSheetAdmin(admin.ModelAdmin):
    list_display = ("id", "project_id", "name", "total_amount", "spent_amount", "frozen_amount", "status", "version")
    list_filter = ("status", "project_id")
    search_fields = ("name", "project_id")


@admin.register(BudgetItem)
class BudgetItemAdmin(admin.ModelAdmin):
    list_display = ("id", "budget_sheet", "category", "subcategory_name", "budget_amount", "spent_amount")
    list_filter = ("category",)


@admin.register(ExpenseRecord)
class ExpenseRecordAdmin(admin.ModelAdmin):
    list_display = ("id", "budget_item", "amount", "expense_date", "supplier", "status")
    list_filter = ("status", "payment_method")


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "category", "status", "rating", "contact_name", "phone")
    list_filter = ("category", "status", "rating")


@admin.register(Reconciliation)
class ReconciliationAdmin(admin.ModelAdmin):
    list_display = ("id", "project_id", "period_month", "supplier", "payable_amount", "paid_amount", "status")
    list_filter = ("status", "period_month")


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ("id", "actor_id", "action", "entity_type", "entity_id", "created_at")
    list_filter = ("action", "entity_type")


admin.site.register(UserRole)
