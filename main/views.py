from django.shortcuts import render

from main.models import Experience

# Create your views here.
def show_main(request):
    context = {
        "name": "Alyssa Rahma Adjani",
        "nickname": "Alyssa",
        "npm": "2506558466",
        "study_program": "S1 Ilmu Komputer KKI",
        "bio": (
            "A Computer Science student driven by endless curiosity and creativity, always looking"
            "for new things to learn, create, and contribute to."
            "Currently, passionate about exploring UI/UX and Data Science."
        ),
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Burhan",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)