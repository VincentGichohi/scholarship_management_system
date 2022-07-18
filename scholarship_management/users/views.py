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