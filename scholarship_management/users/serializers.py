from django.db.models import Q
from rest_framework import serializers
from users import models as user_models

ALLOWED_GENDER = [
    ("MALE", "MALE"),
    ("FEMALE", "FEMALE")
]
