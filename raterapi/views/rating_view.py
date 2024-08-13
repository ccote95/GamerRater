from raterapi.models import Game,GameRating
from rest_framework.response import Response
from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.viewsets import ViewSet
from django.shortcuts import get_object_or_404

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model= GameRating
        fields = ['id','rating','game','player']

class RatingView(ViewSet):
    def create(self, request):
        game_id = request.data.get('game_id')
        game_instance = get_object_or_404(Game, id=game_id)
        new_rating = GameRating()
        new_rating.rating = request.data.get('rating')
        new_rating.game= game_instance
        new_rating.player = request.auth.user
        new_rating.save()
        serializer = RatingSerializer(new_rating, context = {'request':request})

    
        return Response(serializer.data, status=status.HTTP_201_CREATED)
       