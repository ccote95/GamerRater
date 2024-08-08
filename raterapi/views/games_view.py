from raterapi.models import Game, Category
from rest_framework.response import Response
from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.viewsets import ViewSet
import logging
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id','name')

class GameSerializer(serializers.ModelSerializer):
    is_owner = serializers.SerializerMethodField()
    categories = CategorySerializer(many=True)

    def get_is_owner(self,obj):
        return self.context["request"].user == obj.player
    class Meta:
        model = Game
        fields = ('id','title','description','designer','year_released','num_of_players','estimated_play_time','age_recommendation','categories', 'is_owner')




class UpdateGameSerializer(serializers.ModelSerializer):
    is_owner = serializers.SerializerMethodField()
    categories = serializers.PrimaryKeyRelatedField(many=True, queryset=Category.objects.all())

    class Meta:
        model = Game
        fields = ('id','title','description','designer','year_released','num_of_players','estimated_play_time','age_recommendation','categories','is_owner')

class GameView(ViewSet):
    def list(self,request):
        try:   
            games = Game.objects.all()
            serializer = GameSerializer(games, many=True, context = {"request": request})
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

            is_owner = (request.user == game.player) if game.player else False
            game_data = serializer.data
            game_data['is_owner'] = is_owner

            return Response(game_data)
        except Game.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": f"{e}An error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def create(self, request):
        title = request.data.get('title')
        designer = request.data.get('designer')
        year_released = request.data.get('year_released') 
        num_of_players = request.data.get('num_of_players')
        estimated_play_time = request.data.get('estimated_play_time')
        age_recommendation = request.data.get('age_recommendation')

        game = Game.objects.create(
            title = title,
            designer = designer,
            year_released = year_released,
            num_of_players = num_of_players,
            estimated_play_time = estimated_play_time,
            age_recommendation = age_recommendation
        )

        category_ids = request.data.get('categories',[])
        game.categories.set(category_ids)

        serializer = GameSerializer(game, context ={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self,request,pk=None):
        try:
            game = Game.objects.get(pk=pk)

            self.check_object_permissions(request, game)

            serializer = UpdateGameSerializer(game,data=request.data)
            if serializer.is_valid():
                game.title = request.data.get('title')
                game.designer = request.data.get('designer')
                game.year_released = request.data.get('year_released') 
                game.num_of_players = request.data.get('num_of_players')
                game.estimated_play_time = request.data.get('estimated_play_time')
                game.age_recommendation = request.data.get('age_recommendation')
                game.save()

                category_ids = request.data.get('categories', [])
                game.categories.set(category_ids)

                serializer = GameSerializer(game, context={'request': request})
                return Response(None, status.HTTP_204_NO_CONTENT)
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        except Game.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)



