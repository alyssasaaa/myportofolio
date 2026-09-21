from django.forms.models import ModelForm
from django.forms.widgets import DateTimeInput, TextInput, Textarea, URLInput, DateInput

from main.models import Competition, Experience

class ExperienceForm(ModelForm):
    class Meta:
        model = Experience
        fields = [
            "title",
            "description",
            "category",
            "stage",
            "thumbnail",
            "ended_at",
        ]

        labels = {
            "title": "Experience Title",
            "description": "Description",
            "category": "Category",
            "stage": "Education Stage",
            "thumbnail": "Thumbnail URL",
            "ended_at": "End Date",
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "COMPFEST 18 | PIC of Decoration",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Describe your role and contribution",
                    "rows": 3,
                }
            ),
            "thumbnail": URLInput(
                attrs={
                    "placeholder": "https://example.com/image.png",
                }
            ),
            "ended_at": DateTimeInput(
                format="%Y-%m-%dT%H:%M",
                attrs={"type": "datetime-local"},
            ),
        }

class CompetitionForm(ModelForm):
    class Meta:
        model = Competition

        fields = [
            "title",
            "organizer",
            "competition_type",
            "description",
            "competition_date",
            "achievement",
            "participation_type",
            "project_url",
            "project_image_url",
        ]

        labels = {
            "title": "Competition Title",
            "organizer": "Organizer",
            "competition_type": "Competition Type",
            "description": "Description",
            "competition_date": "Competition Date",
            "achievement": "Achievement",
            "participation_type": "Participation Type",
            "project_url": "Project URL",
            "project_image_url": "Project Image URL",
        }

        widgets = {
            "title": TextInput(
                attrs={"placeholder": "Enter competition name"}
            ),
            "organizer": TextInput(
                attrs={"placeholder": "Enter organizer name"}
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Describe your contribution",
                    "rows": 3,
                }
            ),
            "competition_date": DateInput(
                format="%Y-%m-%d",
                attrs={"type": "date"},
            ),
            "achievement": TextInput(
                attrs={"placeholder": "Participant, Finalist, 1st Place"}
            ),
            "project_url": URLInput(
                attrs={"placeholder": "https://example.com/project"}
            ),
            "project_image_url": URLInput(
                attrs={"placeholder": "https://example.com/image.png"}
            ),
        }
        