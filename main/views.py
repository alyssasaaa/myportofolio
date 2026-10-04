from django.shortcuts import render

from main.forms import CompetitionForm, ExperienceForm
from main.models import Education, Experience, Competition
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
import datetime
from django.contrib.auth.decorators import login_required  
from django.core.exceptions import PermissionDenied 
from django.views.decorators.http import require_POST


# Create your views here.
def show_main(request):
    last_login = request.COOKIES.get('last_login', 'No active login session / Cookie not found')

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
    title_query = request.GET.get("title", "").strip()
    context = {
        "name": "Alyssa Rahma Adjani",
        "nickname": "Alyssa",
        "title_query": title_query,
        "is_editor": (
                    request.user.is_authenticated 
                    and request.user.groups.filter(name="Editor").exists()
        ),
        "form": ExperienceForm(),
    }
    return render(request, "experience.html", context)

def show_education(request):
    context = {
        "name": "Alyssa Rahma Adjani",
        "nickname": "Alyssa",
        "education_list": Education.objects.order_by("-start_year"),
    }
    return render(request, "education.html", context)

@login_required(login_url="/login/")
def create_experience(request):
    # These two lines are what you add in this step.
    # Check whether the logged-in account is the superuser (admin/you);
    # if it is not, stop the request with a 403.
    if not request.user.is_superuser:
        raise PermissionDenied
    
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

# TUTORIAL 05
def get_experiences_json(request):
    title_query = request.GET.get("title", "").strip()
    experiences = Experience.objects.prefetch_related('starred_by').all()

    if title_query:
        experiences = experiences.filter(title__icontains=title_query)

    # Manually build the JSON data so we can add the Star logic
    data = []
    for experience in experiences:
        starred_users = experience.starred_by.all()
        is_starred = request.user in starred_users if request.user.is_authenticated else False
        starred_by_names = ", ".join([u.username for u in starred_users])

        data.append({
            "pk": str(experience.id),
            "fields": {
                "title": experience.title,
                "description": experience.description,
                "category": experience.category,
                "category_display": experience.get_category_display(),
                "stage": experience.stage,
                "thumbnail": experience.thumbnail,
                "started_at": experience.started_at,
                "ended_at": experience.ended_at,
                "is_ongoing": experience.is_ongoing,
                "star_count": starred_users.count(),
                "is_starred": is_starred,
                "starred_by_names": starred_by_names,
            },
        })
    return JsonResponse(data, safe=False)

@login_required(login_url="/login/")
def delete_experience(request, experience_id):
    # These two lines are what you add in this step.
    # Check whether the logged-in account is the superuser (admin/you);
    # if it is not, stop the request with a 403.
    if not request.user.is_superuser:
        raise PermissionDenied
    
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

@login_required(login_url="/login/")
def create_competition(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    
    form = CompetitionForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "New competition was successfully added!")
        return redirect("main:show_competition")

    context = {
        "name": "Alyssa Rahma Adjani",
        "nickname": "Alyssa",
        "form": form,
    }
    return render(request, "competition_form.html", context)

@login_required(login_url="/login/")
def update_experience(request, experience_id):
    is_editor = request.user.groups.filter(name="Editor").exists()

    if not (request.user.is_superuser or is_editor):
        raise PermissionDenied
    
    experience = get_object_or_404(
        Experience,
        pk=experience_id,
    )

    form = ExperienceForm(
        request.POST if request.method == "POST" else None,
        instance=experience,
    )

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Experience was successfully updated!")
        return redirect("main:show_experience")

    context = {
        "name": "Alyssa Rahma Adjani",
        "nickname": "Alyssa",
        "form": form,
        "is_edit": True,
    }
    return render(request, "experience_form.html", context)

def get_competitions_json(request):
    title_query = request.GET.get("title", "").strip()
    competitions = Competition.objects.prefetch_related('starred_by').all()

    if title_query:
        competitions = competitions.filter(title__icontains=title_query)

    data = []
    for competition in competitions:
        starred_users = competition.starred_by.all()
        is_starred = request.user in starred_users if request.user.is_authenticated else False
        starred_by_names = ", ".join([u.username for u in starred_users])

        data.append({
            "pk": str(competition.id),
            "fields": {
                "title": competition.title,
                "description": competition.description,
                "organizer": competition.organizer,
                "competition_type": competition.competition_type,
                "competition_date": competition.competition_date,
                "achievement": competition.achievement,
                "participation_type": competition.participation_type,
                "created_at": competition.created_at,
                "project_url": competition.project_url,
                "project_image_url": competition.project_image_url,
                "star_count": starred_users.count(),
                "is_starred": is_starred,
                "starred_by_names": starred_by_names,
            }
        })

    return JsonResponse(data, safe=False)

def show_competition(request):
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "Alyssa Rahma Adjani",
        "nickname": "Alyssa",
        "title_query": title_query,
        "is_editor": (
            request.user.is_authenticated 
            and request.user.groups.filter(name="Editor").exists()
        ),
        "form": CompetitionForm(),
    }
    return render(request, "competition.html", context)

@login_required(login_url="/login/")
def delete_competition(request, competition_id):
    if not request.user.is_superuser:
        raise PermissionDenied
    
    competition = get_object_or_404(
        Competition,
        pk=competition_id,
    )

    if request.method == "POST":
        competition.delete()
        messages.success(
            request,
            "Competition was successfully deleted!",
        )

    return redirect("main:show_competition")

@login_required(login_url="/login/")
def update_competition(request, competition_id):
    is_editor = request.user.groups.filter(name="Editor").exists()

    if not (request.user.is_superuser or is_editor):
        raise PermissionDenied
    
    competition = get_object_or_404(
        Competition,
        pk=competition_id,
    )

    form = CompetitionForm(
        request.POST if request.method == "POST" else None,
        instance=competition,
    )

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Competition was successfully updated!")
        return redirect("main:show_competition")

    context = {
        "name": "Alyssa Rahma Adjani",
        "nickname": "Alyssa",
        "form": form,
        "is_edit": True,
    }

    return render(request, "competition_form.html", context)

# ================== TUTORIAL 4 ==================
def register(request):
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Account created successfully. Please log in.")
        return redirect("main:login")
    
    context = {
        "name": "Alyssa Rahma Adjani",
        "nickname": "Alyssa",
        "form": form,
    }
    return render(request, "register.html", context)

def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        return redirect("main:show_main")

    context = {
            "name": "Alyssa Rahma Adjani",
            "nickname": "Alyssa",
            "form": form,
    }
    return render(request, "login.html", context)

def logout_user(request):
    logout(request)
    return redirect("main:show_main")

def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        response = redirect("main:show_main")
        response.set_cookie('last_login', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return response

    context = {
                "name": "Alyssa Rahma Adjani",
                "nickname": "Alyssa",
                "form": form,
    }
    return render(request, "login.html", context)

def logout_user(request):
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie('last_login')
    return response

# No is_superuser check: any logged-in account may give a star
@login_required(login_url="/login/")
def toggle_star(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)

    if request.method == "POST":
        # If this account has already starred it, remove the star.
        # If not, add one.
        if request.user in experience.starred_by.all():
            experience.starred_by.remove(request.user)
        else:
            experience.starred_by.add(request.user)

    return redirect("main:show_experience")

# ================== ASSIGNMENT 4 ==================
# Add login required for the competition section
# No is_superuser check: any logged-in account may give a star
@login_required(login_url="/login/")
def toggle_competitiion_star(request, competition_id):
    competition = get_object_or_404(Competition, pk=competition_id)

    if request.method == "POST":
        # If this account has already starred it, remove the star.
        # If not, add one.
        if request.user in competition.starred_by.all():
            competition.starred_by.remove(request.user)
        else:
            competition.starred_by.add(request.user)

    return redirect("main:show_competition")

# ================== TUTORIAL 5 ==================
@require_POST
def create_experience_ajax(request):
    if not request.user.is_superuser:
        return JsonResponse(
            {"message": "Only the portfolio owner can add experiences."},
            status=403,
        )

    form = ExperienceForm(request.POST)
    if form.is_valid():
        experience = form.save()
        return JsonResponse(
            {"message": "Experience added successfully.", "pk": str(experience.id)},
            status=201,
        )

    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)

# ================== ASSIGNMENT 5 ==================
@require_POST
def create_competition_ajax(request):
    if not request.user.is_superuser:
        return JsonResponse(
            {"message": "Only the portfolio owner can add competitions."},
            status=403,
        )
    
    form = CompetitionForm(request.POST)
    if form.is_valid():
        competition = form.save()
        return JsonResponse(
            {"message": "Competition added successfully.", "pk": str(competition.id)},
            status=201,
        )

    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)