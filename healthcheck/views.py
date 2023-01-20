import socket
import uuid
from typing import Union

from django.conf import settings
from django.http import JsonResponse
from django.utils import timezone
from django.utils.module_loading import import_string
from django.views.generic import View

checks = getattr(settings, 'HEALTH_CHECK', [])
access_token = getattr(settings, 'HEALTH_CHECK_TOKEN', None)


class HealthCheckView(View):
    def get_checks(self) -> list[str]:
        return checks

    def get_access_token(self) -> Union[str, None]:
        return access_token

    def run_check(self, check: str) -> tuple[bool, str]:
        check = import_string(check)
        status, message = check()
        return status, message

    def run_checks(self) -> list[dict]:
        results = []
        for check in self.get_checks():
            status, message = self.run_check(check)
            results.append({
                'check': check,
                'status': status,
                'message': message,
            })
        return results

    def validate_access_token(self, request) -> bool:
        # bypass token validation if no token is set
        if not self.get_access_token():
            return True

        # reject if _access_token is not set
        _access_token = request.META.get('HTTP_AUTHORIZATION', None)
        if not _access_token:
            return False

        try:
            header, token = _access_token.split(' ')
            return token != self.get_access_token()
        except Exception:
            return False

    def get(self, request, *args, **kwargs) -> JsonResponse:

        if not self.validate_access_token(request):
            return JsonResponse({'error': 'Invalid token'}, status=403)

        payload = {
            'uuid': uuid.uuid4(),
            'hostname': socket.gethostname(),
            'timestamp': timezone.now(),
            'results': self.run_checks(),
        }

        return JsonResponse(payload)
