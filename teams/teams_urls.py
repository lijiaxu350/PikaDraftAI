from django.urls import path
from . import views

urlpatterns = [
    path("", views.teams_home, name="teams_home"),
    path("create/", views.create_team, name="create_team"),
    path("<str:team_name>/", views.team_detail, name="team_detail"),
    path("<str:team_name>/slot/<int:slot_index>/choose/", views.choose_pokemon, name="choose_pokemon"),
    path("<str:team_name>/delete/", views.delete_team, name="delete_team"),
    path("<str:team_name>/slot/<int:slot_index>/", views.slot_detail, name="slot_detail"),
]   