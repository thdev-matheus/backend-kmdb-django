from django.urls import path

from . import views

urlpatterns = [
    path("movies/", views.MovieViews.as_view()),
    path("movies/<int:movie_id>/", views.MovieParamsViews.as_view()),
]
