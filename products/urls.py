from django.urls import path
from .views import HomeView, CategoryView, ProductView, ProductDetails, OrderByProductView


urlpatterns = [
    path('', HomeView, name='home'),
    path('categories/', CategoryView, name='categories'),
    path('categories/<str:parent>/', CategoryView, name='categories'),
    path('products/', ProductView, name='products'),
    path('products/filter/<str:sequence>/', OrderByProductView, name='filter_products'),
    path('products/<str:parent>/', ProductView, name='products'),
    path('product/<int:pk>/', ProductDetails, name='product'),    
]