from django.shortcuts import render

from main.models import Education, Experience

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
        "name": "Alyssa Rahma Adjani",
        "nickname": "Alyssa",
        "experience_list": Education.objects.all(),
    }
    return render(request, "experience.html", context)

def show_education(request):
    context = {
        "name": "Alyssa Rahma Adjani",
        "nickname": "Alyssa",
        "education_list": Education.objects.order_by("-start_year"),
    }
    return render(request, "education.html", context)