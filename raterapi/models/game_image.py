from django.db import models
from .game import Game
from .player import Player

class GameImage(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='game_images/')
