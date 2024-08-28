from django.urls import path, include
from .views import user_login, user_logout, user_details, user_register, user_profile, update_user_profile, update_user_address, update_user_password, search
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('register/', user_register, name='register'),
    path('details/', user_details, name='details'),
    path('search/', search, name='search'),
    path('profile/<str:username>/', user_profile, name='profile'),
    path('profile/<str:username>/update/', update_user_profile, name='update_profile'),
    path('profile/<str:username>/password/', update_user_password, name='update_password'),
    path('profile/<str:username>/address/', update_user_address, name='update_address'),
    
]