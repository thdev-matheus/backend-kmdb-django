from django.urls import path

from . import views

urlpatterns = [
    path("register/", views.UserCreateView.as_view(), name="register_user"),
    path("login/", views.UserLoginView.as_view(), name="login_user"),
    path("", views.UserViews.as_view()),
    path("<int:user_id>/", views.UserParamsViews.as_view()),
]
