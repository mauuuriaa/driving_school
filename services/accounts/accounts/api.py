import pyotp
from django.contrib.auth import authenticate, login, logout
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from accounts.models import UserProfile


class UserProfileViewSet(GenericViewSet):
    queryset = UserProfile.objects.all()

    @action(url_path="my", methods=["GET"], detail=False)
    def get_my(self, *args, **kwargs):
        return Response({
            'id': self.request.user.id,
            'username': self.request.user.username,
            'is_authenticated': self.request.user.is_authenticated,
            'is_staff': self.request.user.is_staff,
            'is_superuser': self.request.user.is_superuser,
            'second_factor_active': self.request.session.get('second_factor_active', False)
        })

    @action(url_path="login", methods=["POST"], detail=False)
    def login_user(self, *args, **kwargs):
        class LoginSerializer(serializers.Serializer):
            username = serializers.CharField()
            password = serializers.CharField()

        serializer = LoginSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        user = authenticate(username=username, password=password)

        if user:
            login(self.request, user)
            return Response({"status": "success"})
        else:
            return Response({"status": "failed"}, status=401)

    @action(url_path="logout", methods=["POST"], detail=False)
    def logout_user(self, request, *args, **kwargs):
        logout(request)
        return Response({"status": "success"})

    @action(url_path="get-totp", methods=['GET'], detail=False)
    def get_totp(self, request, *args, **kwargs):
        user_profile = request.user.userprofile

        if not user_profile.totp_key:
            user_profile.totp_key = pyotp.random_base32()
            user_profile.save()

        url = pyotp.totp.TOTP(user_profile.totp_key).provisioning_uri(
            name=request.user.username,
            issuer_name="DrivingSchoolApp"
        )

        return Response({"url": url})

    @action(url_path="second-login", methods=['POST'], detail=False)
    def second_login(self, request, *args, **kwargs):
        key_from_user = request.data.get('key')
        user_profile = request.user.userprofile

        if not user_profile.totp_key:
            return Response({"status": "failed", "detail": "2FA not set up"}, status=400)

        totp = pyotp.totp.TOTP(user_profile.totp_key)

        if totp.verify(key_from_user):
            request.session['second_factor_active'] = True
            return Response({"status": "success"})
        else:
            return Response({"status": "failed", "detail": "Invalid code"}, status=400)