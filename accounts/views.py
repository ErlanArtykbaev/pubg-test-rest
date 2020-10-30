from django.contrib.auth import get_user_model, logout
from django.utils.translation import gettext as _
from rest_framework import permissions, exceptions, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserMeSerializer, UserSerializer, \
    RegisterSerializer
from .forms import LoginForm, LostPasswordForm, \
    CreateNewPasswordForm, ActivateAccountForm, ResendActivationForm


User = get_user_model()


class LoginView(APIView):
    def post(self, request):
        """
        Login
        ---
            {
            "name": "string",
            "password": "password",
            "phone": "996552887766"
            }
        """
        result = LoginForm(request.data).save()

        if result['status'] == 'error':
            return Response(status=400, data=result['data'])

        user, token = result['data']
        serializer = UserMeSerializer(user, context={'request': request})
        user.save_last_login()

        return Response(serializer.data)


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated, ]

    def post(self, request):
        user = request.user
        try:
            token = Token.objects.get(user=user)
        except Token.DoesNotExist:
            raise exceptions.NotFound(_('User is not signed in'))
        logout(request)
        token.delete()

        return Response({'status': 'success'})


class LostPasswordRequestView(APIView):
    def get(self, request):
        response = LostPasswordForm(request.query_params).save()
        if response['status'] == 'error':
            return Response(status=400, data=response['data'])

        return Response({'status': 'success'})


class CreateNewPasswordView(APIView):
    def post(self, request):
        """
        Create new password
        ---
            {
            "phone": "996552887766",
            "password": "newpassword"
            }
        """
        response = CreateNewPasswordForm(request.data).save()

        if response['status'] == 'error':
            return Response(status=400, data=response['data'])

        user, token = response['data']

        serializer = UserSerializer(user, context={'request': request})

        result = serializer.data
        result['token'] = token
        user.save_last_login()

        return Response(result, status=201)


class ActivateAccountView(APIView):
    def post(self, request):
        result = ActivateAccountForm(request.data).save()

        if result['status'] == 'error':
            return Response(status=400, data=result['data'])

        user = result['data']

        user.backend = 'django.contrib.auth.backends.ModelBackend'
        token = user.get_token()
        serializer = UserSerializer(user, context={'request': request})

        result = serializer.data
        result['token'] = token.key

        return Response(result)


class ResendActivationCodeView(APIView):
    def get(self, request):
        response = ResendActivationForm(request.query_params).save()
        if response['status'] == 'error':
            return Response(status=400, data=response['data'])

        return Response({'status': 'success'})


class RegisterView(APIView):
    def post(self, request):
        """
        Register
        ---
            {
            "name": "string",
            "password": "password",
            "phone": "996552887766"
            }
        """
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            if user:
                return Response({'status': 'success'}, status=status.HTTP_201_CREATED)


class VerifyActivationCodeView(APIView):
    def post(self, request):
        """
        Verify activation code
        ---
            {
                "code": 623451
            }
        """
        result = ActivateAccountForm(request.data).save()

        if result['status'] == 'error':
            return Response(status=400, data=result['data'])

        return Response({'status': 'success'})


class ValidatePassword(APIView):
    def post(self, request):
        """
        Verify activation code
        ---
            {
                "phone": "623451",
                "password": "passpass"
            }
         """
        phone = request.data.get('phone')
        password = request.data.get('password')
        user = User.objects.filter(phone=phone)

        if not user.exists():
            return Response(
                {'status': 'User with this number does not exist'})
        user = user.first()
        if not user.check_password(password):
            return Response(
                {'status': 'password not valid'})

        return Response({'status': 'success'})
