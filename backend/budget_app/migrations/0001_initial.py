# Generated for the renovation budget API sample project.
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="AuditLog",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("actor_id", models.CharField(blank=True, default="", max_length=64)),
                ("action", models.CharField(max_length=80)),
                ("entity_type", models.CharField(max_length=80)),
                ("entity_id", models.CharField(blank=True, default="", max_length=80)),
                ("before", models.JSONField(blank=True, default=dict)),
                ("after", models.JSONField(blank=True, default=dict)),
                ("ip_address", models.GenericIPAddressField(blank=True, null=True)),
            ],
            options={"ordering": ["-created_at"]},
        ),
        migrations.CreateModel(
            name="BudgetSheet",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("project_id", models.CharField(db_index=True, max_length=64)),
                ("name", models.CharField(max_length=120)),
                ("total_amount", models.DecimalField(decimal_places=2, max_digits=14)),
                ("spent_amount", models.DecimalField(decimal_places=2, default="0.00", max_digits=14)),
                ("frozen_amount", models.DecimalField(decimal_places=2, default="0.00", max_digits=14)),
                ("status", models.CharField(choices=[("Draft", "草稿"), ("Active", "启用"), ("Locked", "锁定"), ("Archived", "归档")], default="Draft", max_length=16)),
                ("created_by_id", models.CharField(max_length=64)),
                ("approved_by_id", models.CharField(blank=True, default="", max_length=64)),
                ("version", models.PositiveIntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name="Supplier",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=160)),
                ("category", models.CharField(choices=[("Material", "材料"), ("Furniture", "家具"), ("Appliance", "家电"), ("Labor", "人工"), ("Design", "设计"), ("Other", "其他")], max_length=24)),
                ("contact_name", models.CharField(max_length=80)),
                ("phone", models.CharField(max_length=40)),
                ("address", models.CharField(blank=True, default="", max_length=240)),
                ("bank_name", models.CharField(blank=True, default="", max_length=120)),
                ("bank_account", models.CharField(blank=True, default="", max_length=80)),
                ("status", models.CharField(choices=[("Active", "合作中"), ("Suspended", "暂停"), ("Blacklisted", "黑名单")], default="Active", max_length=24)),
                ("rating", models.PositiveSmallIntegerField(default=5)),
            ],
        ),
        migrations.CreateModel(
            name="UserRole",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("role", models.CharField(choices=[("Admin", "管理员"), ("FinanceManager", "财务经理"), ("ProjectManager", "项目经理"), ("Accountant", "会计"), ("Owner", "业主")], default="Owner", max_length=32)),
                ("user", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="budget_role", to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name="BudgetItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("category", models.CharField(choices=[("Design", "设计"), ("Material", "材料"), ("Labor", "人工"), ("Furniture", "家具"), ("Appliance", "家电"), ("Contingency", "备用金"), ("Other", "其他")], max_length=24)),
                ("subcategory_name", models.CharField(max_length=120)),
                ("budget_amount", models.DecimalField(decimal_places=2, max_digits=14)),
                ("spent_amount", models.DecimalField(decimal_places=2, default="0.00", max_digits=14)),
                ("variance_amount", models.DecimalField(decimal_places=2, default="0.00", max_digits=14)),
                ("sort_order", models.PositiveIntegerField(default=0)),
                ("note", models.TextField(blank=True, default="")),
                ("budget_sheet", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="items", to="budget_app.budgetsheet")),
            ],
            options={"ordering": ["sort_order", "id"]},
        ),
        migrations.CreateModel(
            name="Reconciliation",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("project_id", models.CharField(db_index=True, max_length=64)),
                ("period_month", models.CharField(help_text="YYYY-MM", max_length=7)),
                ("payable_amount", models.DecimalField(decimal_places=2, max_digits=14)),
                ("paid_amount", models.DecimalField(decimal_places=2, default="0.00", max_digits=14)),
                ("unpaid_amount", models.DecimalField(decimal_places=2, default="0.00", max_digits=14)),
                ("status", models.CharField(choices=[("Pending", "待确认"), ("Confirmed", "已确认"), ("Disputed", "有争议"), ("Resolved", "已解决")], default="Pending", max_length=24)),
                ("confirmed_by_id", models.CharField(blank=True, default="", max_length=64)),
                ("supplier", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="reconciliations", to="budget_app.supplier")),
            ],
            options={"unique_together": {("project_id", "period_month", "supplier")}},
        ),
        migrations.CreateModel(
            name="ExpenseRecord",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("amount", models.DecimalField(decimal_places=2, max_digits=14)),
                ("expense_date", models.DateField()),
                ("payment_method", models.CharField(choices=[("Cash", "现金"), ("BankTransfer", "银行转账"), ("Credit", "信用"), ("Company", "公司账户")], max_length=24)),
                ("invoice_no", models.CharField(blank=True, default="", max_length=80)),
                ("description", models.TextField()),
                ("attachment_url", models.URLField(blank=True, default="")),
                ("status", models.CharField(choices=[("Draft", "草稿"), ("Submitted", "已提交"), ("Approved", "已审批"), ("Rejected", "已驳回"), ("Paid", "已付款")], default="Draft", max_length=24)),
                ("applicant_id", models.CharField(max_length=64)),
                ("approver_id", models.CharField(blank=True, default="", max_length=64)),
                ("approval_comment", models.TextField(blank=True, default="")),
                ("paid_at", models.DateField(blank=True, null=True)),
                ("budget_item", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="expenses", to="budget_app.budgetitem")),
                ("supplier", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="expenses", to="budget_app.supplier")),
            ],
            options={"ordering": ["-expense_date", "-id"]},
        ),
    ]
