from django.shortcuts import render
from rest_framework import generics
from .models import Event, Registration
from .serializers import EventSerializer,RegistrationSerializer, UserSerializer
from .permissions import IsAutheticatedOrReadOnly, IsOwnerUser
from django.contrib.auth.models import User
# Create your views here.

class CreateUser(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ListCreateView(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAutheticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class ListUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsOwnerUser]
