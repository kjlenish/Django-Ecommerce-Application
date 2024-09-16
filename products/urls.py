from django.urls import path
from .views import home_view, category_view, product_view, product_details, filter_product_view, search


urlpatterns = [
    path('', home_view, name='home'),
    path('search/', search, name='search'),
    path('categories/', category_view, name='categories'),
    path('categories/<str:parent>/', category_view, name='categories'),
    path('products/', product_view, name='products'),
    path('products/filter/<str:sequence>/', filter_product_view, name='filter_products'),
    path('products/<str:parent>/', product_view, name='products'),
    path('product/<int:pk>/', product_details, name='product_detail'),    
]