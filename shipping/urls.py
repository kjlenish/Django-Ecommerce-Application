from django.urls import path
from .views import add_address


urlpatterns = [
    path('new/', add_address, name='add_address'),
]