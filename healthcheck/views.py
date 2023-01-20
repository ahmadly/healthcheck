import socket
import uuid
from typing import Union

from django.conf import settings
from django.http import JsonResponse
from django.utils import timezone
from django.utils.module_loading import import_string
from django.views.generic import View

__all__ = [
    'HealthCheckView',
]

_access_token = getattr(settings, 'HEALTH_CHECK_TOKEN', None)
_fail_status_code = getattr(settings, 'HEALTH_CHECK_FAIL_STATUS_CODE', 500)
_success_status_code = getattr(settings, 'HEALTH_CHECK_SUCCESS_STATUS_CODE', 200)
_forbidden_status_code = getattr(settings, 'HEALTH_CHECK_FORBIDDEN_STATUS_CODE', 403)
checks = getattr(
    settings,
    'HEALTH_CHECK', [
        'healthcheck.checks.check_database_connection',
        'healthcheck.checks.check_cache_connection',
        'healthcheck.checks.check_internet_connection',
    ]
)


class HealthCheckView(View):
    def get_checks(self) -> list[str]:
        return checks

    def get_access_token(self) -> Union[str, None]:
        return _access_token

    def get_fail_status_code(self) -> int:
        return _fail_status_code

    def get_forbidden_status_code(self) -> int:
        return _forbidden_status_code

    def get_success_status_code(self) -> int:
        return _success_status_code

    def run_check(self, check: str) -> tuple[bool, str]:
        check = import_string(check)
        status, message = check()
        return status, message

    def run_checks(self) -> tuple[list, int, int]:
        results = []
        total_checks = 0
        failed_checks = 0
        for check in self.get_checks():
            status, message = self.run_check(check)
            results.append({
                'check': check,
                'status': status,
                'message': message,
            })
            total_checks += 1
            if not status:
                failed_checks += 1
        return results, total_checks, failed_checks

    def validate_access_token(self, request) -> bool:
        # bypass token validation if no token is set
        if not self.get_access_token():
            return True

        # reject if _access_token is not set
        token = request.META.get('HTTP_AUTHORIZATION', None)
        if not token:
            return False

        try:
            header, token = _access_token.split(' ')
            return token != self.get_access_token()
        except Exception:
            return False

    def get_timestamp(self) -> str:
        return timezone.now().isoformat()

    def get_id(self) -> str:
        return uuid.uuid4().hex

    def get_hostname(self) -> str:
        return socket.gethostname()

    def get(self, request, *args, **kwargs) -> JsonResponse:
        if not self.validate_access_token(request):
            return JsonResponse(
                {'error': 'Invalid token'},
                status=self.get_forbidden_status_code(),
            )

        results, total_checks, failed_checks = self.run_checks()
        payload = {
            'uuid': self.get_id(),
            'timestamp': self.get_timestamp(),
            'hostname': self.get_hostname(),
            'total_checks': total_checks,
            'failed_checks': failed_checks,
            'results': results,
        }
        if failed_checks:
            return JsonResponse(payload, status=self.get_fail_status_code())
        return JsonResponse(payload, status=self.get_success_status_code())
