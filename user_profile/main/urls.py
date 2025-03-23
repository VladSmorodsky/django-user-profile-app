from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('profile/edit/', views.edit_user_profile_view, name='edit_profile'),
    path('profile/change_password', views.change_password_view, name='change_password'),
    path('profile/<str:username>/', views.profile_view, name='profile_view'),
]
