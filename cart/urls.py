from django.urls import path
from . views import CartView, AddToCart


urlpatterns = [
    path('', CartView, name='cart'), 
    path('add/<int:product_id>', AddToCart, name='add_to_cart'),
]