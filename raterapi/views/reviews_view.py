from rest_framework.viewsets import ViewSet
from rest_framework import serializers, status
from raterapi.models import GameReview
from django.http import HttpResponseServerError
from rest_framework.response import Response
from django.contrib.auth.models import User


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model= GameReview
        fields = ('id', 'review', 'player_id')

class ReviewView(ViewSet):
    def create(self, request):
        review = request.data.get('review')
        game_id = request.data.get('game_id')
        player_id = request.auth.user

        review = GameReview.objects.create(
            review = review,
            game_id = game_id,
            player_id = player_id
        )
        serializer = ReviewSerializer(review, context = {'request': request})
        return Response(serializer.data, status= status.HTTP_201_CREATED)
    
    def list(self, request):
        try:
            reviews = GameReview.objects.all()
            serializer = ReviewSerializer(reviews,many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            return HttpResponseServerError(ex)