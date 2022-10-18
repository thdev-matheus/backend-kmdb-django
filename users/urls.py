from django.urls import path

from . import views

urlpatterns = [
    path("users/", views.UserViews.as_view()),
    path("users/<int:user_id>/", views.UserParamsViews.as_view()),
    path("users/register/", views.UserCreateView.as_view(), name="register_user"),
    path("users/login/", views.UserLoginView.as_view(), name="login_user"),
]
