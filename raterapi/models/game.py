from django.db import models
from django.contrib.auth.models import User

class Game(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    designer = models.CharField(max_length=255)
    year_released = models.DateTimeField()
    num_of_players = models.IntegerField()
    estimated_play_time = models.IntegerField()
    age_recommendation = models.IntegerField()
    player = models.ForeignKey(User, on_delete=models.CASCADE)
    categories = models.ManyToManyField(
        "Category",
        through = 'gameCategory',
        related_name="games"
    )

    def __str__(self):
        return self.title
