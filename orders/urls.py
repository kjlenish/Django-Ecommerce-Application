from django.urls import path
from .views import place_order, view_orders


urlpatterns = [
    path('checkout/', place_order, name='check_out'),
    path('', view_orders, name='all_orders'),
]