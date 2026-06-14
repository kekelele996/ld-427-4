import logging

from django.http import JsonResponse


logger = logging.getLogger("budget_app.errors")


class ErrorHandlerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            return self.get_response(request)
        except Exception as exc:
            logger.exception("Unhandled API error")
            return JsonResponse({"detail": "服务器处理请求失败。", "error": exc.__class__.__name__}, status=500)
