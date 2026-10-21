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

    def token(self):
        r = self.client.post("/api/token/", {"username": "alice", "password": "secret123"})
        self.assertEqual(r.status_code, 200)
        return r.data["access"]

    def test_public_list_hides_votes(self):
        r = self.client.get("/api/questions/")
        self.assertEqual(r.status_code, 200)
        self.assertNotIn("votes", r.data[0]["choices"][0] if isinstance(r.data, list) else r.data["results"][0]["choices"][0])

    def test_public_can_vote(self):
        r = self.client.post(f"/api/questions/{self.q.id}/vote/", {"choice": self.c1.id})
        self.assertEqual(r.status_code, 200)
        self.c1.refresh_from_db()
        self.assertEqual(self.c1.votes, 1)

    def test_vote_invalid_choice(self):
        r = self.client.post(f"/api/questions/{self.q.id}/vote/", {"choice": 9999})
        self.assertEqual(r.status_code, 400)

    def test_public_cannot_create(self):
        r = self.client.post("/api/questions/", {"question_text": "x", "choices": []}, format="json")
        self.assertEqual(r.status_code, 401)

    def test_auth_sees_votes_and_creates(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token()}")
        r = self.client.get("/api/questions/")
        self.assertIn("votes", r.data[0]["choices"][0])
        r = self.client.post(
            "/api/questions/",
            {"question_text": "Nouveau", "choices": [{"choice_text": "Oui"}, {"choice_text": "Non"}]},
            format="json",
        )
        self.assertEqual(r.status_code, 201)
        self.assertEqual(Question.objects.get(question_text="Nouveau").choice_set.count(), 2)
