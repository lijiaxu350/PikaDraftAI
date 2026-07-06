from django.urls import path
from . import views

urlpatterns = [
    path("", views.coach_home, name="coach_home"),
]