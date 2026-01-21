from rest_framework import serializers
from .models import Movie , WatchHistory , Watchlist



class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'


class WatchHistorySerializer(serializers.ModelSerializer):
    movie = MovieSerializer( read_only=True)
    class Meta:
        model = WatchHistory
        fields = ['user', 'movie', 'watched_at']  

class WatchlistSerializer(serializers.ModelSerializer):
    movie = MovieSerializer( read_only=True)
    class Meta:
        model = Watchlist
        fields = ['user', 'movie', 'added_at']