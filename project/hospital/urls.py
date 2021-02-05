from django.urls import path
from . import views
 
 
urlpatterns = [
    path('', views.Register, name='accounts' ),
    
   # path('signup/', views.signup, name='signup')
    ]