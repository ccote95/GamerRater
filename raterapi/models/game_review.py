from django.db import models
from .game import Game
from django.contrib.auth.models import User

class GameReview(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    player = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.TextField()
