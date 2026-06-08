import logging
import time

logger = logging.getLogger('lacrei.access')


class RequestLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()

        response = self.get_response(request)

        duration = time.time() - start_time

        logger.info(
            "Método=%s | Path=%s | Status=%s | IP=%s | Tempo=%.3fs",
            request.method,
            request.get_full_path(),
            response.status_code,
            self._get_client_ip(request),
            duration,
        )

        return response

    @staticmethod
    def _get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR', 'desconhecido')
