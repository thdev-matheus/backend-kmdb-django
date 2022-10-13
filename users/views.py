from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView, Request, Response, status

from .serializers import UserSerializer


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
