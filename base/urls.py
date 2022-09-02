from django.urls import path
from . import views

urlpatterns = [        
    path('', views.index, name="index"),
    path('user/login/', views.login_user, name='login-user'),
    path('user/logout/', views.logout_user, name='logout-user'),    
    path('user/register/', views.register_user, name='register-user'),    
    path('user/profile/<str:action>/', views.get_user_profile, name='user-profile'),
]