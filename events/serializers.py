from rest_framework import serializers
from .models import Event, Registration
from django.contrib.auth.models import User


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ['creator']

    def validate(self, data):
        exist_event = Event.objects.filter(title=data['title']).filter(date=data['date']).filter(time=data['time'])
        if len(exist_event) > 0:
            raise serializers.ValidationError('Já existe um evento neste local, data e horario.')
        return super().validate(data)

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = '__all__'
        read_only_fields = ['user', 'event']

    def create(self, validated_data):
        number_regristrations = len(Registration.objects.filter(event_id=validated_data['event'].id))
        event_capacity = Event.objects.get(pk=validated_data['event'].id)
        duplicate_registration = Registration.objects.filter(event_id=validated_data['event'].id).filter(user_id=validated_data['user'].id)
        
        if number_regristrations >= event_capacity.capacity:
            raise serializers.ValidationError('Número de inscrições chegou ao limite maximo.')
        if len(duplicate_registration) >= 1:
            raise serializers.ValidationError('Você já está inscrito neste evento.')
        return super().create(validated_data)
    
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirmation = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'password_confirmation']

    def validate(self, data):
        if data['password'] != data['password_confirmation']:
            raise serializers.ValidationError('As senha não coincidem.')
        return data
    
    def create(self, validated_data):
        validated_data.pop('password_confirmation')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()