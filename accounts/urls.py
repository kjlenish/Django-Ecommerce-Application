from django.urls import path
from django.contrib.auth import views as auth_views
from .views import user_login, user_logout, user_details, user_register, user_profile, update_user_profile, update_primary_address, update_user_password


urlpatterns = [
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('register/', user_register, name='register'),
    path('details/', user_details, name='details'),
    path('profile/<str:username>/', user_profile, name='profile'),
    path('profile/<str:username>/update/', update_user_profile, name='update_profile'),
    path('profile/<str:username>/password/', update_user_password, name='update_password'),
    path('profile/<str:username>/address/', update_primary_address, name='update_address'),
    path('password/reset/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'), name='password_reset'),
    path('password/reset/confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password/reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_done'),
    path('password/reset/complete/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name='password_reset_complete'),
]