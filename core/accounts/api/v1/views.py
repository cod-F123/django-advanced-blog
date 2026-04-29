from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    RegistrationSerializer,
    CustomAuthTokenSerializer,
    CustomTokenObtainPairSerializer,
    ChangePasswordSerializer,
    ProfileSerializer,
    ResendActivationSerializer,
)
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from ...models import Profile
from django.shortcuts import get_object_or_404
from mail_templated import EmailMessage
from ..utils import EmialThreading
from rest_framework_simplejwt.tokens import RefreshToken
import jwt
from jwt.exceptions import InvalidSignatureError, ExpiredSignatureError
from django.conf import settings

User = get_user_model()


class RegistrationApiView(generics.GenericAPIView):
    """Register a new user in the system"""

    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):

        serializer = RegistrationSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            email = serializer.validated_data["email"]

            data = {
                "email": email,
            }

            user = get_object_or_404(User, email=email)

            token = self.get_user_token(user)

            email_obj = EmailMessage(
                "email/activation.tpl",
                {"token": token},
                "from@exp.com",
                [email],
            )

            EmialThreading(email_obj).start()

            return Response(data=data, status=status.HTTP_201_CREATED)

        else:
            return Response(
                data=serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

    def get_user_token(self, user):
        token = RefreshToken.for_user(user)

        return str(token.access_token)


class CustomObtainAuthToken(ObtainAuthToken):

    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):

        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )

        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data.get("user")

        token, created = Token.objects.get_or_create(user=user)

        return Response(
            {"token": token.key, "user_id": user.id, "email": user.email}
        )


class CustomDiscardAuthToken(APIView):

    permission_classes = [
        IsAuthenticated,
    ]

    def post(self, request):
        request.user.auth_token.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class ChangePasswordApiView(generics.GenericAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def put(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():

            old_password = serializer.validated_data.get("old_password")

            user = self.get_object()

            if not user.check_password(old_password):
                return Response(
                    {"detail": "password is wrong !"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            new_password = serializer.validated_data.get("new_password")
            user.set_password(new_password)

            user.save()

            return Response({"detail": "password successfully chenged !"})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileApiView(generics.RetrieveUpdateAPIView):

    serializer_class = ProfileSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    queryset = Profile.objects.all()

    def get_object(self):
        queryset = self.queryset
        user_profile = get_object_or_404(queryset, user=self.request.user)

        return user_profile


class TestSendEmail(APIView):

    def get(self, request):

        self.user_email = "admin1@admin.com"

        user = get_object_or_404(User, email=self.user_email)

        token = self.get_user_token(user)

        email_obj = EmailMessage(
            "email/hello.tpl",
            {"token": token},
            "from@exp.com",
            [self.user_email],
        )

        EmialThreading(email_obj).start()

        return Response("email sended !")

    def get_user_token(self, user):
        token = RefreshToken.for_user(user)

        return str(token.access_token)


class ActivationApiView(APIView):

    def get(self, request, token, *args, **kwargs):

        try:
            token = jwt.decode(
                token, settings.SECRET_KEY, algorithms=["HS256"]
            )
            user_id = token.get("user_id")

        except ExpiredSignatureError:
            return Response(
                {"details": "Token expired !"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        except InvalidSignatureError:
            return Response(
                {"details": "Invalid token !"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = User.objects.get(pk=user_id)

        if user.is_verified:
            return Response(
                {"details": "youre account has already verified !"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.is_verified = True
        user.save()

        return Response({"details": "user verification successfully !"})


class ResendActivationApiView(generics.GenericAPIView):

    serializer_class = ResendActivationSerializer

    def post(self, request, *args, **kwargs):

        serializer = ResendActivationSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]

        token = self.get_user_token(user)

        email_obj = EmailMessage(
            "email/activation.tpl",
            {"token": token},
            "from@exp.com",
            [user.email],
        )

        EmialThreading(email_obj).start()

        return Response(
            {"details": "Activation Email resended seccessfully !"}
        )

    def get_user_token(self, user):
        token = RefreshToken.for_user(user)

        return str(token.access_token)
