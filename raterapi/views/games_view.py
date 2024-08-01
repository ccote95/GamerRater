from raterapi.models import Game
from rest_framework.response import Response
from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.viewsets import ViewSet

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('id','title','description','designer','year_released','num_of_players','estimated_play_time','age_recommendation')

class GameView(ViewSet):
    def list(self,request):
        try:   
            games = Game.objects.all()
            serializer = GameSerializer(games, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            return HttpResponseServerError(ex)