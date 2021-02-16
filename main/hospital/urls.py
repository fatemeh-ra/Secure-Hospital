from django.urls import path
from . import views
 
 
urlpatterns = [
    path('', views.Register, name='accounts' ),
    
    path('addpeaple', views.addpatient, name='add')
    ]