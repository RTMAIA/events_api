from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView


urlpatterns = [
    path('api/schema', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/swagger', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/docs/redoc', SpectacularRedocView.as_view(url_name='schema'),name='redoc'),

    path('api/token',TokenObtainPairView.as_view(), name='TokenObtainPair'),
    path('api/refresh', TokenRefreshView.as_view(), name='TokenRefresh'),

    path('api/events', views.ListCreateView.as_view(), name='ListCreate'),
    path('api/events/<int:pk>', views.ListUpdateDeleteView.as_view(), name='ListUpdateDelete'),
    path('api/user/create', views.CreateUser.as_view(), name='CreateUser'),

    path('api/events/<int:pk>/register', views.CreateRegistration.as_view(), name='Registration'),
    path('api/my-registrations', views.ListMyRegistrations.as_view(), name='ListMyResgistrations')

]
