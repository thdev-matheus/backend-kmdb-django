from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from . import views

urlpatterns = [
    path("users/", views.UserViews.as_view()),
    path("users/<int:user_id>/", views.UserParamsViews.as_view()),
    path("users/register/", views.UserCreateView.as_view(), name="register_user"),
    path("users/login/", obtain_auth_token, name="login_user"),
]
