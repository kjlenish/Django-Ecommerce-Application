from django.urls import path
from .views import place_order, view_orders, order_details, order_summary


urlpatterns = [
    path('', view_orders, name='all_orders'),
    path('checkout/', place_order, name='check_out'),
    path('details/<int:pk>/', order_details, name='order_detail'),
    path('summary/<int:order_id>/', order_summary, name='order_summary'),
]