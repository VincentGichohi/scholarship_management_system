import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from users.utils.manage import BaseUserManager

ALLOWED_STATUS = [
    ("ACTIVE", "ACTIVE"),
    ("SUSPENDED", "SUSPENDED")
]