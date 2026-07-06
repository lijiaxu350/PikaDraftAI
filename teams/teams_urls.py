from django.urls import path
from . import views

urlpatterns = [
    path("", views.teams_home, name="teams_home"),
    path("create/", views.create_team, name="create_team"),
    path("<int:team_id>/", views.team_detail, name="team_detail"),
    path("<int:team_id>/slot/<int:slot_index>/choose/", views.choose_pokemon, name="choose_pokemon"),
    path("<int:team_id>/delete/", views.delete_team, name="delete_team"),
    path("<int:team_id>/slot/<int:slot_index>/", views.slot_detail, name="slot_detail"),
]   