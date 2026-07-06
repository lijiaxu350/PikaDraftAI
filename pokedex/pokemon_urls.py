from django.urls import path
from . import views

urlpatterns = [
    path('', views.pokedex_list, name = 'pokedex_list'),
]

