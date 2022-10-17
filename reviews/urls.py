from django.urls import path

from . import views

urlpatterns = [
    path(
        "<int:movie_id>/reviews/",
        views.ReviewView.as_view(),
    ),
    path(
        "<int:movie_id>/reviews/<int:review_id>/",
        views.ReviewParamsView.as_view(),
    ),
]
