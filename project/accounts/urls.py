from django.urls import path
from . import views
 
 
urlpatterns = [
    # path('', views.home, name='accounts' ),
    path('login/', views.login, name = 'login'),
     path('mainpage/', views.loggedin, name = 'loggedin'),
    # path('logout/', views.logout, name = 'logout'),
    # path('signup/', views.signup, name='signup')
    ]