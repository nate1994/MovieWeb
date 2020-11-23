from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('tmdbdata/', views.tmdbdata),
    path('', views.index, name='index'),
    path('<int:pk>/like/', views.like,name = "like")
]