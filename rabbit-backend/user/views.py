from django.contrib.auth import get_user_model, authenticate, login
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .serializers import UserSerializer

User = get_user_model()


class UserViewSet(ModelViewSet):
    model = User
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_object(self):
        pk = self.kwargs.get('pk', None)
        return User.objects.get(pk=pk)


class Login(APIView):
    def post(self, request, *args, **kwargs):
        data = {
            'username': self.request.data.get('username', None),
            'password': self.request.data.get('password', None),
        }
        user = authenticate(request, **data)
        token, _ = Token.objects.get_or_create(user=user)
        login(request, user)
        return Response({"auth_token": token.key}, status=status.HTTP_200_OK)
