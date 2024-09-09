from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken

from user.api import serializers


@api_view(['POST'])
def logout(request):

    if request.method == 'POST':
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
def registration(request):

    if request.method == 'POST':
        serializer = serializers.UserSerializer(data=request.data)
        data = {}

        if serializer.is_valid():
            account = serializer.save()
            data['response'] = 'Registration Successful!'
            data['username'] = account.username
            data['email'] = account.email
            # built in auth token
            # token = Token.objects.get(user=account).key
            # token = Token.objects.create(user=account).key
            # data['token'] = token

            # jwt token
            refresh = RefreshToken.for_user(account)
            data['token'] = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }

        else:
            data = serializer.errors

        return Response(data, status=status.HTTP_201_CREATED)
