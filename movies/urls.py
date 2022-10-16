from django.urls import path

from . import views

urlpatterns = [
    path("", views.MovieViews.as_view()),
    path("<int:movie_id>/", views.MovieParamsViews.as_view()),
]
