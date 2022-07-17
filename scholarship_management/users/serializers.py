from secrets import choice
from tkinter import ALL
from django.db.models import Q
from rest_framework import serializers
from users import models as user_models

ALLOWED_GENDER = [
    ("MALE", "MALE"),
    ("FEMALE", "FEMALE")
]

class BaseSerializer(serializers.Serializer):
    user_id = serializers.UUIDField(required=True)

class RegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    phone = serializers.CharField(required=True)
    name = serializers.CharField(required=True)
    gender = serializers.ChoiceField(required=True, choices=ALLOWED_GENDER)
    password = serializers.CharField(required=True, trim_whitespace=True)
    confirn_password = serializers.CharField(required=True, trim_whitespace=True)

    def validate(self, obj):
        password=obj['password']
        password2=obj['password2']
        email=obj['email']
        phone=obj['phone']
        qs = user_models.User.objects.filter(Q(username=email) | Q(phone=phone))

        if qs.exists():
            raise serializers.ValidationError("Users with email or phone number exists")
        
        if password != password2:
            raise serializers.ValidationError("Password's do not match")

        return obj
        
