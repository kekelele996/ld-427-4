from decimal import Decimal

from django.conf import settings
from django.db import models


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Role(models.TextChoices):
    ADMIN = "Admin", "管理员"
    FINANCE_MANAGER = "FinanceManager", "财务经理"
    PROJECT_MANAGER = "ProjectManager", "项目经理"
    ACCOUNTANT = "Accountant", "会计"
    OWNER = "Owner", "业主"


class UserRole(TimestampedModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="budget_role")
    role = models.CharField(max_length=32, choices=Role.choices, default=Role.OWNER)

    def __str__(self) -> str:
        return f"{self.user_id}:{self.role}"


# BudgetSheet entity
class BudgetStatus(models.TextChoices):
    DRAFT = "Draft", "草稿"
    ACTIVE = "Active", "启用"
    LOCKED = "Locked", "锁定"
    ARCHIVED = "Archived", "归档"


class BudgetSheet(TimestampedModel):
    project_id = models.CharField(max_length=64, db_index=True)
    name = models.CharField(max_length=120)
    total_amount = models.DecimalField(max_digits=14, decimal_places=2)
    spent_amount = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"))
    frozen_amount = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"))
    status = models.CharField(max_length=16, choices=BudgetStatus.choices, default=BudgetStatus.DRAFT)
    created_by_id = models.CharField(max_length=64)
    approved_by_id = models.CharField(max_length=64, blank=True, default="")
    version = models.PositiveIntegerField(default=1)

    @property
    def available_balance(self) -> Decimal:
        return self.total_amount - self.spent_amount - self.frozen_amount

    def __str__(self) -> str:
        return f"{self.project_id}:{self.name}"


# BudgetItem entity
class BudgetCategory(models.TextChoices):
    DESIGN = "Design", "设计"
    MATERIAL = "Material", "材料"
    LABOR = "Labor", "人工"
    FURNITURE = "Furniture", "家具"
    APPLIANCE = "Appliance", "家电"
    CONTINGENCY = "Contingency", "备用金"
    OTHER = "Other", "其他"


class BudgetItem(TimestampedModel):
    budget_sheet = models.ForeignKey(BudgetSheet, on_delete=models.CASCADE, related_name="items")
    category = models.CharField(max_length=24, choices=BudgetCategory.choices)
    subcategory_name = models.CharField(max_length=120)
    budget_amount = models.DecimalField(max_digits=14, decimal_places=2)
    spent_amount = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"))
    variance_amount = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"))
    sort_order = models.PositiveIntegerField(default=0)
    note = models.TextField(blank=True, default="")

    class Meta:
        ordering = ["sort_order", "id"]

    def recalculate_variance(self) -> None:
        self.variance_amount = self.budget_amount - self.spent_amount

    def __str__(self) -> str:
        return f"{self.budget_sheet_id}:{self.category}:{self.subcategory_name}"


# Supplier entity
class SupplierCategory(models.TextChoices):
    MATERIAL = "Material", "材料"
    FURNITURE = "Furniture", "家具"
    APPLIANCE = "Appliance", "家电"
    LABOR = "Labor", "人工"
    DESIGN = "Design", "设计"
    OTHER = "Other", "其他"


class SupplierStatus(models.TextChoices):
    ACTIVE = "Active", "合作中"
    SUSPENDED = "Suspended", "暂停"
    BLACKLISTED = "Blacklisted", "黑名单"


class Supplier(TimestampedModel):
    name = models.CharField(max_length=160)
    category = models.CharField(max_length=24, choices=SupplierCategory.choices)
    contact_name = models.CharField(max_length=80)
    phone = models.CharField(max_length=40)
    address = models.CharField(max_length=240, blank=True, default="")
    bank_name = models.CharField(max_length=120, blank=True, default="")
    bank_account = models.CharField(max_length=80, blank=True, default="")
    status = models.CharField(max_length=24, choices=SupplierStatus.choices, default=SupplierStatus.ACTIVE)
    rating = models.PositiveSmallIntegerField(default=5)

    def __str__(self) -> str:
        return self.name


# ExpenseRecord entity
class PaymentMethod(models.TextChoices):
    CASH = "Cash", "现金"
    BANK_TRANSFER = "BankTransfer", "银行转账"
    CREDIT = "Credit", "信用"
    COMPANY = "Company", "公司账户"


class ExpenseStatus(models.TextChoices):
    DRAFT = "Draft", "草稿"
    SUBMITTED = "Submitted", "已提交"
    APPROVED = "Approved", "已审批"
    REJECTED = "Rejected", "已驳回"
    PAID = "Paid", "已付款"


class ExpenseRecord(TimestampedModel):
    budget_item = models.ForeignKey(BudgetItem, on_delete=models.PROTECT, related_name="expenses")
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    expense_date = models.DateField()
    payment_method = models.CharField(max_length=24, choices=PaymentMethod.choices)
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, related_name="expenses")
    invoice_no = models.CharField(max_length=80, blank=True, default="")
    description = models.TextField()
    attachment_url = models.URLField(blank=True, default="")
    status = models.CharField(max_length=24, choices=ExpenseStatus.choices, default=ExpenseStatus.DRAFT)
    applicant_id = models.CharField(max_length=64)
    approver_id = models.CharField(max_length=64, blank=True, default="")
    approval_comment = models.TextField(blank=True, default="")
    paid_at = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ["-expense_date", "-id"]

    def __str__(self) -> str:
        return f"{self.budget_item_id}:{self.amount}:{self.status}"


# Reconciliation entity
class ReconciliationStatus(models.TextChoices):
    PENDING = "Pending", "待确认"
    CONFIRMED = "Confirmed", "已确认"
    DISPUTED = "Disputed", "有争议"
    RESOLVED = "Resolved", "已解决"


class Reconciliation(TimestampedModel):
    project_id = models.CharField(max_length=64, db_index=True)
    period_month = models.CharField(max_length=7, help_text="YYYY-MM")
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, related_name="reconciliations")
    payable_amount = models.DecimalField(max_digits=14, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"))
    unpaid_amount = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"))
    status = models.CharField(max_length=24, choices=ReconciliationStatus.choices, default=ReconciliationStatus.PENDING)
    confirmed_by_id = models.CharField(max_length=64, blank=True, default="")

    class Meta:
        unique_together = [("project_id", "period_month", "supplier")]

    def save(self, *args, **kwargs):
        self.unpaid_amount = self.payable_amount - self.paid_amount
        super().save(*args, **kwargs)


class AuditLog(TimestampedModel):
    actor_id = models.CharField(max_length=64, blank=True, default="")
    action = models.CharField(max_length=80)
    entity_type = models.CharField(max_length=80)
    entity_id = models.CharField(max_length=80, blank=True, default="")
    before = models.JSONField(default=dict, blank=True)
    after = models.JSONField(default=dict, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
