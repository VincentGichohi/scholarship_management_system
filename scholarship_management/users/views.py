from webbrowser import get
from django.shortcuts import render
from requests import Response
from rest_framework.views import APIView
from users import serializers as user_serializers, models as user_models
from django.contrib.auth import authenticate
from oauth2_provider.models import get_application_model
from users.utils import oauth2_users
from rest_framework import status

klass = oauth2_users.ApplicationUser()

class RegistationView(APIView):

    def post(self, request):
        serializer = user_serializers.RegistrationSerializer(data=request.data, many=False)

        if not serializer.is_valid():
            return Response({'details': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        email = validated_data['email']
        phone = validated_data['phone']
        gender = validated_data['gender']
        password = validated_data['password']
        name = validated_data['name']

        user = user_models.User.objects.create(
            username=email,
            phone=phone,
            gender=gender,
            name=name
        )
        user.set_password(password)
        user.save()

        klass.create_application_user(user)  #create application user

        return Response({"details": "User created successfully"}, status=status.HTTP_200_OK)

    
class LoginAPIView(APIView):
    
    def post(self, request):
        serializer = user_serializers.LoginSerializer(data=request.data, many=False)

        if not serializer.is_valid():
            return Response({"details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        email = validated_data['email']
        password = validated_data['password']

        user = authenticate(emil=email, password=password)

        if not user:
            return Response({'details': "Invalid email or password"}, status=status.HTTP_400_BAD_REQUEST)
        
        if user.status != "ACTIVE":
            return Response({'details': 'User is {}'.format(user.status.lower())}, status=status.HTTP_400_BAD_REQUEST)

        try:
            instance = get_application_model().objects.get(user=user)
        except get_application_model().DoesNotExist:
            return Response({'details': "Invalid Client"}, status=status.HTTP_400_BAD_REQUEST)

        dt = {
            "grant_type": "password",
            "username": "username",
            "password": "password",
            "client_id": instance.client_id,
            "client_secret": instance.client_secret
        }


        resp = klass.get_client_details(dt)

        if not resp:
            return Response({'details': "Invalid Client credentials"}, status=status.HTTP_400_BAD_REQUEST)

        userInfo = {
            "access_token": resp['access_token'],
            "expires_in": resp["expires_in"],
            "token_type": resp["token_type"],
            "refresh_token": ["refresh_token"],
            "jwt_token": klass.generate_jwt_token(user)
        }
