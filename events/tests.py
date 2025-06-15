from rest_framework.test import APIClient
import pytest
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Event
from django.contrib.auth.models import User


@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user():
    return User.objects.create_user(username='rafael', password='rafael')

@pytest.fixture
def event(user):
    return Event.objects.create(
        title = 'titulo de teste',
        description = 'descricao do teste',
        date = '2025-06-13',
        time = '16:37:21',
        local = 'qualquer lugar',
        capacity = 150,
        category = 2,
        creator_id = user.pk)

@pytest.fixture
def auth_client(api_client, user):
    token = str(RefreshToken.for_user(user).access_token)
    api_client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
    return api_client

@pytest.mark.django_db
def test_list_event(auth_client, event):
    url = reverse('ListCreate')
    response = auth_client.get(url, format='json')

    assert response.status_code == 200
    assert len(response.data) >= 1

@pytest.mark.django_db
def test_create_event(auth_client, user):
    url = reverse('ListCreate')
    data = {
    "title": "teste titulo",
    "description": "descricao do teste da criacao",
    "date": "2025-06-13",
    "time": "16:47:21",
    "local": "qualquer lugar ou rua",
    "capacity": 15,
    "category": 4}

    response = auth_client.post(url, data, format='json')

    assert response.status_code == 201
    assert response.data['title'] == data['title']
    assert response.data['description'] == data['description']
    assert response.data['date'] == data['date']
    assert response.data['time'] == data['time']
    assert response.data['local'] == data['local']
    assert response.data['capacity'] == data['capacity']
    assert response.data['category'] == data['category']
    assert response.data['creator'] == user.pk
    assert Event.objects.get(pk=response.data['id'])

@pytest.mark.django_db
def test_update_event(auth_client, event, user):
    url = reverse('ListUpdateDelete', kwargs={'pk': event.pk})
    data = {
    "title": "blablabla teste",
    "description": "descricao do blablbbla teste da criacao",
    "date": "2025-06-13",
    "time": "16:57:21",
    "local": "qualquer lugar ou rua ou cidade",
    "capacity": 5,
    "category": 6}

    response = auth_client.put(url, data, format='json')
    event = Event.objects.get(id=event.pk)

    del response.data['id']
    for key, value in zip(response.data.values(), data.values()):
            assert key == value
    assert response.data['title'] == event.title

@pytest.mark.django_db
def test_delete_event(auth_client, event):
    url = reverse('ListUpdateDelete', kwargs={'pk': event.pk})
    response = auth_client.delete(url)

    assert response.status_code == 204
    assert response.data == None
    assert len(Event.objects.filter(pk=event.pk)) == 0

@pytest.mark.django_db
def test_update_user_not_owner(api_client, event):
    user = User.objects.create_user(username='gabriel', password='gabriel')
    token = str(RefreshToken.for_user(user).access_token)
    api_client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    url = reverse('ListUpdateDelete', kwargs={'pk': event.pk})
    data = {
    "title": "blablabla teste",
    "description": "descricao do blablbbla teste da criacao",
    "date": "2025-06-13",
    "time": "16:57:21",
    "local": "qualquer lugar ou rua ou cidade",
    "capacity": 5,
    "category": 6}

    response = api_client.put(url, data, format='json')
    
    assert response.status_code == 403


@pytest.mark.django_db
def test_create_event_not_authenticated(api_client):
    url = reverse('ListCreate')
    data = {
    "title": "teste titulo",
    "description": "descricao do teste da criacao",
    "date": "2025-06-13",
    "time": "16:47:21",
    "local": "qualquer lugar ou rua",
    "capacity": 15,
    "category": 4}

    response = api_client.post(url, data, format='json')

    assert response.status_code == 401
    


    
    
   
