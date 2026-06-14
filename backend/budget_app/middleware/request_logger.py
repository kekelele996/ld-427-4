import logging
import time


logger = logging.getLogger("budget_app.requests")


class RequestLoggerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        started = time.monotonic()
        response = self.get_response(request)
        elapsed_ms = int((time.monotonic() - started) * 1000)
        logger.info("%s %s %s %sms", request.method, request.path, response.status_code, elapsed_ms)
        return response
