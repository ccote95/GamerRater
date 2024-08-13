from raterapi.models import Game,GameRating
from rest_framework.response import Response
from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.viewsets import ViewSet

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model= GameRating
        fields = ['id','rating','game','player']

class RatingView(ViewSet):
    def create(self, request, game_id):
        game = Game.objects.get(id=game_id)
        serializer = RatingSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(player=request.user, game=game)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)