from rest_framework.test import APIClient
import pytest
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Event, Registration
from django.contrib.auth.models import User
from django.test.utils import CaptureQueriesContext
from django.db import connection


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
        capacity = 1,
        category = 'tecnologia',
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
    "category": 'tecnologia'}

    response = auth_client.post(url, data, format='json')

    assert response.status_code == 201
    assert response.data['title'] == data['title']
    assert response.data['description'] == data['description']
    assert response.data['date'] == data['date']
    assert response.data['time'] == data['time']
    assert response.data['local'] == data['local']
    assert response.data['capacity'] == data['capacity']
    assert response.data['category'] == data['category']
    assert response.data['creator'] == user.username
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
    "category": 'saude'}

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
    "capacity": 1,
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

@pytest.mark.django_db
def test_create_registration(auth_client, event):
    url = reverse('Registration', kwargs={'pk': event.pk})
    response = auth_client.post(url, format='json')
    registration = Registration.objects.filter(event_id=event.pk)

    assert response.status_code == 201
    assert len(registration) == 1
    assert response.data['registration_date'] == str(registration[0].registration_date)
    assert response.data['event'] == registration[0].event.title
    assert response.data['user'] == registration[0].user.username

@pytest.mark.django_db
def test_event_capacity_limit(auth_client, event):
    api_client = APIClient()
    user_local = User.objects.create_user(username='gabriel', password='gabriel')
    token_local = str(RefreshToken.for_user(user_local).access_token)
    api_client.credentials(HTTP_AUTHORIZATION='Bearer ' + token_local)

    url = reverse('Registration', kwargs={'pk': event.id})
    response = auth_client.post(url, format='json')
    response = api_client.post(url, format='json')
    
    assert response.status_code == 400
    assert response.data[0] == 'Número de inscrições chegou ao limite maximo.'
    
@pytest.mark.django_db
def test_duplicate_user_registration(auth_client, event):
    url = reverse('Registration', kwargs={'pk': event.pk})
    response = auth_client.post(url, format='json')
    response = auth_client.post(url, format='json')

    assert response.status_code == 400
    assert response.data[0] == 'Você já está inscrito neste evento.'

@pytest.mark.django_db
def test_event_filter_category(api_client, event):
    category = 'tecnologia'
    url = reverse('ListCreate') + f'?category={category}'
    response = api_client.get(url, format='json')

    assert response.status_code == 200
    assert response.data['results'][0]['category'] == category

@pytest.mark.django_db
def test_event_filter_category_not_exist(api_client, event):
    category = 'esporte'
    url = reverse('ListCreate') + f'?category={category}'
    response = api_client.get(url, format='json')
    
    assert response.status_code == 204

@pytest.mark.django_db
def test_event_filter_date(api_client, event):
    date = '2025-06-13'
    url = reverse('ListCreate') + f'?date={date}'
    response = api_client.get(url, format='json')

    assert response.status_code == 200
    assert response.data['results'][0]['date'] == date

@pytest.mark.django_db
def test_event_filter_year(api_client, event):
    year = '2025'
    url = reverse('ListCreate') + f'?year={year}'
    response = api_client.get(url, format='json')

    assert response.status_code == 200
    assert response.data['results'][0]['date'][0:4] == year
    
@pytest.mark.django_db
def test_event_filter_year_gte(api_client, event):
    year = '2025'
    url = reverse('ListCreate') + f'?year_gte={year}'
    response = api_client.get(url, format='json')
    
    assert response.status_code == 200
    assert response.data['results'][0]['date'][0:4] == year
    assert len(response.data) > 0

@pytest.mark.django_db
def test_event_filter_year_lte(api_client, event):
    year = '2025'
    url = reverse('ListCreate') + f'?year_lte={year}'
    response = api_client.get(url, format='json')
    
    assert response.status_code == 200
    assert response.data['results'][0]['date'][0:4] == year
    assert len(response.data) > 0

@pytest.mark.django_db
def test_event_filter_month(api_client, event):
    month = '06'
    url = reverse('ListCreate') + f'?month={month}'
    response = api_client.get(url, format='json')
    
    assert response.status_code == 200
    assert response.data['results'][0]['date'][5:7] == month

@pytest.mark.django_db
def test_event_filter_month_gte(api_client, event):
    month = '06'
    url = reverse('ListCreate') + f'?month_gte={month}'
    response = api_client.get(url, format='json')
    
    assert response.status_code == 200
    assert response.data['results'][0]['date'][5:7] == month 
    assert len(response.data) > 0

@pytest.mark.django_db
def test_event_filter_month_lte(api_client, event):
    month = '06'
    url = reverse('ListCreate') + f'?month_lte={month}'
    response = api_client.get(url, format='json')
    
    assert response.status_code == 200
    assert response.data['results'][0]['date'][5:7] == month 
    assert len(response.data) > 0 

@pytest.mark.django_db
def test_event_filter_day(api_client, event):
    day = '13'
    url = reverse('ListCreate') + f'?day={day}'
    response = api_client.get(url, format='json')
   
    assert response.status_code == 200
    assert response.data['results'][0]['date'][8:10] == day
    
@pytest.mark.django_db
def test_event_filter_day_gte(api_client, event):
    day = '13'
    url = reverse('ListCreate') + f'?day_gte={day}'
    response = api_client.get(url, format='json')
   
    assert response.status_code == 200
    assert response.data['results'][0]['date'][8:10] == day
    assert len(response.data) > 0

@pytest.mark.django_db
def test_event_filter_day_lte(api_client, event):
    day = '13'
    url = reverse('ListCreate') + f'?day_lte={day}'
    response = api_client.get(url, format='json')
   
    assert response.status_code == 200
    assert response.data['results'][0]['date'][8:10] == day
    assert len(response.data)

@pytest.mark.django_db
def test_event_filter_date_not_exist(api_client, event):
    date = '2025-06-02'
    url = reverse('ListCreate') + f'?date={date}'
    response = api_client.get(url, format='json')

    assert response.status_code == 204

@pytest.mark.django_db
def test_event_filter_year_not_exist(api_client, event):
    year = '2022'
    url = reverse('ListCreate') + f'?year={year}'
    response = api_client.get(url, format='json')

    assert response.status_code == 204
    
@pytest.mark.django_db
def test_event_filter_year_gte_not_exist(api_client, event):
    year = '2035'
    url = reverse('ListCreate') + f'?year_gte={year}'
    response = api_client.get(url, format='json')
    
    assert response.status_code == 204

@pytest.mark.django_db
def test_event_filter_year_lte_not_exist(api_client, event):
    year = '2000'
    url = reverse('ListCreate') + f'?year_lte={year}'
    response = api_client.get(url, format='json')
    
    assert response.status_code == 204

@pytest.mark.django_db
def test_event_filter_month_not_exist(api_client, event):
    month = '12'
    url = reverse('ListCreate') + f'?month={month}'
    response = api_client.get(url, format='json')
    
    assert response.status_code == 204

@pytest.mark.django_db
def test_event_filter_month_gte_not_exist(api_client, event):
    month = '10'
    url = reverse('ListCreate') + f'?month_gte={month}'
    response = api_client.get(url, format='json')
    
    assert response.status_code == 204

@pytest.mark.django_db
def test_event_filter_month_lte_not_exist(api_client, event):
    month = '02'
    url = reverse('ListCreate') + f'?month_lte={month}'
    response = api_client.get(url, format='json')
    
    assert response.status_code == 204

@pytest.mark.django_db
def test_event_filter_day_not_exist(api_client, event):
    day = '10'
    url = reverse('ListCreate') + f'?day={day}'
    response = api_client.get(url, format='json')
   
    assert response.status_code == 204
    
@pytest.mark.django_db
def test_event_filter_day_gte_not_exist(api_client, event):
    day = '24'
    url = reverse('ListCreate') + f'?day_gte={day}'
    response = api_client.get(url, format='json')
   
    assert response.status_code == 204

@pytest.mark.django_db
def test_event_filter_day_lte_not_exist(api_client, event):
    day = '10'
    url = reverse('ListCreate') + f'?day_lte={day}'
    response = api_client.get(url, format='json')
   
    assert response.status_code == 204

@pytest.mark.django_db
def test_event_queryset_optimized(api_client, event):
    with CaptureQueriesContext(connection) as ctx:
        url = reverse('ListCreate')
        response = api_client.get(url, format='json')
       
        assert response.status_code == 200
