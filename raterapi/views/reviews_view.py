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
    is_owner = serializers.SerializerMethodField()
    player = ReviewUserSerializer(many=False)

    def get_is_owner(self,obj):
        return self.context["request"].user == obj.player
    class Meta:
        model= GameReview
        fields = ('id', 'review', 'player', 'game_id','is_owner')

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
                pass
                reviews = GameReview.objects.all()
            serializer = ReviewSerializer(reviews,many=True, context = {'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            return HttpResponseServerError(ex)
        
    def destroy(self, request, pk=None):
        try:
            review = GameReview.objects.get(pk=pk)

            if review.player != request.user:
                return Response(status=status.HTTP_403_FORBIDDEN)
            
            review.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except GameReview.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)