from movies.serializers import MovieSerializer
from rest_framework import serializers
from users.serializers import CriticMovieSerializer

from reviews.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    critic = CriticMovieSerializer(read_only=True)

    class Meta:
        model = Review

        fields = [
            "id",
            "stars",
            "review",
            "spoilers",
            "recomendation",
            "movie_id",
            "critic",
        ]

        read_only_fields = ["movie_id"]
        extra_kwargs = {
            "stars": {
                "min_value": 1,
                "max_value": 10,
            }
        }
