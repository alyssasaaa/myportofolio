from django.shortcuts import render

from main.forms import ExperienceForm
from main.models import Education, Experience
from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

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
    json_response = get_experiences_json(request)

    deserialized_experiences = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    experiences = [
        item.object
        for item in deserialized_experiences
    ]

    title_query = request.GET.get("title", "").strip()

    university_experiences = [
        experience
        for experience in experiences
        if experience.stage == "university"
    ]
    high_school_experiences = [
        experience
        for experience in experiences
        if experience.stage == "high-school"
    ]
    context = {
        "name": "Alyssa Rahma Adjani",
        "nickname": "Alyssa",
        "university_experience_list": university_experiences,
        "high_school_experience_list": high_school_experiences,
        "title_query": title_query,
    }
    return render(request, "experience.html", context)

def show_education(request):
    context = {
        "name": "Alyssa Rahma Adjani",
        "nickname": "Alyssa",
        "education_list": Education.objects.order_by("-start_year"),
    }
    return render(request, "education.html", context)

def create_experience(request):
    form = ExperienceForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "New experience was successfully added!")
        return redirect("main:show_experience")

    context = {
        "name": "Alyssa Rahma Adjani",
        "nickname": "Alyssa",
        "form": form,
    }

    return render(request, "experience_form.html", context)

def get_experiences_json(request):
    title_query = request.GET.get("title", "").strip()
    experiences = Experience.objects.all()

    if title_query:
        experiences = experiences.filter(title__icontains=title_query)

    experiences_json = serializers.serialize("json", experiences)

    return HttpResponse(experiences_json, content_type="application/json")

def delete_experience(request, experience_id):
    experience = get_object_or_404(
        Experience,
        pk=experience_id,
    )

    if request.method == "POST":
        experience.delete()
        messages.success(
            request,
            "Experience was successfully deleted!",
        )

    return redirect("main:show_experience")