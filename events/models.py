from django.db import models
from django.contrib.auth.models import User


class Event(models.Model):
    title = models.CharField(max_length= 50)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    local = models.CharField(max_length=50)
    capacity = models.IntegerField()
    category = models.IntegerField()
    creator = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.title

class Registration(models.Model):
    user = models.CharField(max_length=15)
    event = models.CharField(max_length=50)
    resgistration_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user
