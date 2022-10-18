from django.shortcuts import get_object_or_404
from KMDB.pagination import CustomPageNumberPagination
from movies.models import Movie
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView, Request, Response, status

from .models import Review
from .permissions import AdminCriticOrOwner, AdminCriticOrReadOnly
from .serializers import ReviewSerializer


class ReviewView(APIView, CustomPageNumberPagination):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AdminCriticOrReadOnly]

    def get(self, request: Request, movie_id: int) -> Response:
        reviews = Review.objects.filter(movie_id=movie_id)

        result_page = self.paginate_queryset(reviews, request, view=self)

        serializer = ReviewSerializer(result_page, many=True)

        return self.get_paginated_response(serializer.data)

    def post(self, request: Request, movie_id: int) -> Response:
        movie = get_object_or_404(Movie, id=movie_id)
        review_already_exists = Review.objects.filter(
            movie_id=movie.id, critic=request.user.id
        ).exists()

        if review_already_exists:
            return Response(
                {"detail": "It is not possible to do two reviews for the same movie."},
                status.HTTP_403_FORBIDDEN,
            )

        serializer = ReviewSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save(movie=movie, critic=request.user)

        return Response(serializer.data, status.HTTP_201_CREATED)


class ReviewParamsView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AdminCriticOrReadOnly, AdminCriticOrOwner]

    def get(self, request: Request, movie_id: int, review_id: int) -> Response:
        review = get_object_or_404(Review, id=review_id, movie_id=movie_id)

        serializer = ReviewSerializer(review)

        return Response(serializer.data)

    def delete(self, request: Request, movie_id: int, review_id: int) -> Response:

        review = get_object_or_404(Review, id=review_id, movie_id=movie_id)

        self.check_object_permissions(request, review.critic)

        review.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
