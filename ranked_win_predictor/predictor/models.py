from django.db import models
from django.contrib.auth.models import User

class Predict(models.Model):
    summoner = models.CharField(max_length=15)
    predict = models.CharField(max_length=4)
    accuracy = models.FloatField(max_length=4)
    result = models.BooleanField()
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.summoner
# Create your models here.
