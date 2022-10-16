from django.shortcuts import get_object_or_404
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView, Request, Response, status

from users.models import User
from users.permissions import IsAdminOrOwner

from .serializers import UserSerializer


class UserViews(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request: Request) -> Response:
        users = User.objects.all()

        serializer = UserSerializer(users, many=True)

        return Response(serializer.data)


class UserParamsViews(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminOrOwner]

    def get(self, request: Request, user_id: int) -> Response:
        user = get_object_or_404(User, id=user_id)

        self.check_object_permissions(request, user)

        serializer = UserSerializer(user)

        return Response(serializer.data)


class UserCreateView(APIView):
    def post(self, request: Request) -> Response:
        serializer = UserSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserLoginView(ObtainAuthToken):
    def post(self, request: Request) -> Response:
        login_serializer = self.serializer_class(data=request.data)
        login_serializer.is_valid(raise_exception=True)

        user = login_serializer.validated_data["user"]
        user_serializer = UserSerializer(user)

        token, _ = Token.objects.get_or_create(user=user)

        return Response({"token": token.key, "user": user_serializer.data})
