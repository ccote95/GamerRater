from django.db import models
from .game import Game
from .player import Player

class GameRating(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    rating = models.IntegerField()
