from budget_app.models import AuditLog


class AuditLogMiddleware:
    MUTATING_METHODS = {"POST", "PUT", "PATCH", "DELETE"}

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.method in self.MUTATING_METHODS and request.path.startswith("/api/"):
            user = getattr(request, "user", None)
            AuditLog.objects.create(
                actor_id=str(user.id) if getattr(user, "is_authenticated", False) else "",
                action=f"http.{request.method.lower()}",
                entity_type="HttpRequest",
                entity_id=request.path[:80],
                after={"status_code": response.status_code},
                ip_address=self._client_ip(request),
            )
        return response

    def _client_ip(self, request):
        forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
        if forwarded:
            return forwarded.split(",")[0].strip()
        return request.META.get("REMOTE_ADDR")
