from django.urls import path
from rest_framework.routers import DefaultRouter
from users import views

router = DefaultRouter(trailing_slash=False)

router.register("accounts", views.authentication, basename="accounts")

urlpatterns = [
    path("registration", views.RegistationView.as_view()),
]