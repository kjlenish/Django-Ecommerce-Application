from django.urls import path
from .views import add_address, manage_addresses,update_address, remove_address


urlpatterns = [
    path('new/', add_address, name='add_address'),
    path('manage/', manage_addresses, name='manage_addresses'),
    path('update/<int:id>/', update_address, name='update_address'),
    path('remove/<int:id>/', remove_address, name='remove_address'),

]