import uuid

from django.contrib.auth.models import Group, User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from main.models import Experience, Competition                                                            


class ExperienceAPITest(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_superuser(
            username="owner", password="test-password", email="owner@example.com",
        )
        self.visitor = User.objects.create_user(username="visitor", password="test-password")
        self.experience = Experience.objects.create(
            title="Research Assistant", description="Assisted with university research.",
            category="research", stage="university",
        )
        self.list_url = reverse("api:experience-list")
        self.detail_url = reverse("api:experience-detail", args=[self.experience.id])
        self.star_url = reverse("api:experience-star", args=[self.experience.id])
        self.payload = {
            "title": "New internship", "description": "Worked on a software development team.",
            "category": "internship", "stage": "university",
            "thumbnail": "https://example.com/image.png", "ended_at": None,
        }

    def test_public_list_and_detail(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["id"], str(self.experience.id))
        self.assertFalse(response.data[0]["is_starred"])
        self.assertTrue(response.data[0]["is_ongoing"])
        self.assertEqual(response.data[0]["category"], "research")
        self.assertNotIn("fields", response.data[0])
        self.assertEqual(self.client.get(self.detail_url).status_code, status.HTTP_200_OK)

    def test_search_and_empty_results(self):
        response = self.client.get(self.list_url, {"title": "RESEARCH"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        response = self.client.get(self.list_url, {"title": "not-found"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_missing_experience(self):
        url = reverse("api:experience-detail", args=[uuid.uuid4()])
        self.assertEqual(self.client.get(url).status_code, status.HTTP_404_NOT_FOUND)

    def test_guest_and_visitor_cannot_write(self):
        for user in (None, self.visitor):
            self.client.force_authenticate(user=user)
            self.assertEqual(self.client.post(self.list_url, self.payload, format="json").status_code, 403)
            self.assertEqual(self.client.patch(self.detail_url, {"title": "Changed"}, format="json").status_code, 403)
            self.assertEqual(self.client.delete(self.detail_url).status_code, 403)
        self.assertEqual(Experience.objects.count(), 1)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Research Assistant")

    def test_owner_can_create(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Experience.objects.filter(pk=response.data["id"]).exists())
        self.assertTrue(response.data["is_ongoing"])

    def test_validation(self):
        self.client.force_authenticate(user=self.owner)
        for changes, field in [
            ({"title": "   "}, "title"),
            ({"title": '<img src="x" onerror="alert(1)">'}, "title"),
            ({"description": "<b></b>"}, "description"),
            ({"thumbnail": "javascript:alert(1)"}, "thumbnail"),
            ({"category": "invalid-category"}, "category"),
            ({"stage": "invalid-stage"}, "stage"),
            ({"ended_at": "not-a-date"}, "ended_at"),
        ]:
            with self.subTest(changes=changes):
                response = self.client.post(self.list_url, {**self.payload, **changes}, format="json")
                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
                self.assertIn(field, response.data)
        self.assertEqual(Experience.objects.count(), 1)

    def test_patch_put_and_delete(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.patch(self.detail_url, {"title": "Changed"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Changed")
        self.assertEqual(self.experience.description, "Assisted with university research.")

        response = self.client.put(self.detail_url, {"title": "Incomplete"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.put(
            self.detail_url, {**self.payload, "ended_at": "2026-10-01T12:00:00Z"}, format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data["is_ongoing"])

        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.content, b"")
        self.assertFalse(Experience.objects.filter(pk=self.experience.id).exists())

    def test_star_requires_login_and_toggles(self):
        self.assertEqual(self.client.post(self.star_url).status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.visitor)
        response = self.client.post(self.star_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 1)
        self.assertEqual(response.data["starred_by_names"], "visitor")

        response = self.client.post(self.star_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 0)
        self.assertEqual(response.data["starred_by_names"], "")

    def test_computed_fields_are_read_only(self):
        self.client.force_authenticate(user=self.owner)
        forged_id = uuid.uuid4()
        response = self.client.post(self.list_url, {
            **self.payload,
            "id": str(forged_id), "started_at": "2000-01-01T00:00:00Z",
            "is_ongoing": False, "star_count": 99, "is_starred": True,
            "starred_by_names": "forged", "starred_by": [self.visitor.id],
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(response.data["id"], str(forged_id))
        self.assertTrue(response.data["is_ongoing"])
        self.assertEqual(response.data["star_count"], 0)
        self.assertFalse(response.data["is_starred"])
        self.assertEqual(response.data["starred_by_names"], "")

        created = Experience.objects.get(pk=response.data["id"])
        self.assertNotEqual(created.started_at.year, 2000)
        self.assertEqual(created.starred_by.count(), 0)

    def test_staff_without_editor_role_cannot_update(self):
        self.visitor.is_staff = True
        self.visitor.save()
        self.client.force_authenticate(user=self.visitor)
        response = self.client.patch(self.detail_url, {"title": "Changed"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_editor_can_update_but_cannot_create_or_delete(self):
        editor_group, _ = Group.objects.get_or_create(name="Editor")
        self.visitor.groups.add(editor_group)
        self.client.force_authenticate(user=self.visitor)

        response = self.client.patch(self.detail_url, {"title": "Edited by Editor"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Edited by Editor")

        response = self.client.put(self.detail_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.client.delete(self.detail_url).status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Experience.objects.count(), 1)

    def test_wrong_method(self):
        self.client.force_authenticate(user=self.owner)
        self.assertEqual(self.client.delete(self.list_url).status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(self.client.get(self.star_url).status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_session_write_without_csrf_is_rejected(self):
        client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(client.login(username="owner", password="test-password"))
        response = client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Experience.objects.count(), 1)

    def test_session_write_with_csrf_succeeds(self):
        client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(client.login(username="owner", password="test-password"))
        page = client.get(self.list_url, HTTP_ACCEPT="text/html")
        self.assertEqual(page.status_code, status.HTTP_200_OK)
        token = client.cookies["csrftoken"].value
        response = client.post(
            self.list_url, self.payload, format="json", HTTP_X_CSRFTOKEN=token,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class CompetitionAPITest(APITestCase):
    def setUp(self):
        from main.models import Competition

        self.owner = User.objects.create_superuser(
            username="competition-owner", password="test-password",
            email="competition-owner@example.com",
        )
        self.editor = User.objects.create_user(username="competition-editor", password="test-password")
        self.editor.groups.add(Group.objects.get_or_create(name="Editor")[0])
        self.visitor = User.objects.create_user(username="competition-visitor", password="test-password")
        self.payload = {
            "title": "Campus Hackathon", "organizer": "University",
            "competition_type": "hackathon", "description": "Built a useful app.",
            "competition_date": "2026-11-09", "achievement": "Finalist",
            "participation_type": "group", "project_url": "https://example.com/project",
            "project_image_url": "",
        }
        self.competition = Competition.objects.create(**self.payload)
        self.list_url = reverse("api:competition-list")
        self.detail_url = reverse("api:competition-detail", args=[self.competition.id])
        self.star_url = reverse("api:competition-star", args=[self.competition.id])

    def test_public_search_and_flat_response(self):
        response = self.client.get(self.list_url, {"title": "CAMPUS"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["id"], str(self.competition.id))
        self.assertEqual(response.data[0]["organizer"], "University")
        self.assertNotIn("fields", response.data[0])
        self.assertEqual(self.client.get(self.list_url, {"title": "missing"}).data, [])
        self.assertEqual(self.client.get(self.detail_url).status_code, 200)

    def test_owner_create_patch_and_delete(self):
        self.client.force_authenticate(self.owner)
        response = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, 201)
        detail = reverse("api:competition-detail", args=[response.data["id"]])
        response = self.client.patch(detail, {"achievement": "Winner"}, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["achievement"], "Winner")
        self.assertEqual(response.data["organizer"], self.payload["organizer"])
        response = self.client.delete(detail)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.content, b"")
        self.assertEqual(self.client.get(detail).status_code, 404)

    def test_editor_update_and_role_restrictions(self):
        for user in (None, self.visitor, self.editor):
            with self.subTest(user=user):
                self.client.force_authenticate(user)
                original_count = Competition.objects.count()
                original_data = Competition.objects.values().get(pk=self.competition.pk)

                response = self.client.post(self.list_url, self.payload, format="json")
                self.assertEqual(response.status_code, 403)
                self.assertEqual(Competition.objects.count(), original_count)
                self.assertEqual(Competition.objects.values().get(pk=self.competition.pk), original_data)

                response = self.client.delete(self.detail_url)
                self.assertEqual(response.status_code, 403)
                self.assertEqual(Competition.objects.count(), original_count)
                self.assertEqual(Competition.objects.values().get(pk=self.competition.pk), original_data)

                response = self.client.patch(self.detail_url, {"achievement": "Winner"}, format="json")
                self.competition.refresh_from_db()

                if user == self.editor:
                    self.assertEqual(response.status_code, 200)
                    self.assertEqual(self.competition.achievement, "Winner")
                else:
                    self.assertEqual(response.status_code, 403)
                    self.assertEqual(Competition.objects.values().get(pk=self.competition.pk), original_data)

    def test_invalid_input_and_text_cleaning(self):
        self.client.force_authenticate(self.owner)
        for field, value in [
            ("title", "<b></b>"), ("organizer", "<b></b>"),
            ("description", "<b></b>"), ("achievement", "<b></b>"),
            ("competition_type", "unknown"), ("participation_type", "unknown"),
            ("competition_date", "invalid"), ("project_url", "javascript:alert(1)"),
            ("project_image_url", "invalid"),
        ]:
            with self.subTest(field=field):
                response = self.client.post(self.list_url, {**self.payload, field: value}, format="json")
                self.assertEqual(response.status_code, 400)
                self.assertIn(field, response.data)
        response = self.client.patch(self.detail_url, {"organizer": " <b>Campus</b> "}, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["organizer"], "Campus")

    def test_star_uses_current_account_and_ignores_computed_input(self):
        self.assertEqual(self.client.post(self.star_url).status_code, 403)
        self.client.force_authenticate(self.visitor)
        response = self.client.post(self.star_url, {"starred_by": [self.owner.pk]}, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 1)
        self.assertEqual(response.data["starred_by_names"], self.visitor.username)
        response = self.client.post(self.star_url)
        self.assertFalse(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 0)

    def test_competition_page_supplies_csrf_for_session_ajax(self):
        client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(client.login(username=self.visitor.username, password="test-password"))

        response = client.post(self.star_url, {}, format="json")
        self.assertEqual(response.status_code, 403)
        self.assertEqual(self.competition.starred_by.count(), 0)

        page = client.get(reverse("main:show_competition"))
        self.assertEqual(page.status_code, 200)
        self.assertContains(page, self.list_url)
        self.assertNotContains(page, "item.fields")
        self.assertNotContains(page, 'id="competition-form"')

        response = client.post(
            self.star_url, {}, format="json",
            HTTP_X_CSRFTOKEN=client.cookies["csrftoken"].value,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.competition.starred_by.filter(pk=self.visitor.pk).exists())
        self.assertEqual(self.competition.starred_by.count(), 1)
