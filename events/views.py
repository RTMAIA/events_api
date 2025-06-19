from django.shortcuts import render
from rest_framework import generics
from .models import Event, Registration
from .serializers import EventSerializer,RegistrationSerializer, UserSerializer
from .permissions import IsAutheticatedOrReadOnly, IsOwnerOrReadOnly, IsAdminUser
from django.contrib.auth.models import User
from rest_framework.exceptions import NotAuthenticated, NotFound
# Create your views here.

class CreateUser(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

class ListCreateView(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAutheticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

class ListUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsOwnerOrReadOnly]

class CreateRegistration(generics.CreateAPIView):
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [IsAutheticatedOrReadOnly]

    def perform_create(self, serializer):
        event = Event.objects.get(pk=self.kwargs['pk'])
        serializer.save(user=self.request.user, event=event)

class ListMyRegistrations(generics.ListAPIView):
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        registration = Registration.objects.filter(user_id=self.request.user)
        if not user.is_authenticated:
            raise NotAuthenticated('Você deve estar logado para acessar Minhas Inscrições.')
        if user.is_authenticated and len(registration) == 0:
            raise NotFound('Sem inscrições.')
        return registration

        

       
       
