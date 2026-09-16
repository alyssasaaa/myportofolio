from django.urls import path

from main.views import delete_experience, get_experiences_json, show_education, show_main, show_experience, create_experience

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("education/", show_education, name="show_education"),
    path("experience/", show_experience, name="show_experience"),
    path("experience/add/", create_experience, name="create_experience"),
    path("api/experiences/", get_experiences_json, name="get_experiences_json"),
    path("experience/<uuid:experience_id>/delete/", delete_experience, name="delete_experience"),
]