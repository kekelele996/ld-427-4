from rest_framework.permissions import SAFE_METHODS, BasePermission

from budget_app.models import Role


WRITE_ROLES = {Role.ADMIN, Role.FINANCE_MANAGER, Role.PROJECT_MANAGER, Role.ACCOUNTANT}
APPROVAL_ROLES = {Role.ADMIN, Role.FINANCE_MANAGER, Role.PROJECT_MANAGER}


def user_role(user) -> str:
    if not user or not user.is_authenticated:
        return Role.OWNER
    if user.is_superuser:
        return Role.ADMIN
    return getattr(getattr(user, "budget_role", None), "role", Role.OWNER)


class BudgetRBACPermission(BasePermission):
    def has_permission(self, request, view) -> bool:
        role = user_role(request.user)
        if request.method in SAFE_METHODS:
            return True
        if getattr(view, "approval_action", False):
            return role in APPROVAL_ROLES
        if getattr(view, "accounting_action", False):
            return role in {Role.ADMIN, Role.FINANCE_MANAGER, Role.ACCOUNTANT}
        return role in WRITE_ROLES
