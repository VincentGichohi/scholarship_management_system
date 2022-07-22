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
        serializer = user_serializers.LoginSerializer()