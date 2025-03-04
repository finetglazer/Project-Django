# services/auth_service.py

from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password

import accounts
from accounts.models import UserAccount


class AuthService:
    @staticmethod
    def authenticate_user(username, password):
        try:
            user = UserAccount.objects.get(username=username)
            if check_password(password, user.password):
                return user
            else:
                return None
        except UserAccount.DoesNotExist:
            return None