import requests
from django.conf import settings
from rest_framework.authentication import SessionAuthentication
from rest_framework.exceptions import APIException


class AccountsUnavailable(APIException):
    status_code = 503
    default_detail = "Сервис accounts недоступен"
    default_code = "accounts_unavailable"


class RemoteUser:
    """Пользователь, данные о котором получены от сервиса accounts."""
    is_authenticated = True
    is_anonymous = False
    is_active = True

    def __init__(self, data):
        self.id = data["id"]
        self.pk = data["id"]
        self.username = data["username"]
        self.is_staff = data["is_staff"]
        self.is_superuser = data["is_superuser"]
        self.second_factor_active = data["second_factor_active"]

    def __str__(self):
        return self.username


class AccountsSessionAuthentication(SessionAuthentication):
    def authenticate(self, request):
        session_id = request.COOKIES.get(settings.SESSION_COOKIE_NAME)
        if not session_id:
            return None

        try:
            response = requests.get(
                f"{settings.ACCOUNTS_URL}/api/users/my/",
                cookies={settings.SESSION_COOKIE_NAME: session_id},
                timeout=3,
            )
            response.raise_for_status()
        except requests.RequestException:
            raise AccountsUnavailable()

        data = response.json()
        if not data.get("is_authenticated"):
            return None

        self.enforce_csrf(request)
        return RemoteUser(data), None