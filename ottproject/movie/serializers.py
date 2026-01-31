from rest_framework import serializers
from .models import Movie , WatchHistory , Watchlist



class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'title', 'poster']

class WatchlistSerializer(serializers.ModelSerializer):
    movie = MovieSerializer(read_only=True)
    movie_id = serializers.PrimaryKeyRelatedField(
        queryset=Movie.objects.all(),
        write_only=True,
        source='movie'
    )

    class Meta:
        model = Watchlist
        fields = ['id', 'user', 'movie', 'movie_id', 'added_at']
        read_only_fields = ['id', 'user', 'movie', 'added_at']

    def create(self, validated_data):
        user = self.context['request'].user
        movie = validated_data['movie']
        return Watchlist.objects.create(user=user, movie=movie)


class WatchHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = WatchHistory
        fields = '__all__'