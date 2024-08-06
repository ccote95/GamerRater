from rest_framework.viewsets import ViewSet
from rest_framework import serializers, status
from raterapi.models import GameReview, Game
from django.http import HttpResponseServerError
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404



class ReviewUserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields = ('first_name', 'last_name')

class ReviewSerializer(serializers.ModelSerializer):
    player = ReviewUserSerializer(many=False)
    class Meta:
        model= GameReview
        fields = ('id', 'review', 'player', 'game_id')

class ReviewView(ViewSet):
    def create(self, request):
        game_id = request.data.get('game_id')

        game_instance = get_object_or_404(Game, id=game_id)
        new_review = GameReview()
        new_review.review = request.data.get('review')
        new_review.game = game_instance
        new_review.player = request.auth.user
        new_review.save()

        # gameReview = GameReview.objects.create(
        #     review = review,
        #     game_id = game_id,
        #     player_id = player_id
        # )
        serializer = ReviewSerializer(new_review, context = {'request': request})
        return Response(serializer.data, status= status.HTTP_201_CREATED)
    
    def list(self, request):
        game = self.request.query_params.get("game", None)
        try:
            if game is not None:
                reviews = GameReview.objects.filter(game_id = game)
            else:
                reviews = GameReview.objects.all()
            serializer = ReviewSerializer(reviews,many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            return HttpResponseServerError(ex)