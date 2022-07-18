from django.shortcuts import render
from rest_framework.views import APIView
from users import serializers as user_serializers, models as user_models
from django.contrib.auth import authenticate
