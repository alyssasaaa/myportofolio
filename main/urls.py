from django.urls import path

from main.views import (
    show_main, show_education,
    create_experience, show_experience, get_experiences_json, delete_experience, update_experience,
    create_competition, show_competition, get_competitions_json, delete_competition, update_competition,
)

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("education/", show_education, name="show_education"),
    path("experience/", show_experience, name="show_experience"),
    path("experience/add/", create_experience, name="create_experience"),
    path("api/experiences/", get_experiences_json, name="get_experiences_json"),
    path("experience/<uuid:experience_id>/delete/", delete_experience, name="delete_experience"),
    path("experience/<uuid:experience_id>/edit/", update_experience, name="update_experience"),
    path("competition/", show_competition, name="show_competition"),
    path("competition/add/", create_competition, name="create_competition"),
    path("api/competitions/", get_competitions_json, name="get_competitions_json"),
    path("competition/<uuid:competition_id>/delete/", delete_competition, name="delete_competition"),
    path("competition/<uuid:competition_id>/edit/", update_competition, name="update_competition"),
]