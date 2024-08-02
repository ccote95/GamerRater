from raterapi.models import Game, Category
from rest_framework.response import Response
from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.viewsets import ViewSet
import logging
class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('id','title','description','designer','year_released','num_of_players','estimated_play_time','age_recommendation')

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id','name')

class GameView(ViewSet):
    def list(self,request):
        try:   
            games = Game.objects.all()
            serializer = GameSerializer(games, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            return HttpResponseServerError(ex)
        
    def retrieve(self, request, pk=None):
        try:
            game = Game.objects.get(pk=pk)
            serializer = GameSerializer(game, context={'request': request})

            # Get the categories for the game
            categories = Category.objects.filter(gamecategory__game=game)
            category_serializer = CategorySerializer(categories, many=True, context={'request': request})

            # Add categories to the serialized data
            game_data = serializer.data
            game_data['categories'] = category_serializer.data

            return Response(game_data)
        except Game.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error retrieving game: {str(e)}")
            return Response({"detail": "An error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
