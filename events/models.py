from django.db import models
from django.contrib.auth.models import User


class Event(models.Model):
    title = models.CharField(max_length= 50)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    local = models.CharField(max_length=50)
    capacity = models.IntegerField()
    category = models.CharField(
        max_length=20,choices=[
                                ('tecnologia', 'Técnologia'),
                                ('educacao', 'Educação'),
                                ('saude', 'Saúde'),
                                ('empreendedorismo', 'Empreendedorismo')])
    creator = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f'{self.creator} | {self.title}'

class Registration(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    event = models.ForeignKey(Event, on_delete=models.DO_NOTHING)
    registration_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} | {self.event.title} | {self.registration_date}'
