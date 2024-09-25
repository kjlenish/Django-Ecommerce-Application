from django.urls import path
from .views import cart_view, add_to_cart, update_cart


urlpatterns = [
    path('', cart_view, name='cart'), 
    path('add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('update/', update_cart, name='update_cart'),
]