from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework.test import APITestCase

from polls.models import Question


class PollsApiTests(APITestCase):
    def setUp(self):
        User.objects.create_user("alice", password="secret123")
        self.q = Question.objects.create(question_text="Q?", pub_date=timezone.now())
        self.c1 = self.q.choice_set.create(choice_text="A")
        self.q.choice_set.create(choice_text="B")

    def login(self):
        r = self.client.post("/api/token/", {"username": "alice", "password": "secret123"})
        self.assertEqual(r.status_code, 200)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {r.data['access']}")

    def test_public_list_hides_votes(self):
        r = self.client.get("/api/question/")
        self.assertEqual(r.status_code, 200)
        self.assertNotIn("votes", r.data["results"][0]["choices"][0])

    def test_public_can_vote(self):
        r = self.client.post(f"/api/question/{self.q.id}/vote/", {"choice": self.c1.id})
        self.assertEqual(r.status_code, 200)
        self.c1.refresh_from_db()
        self.assertEqual(self.c1.votes, 1)

    def test_vote_invalid_choice(self):
        r = self.client.post(f"/api/question/{self.q.id}/vote/", {"choice": 9999})
        self.assertEqual(r.status_code, 400)

    def test_public_cannot_access_admin(self):
        self.assertEqual(self.client.get("/api/admin/question/").status_code, 401)
        r = self.client.post("/api/admin/question/", {"question_text": "x", "choices": []}, format="json")
        self.assertEqual(r.status_code, 401)

    def test_auth_sees_votes_and_creates(self):
        self.login()
        r = self.client.get("/api/admin/question/")
        self.assertIn("votes", r.data["results"][0]["choices"][0])
        r = self.client.post(
            "/api/admin/question/",
            {"question_text": "Nouveau", "choices": [{"choice_text": "Oui"}, {"choice_text": "Non"}]},
            format="json",
        )
        self.assertEqual(r.status_code, 201)
        self.assertEqual(Question.objects.get(question_text="Nouveau").choice_set.count(), 2)

    def test_create_needs_two_choices(self):
        self.login()
        r = self.client.post(
            "/api/admin/question/",
            {"question_text": "N", "choices": [{"choice_text": "Seul"}]},
            format="json",
        )
        self.assertEqual(r.status_code, 400)
