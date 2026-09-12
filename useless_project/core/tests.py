import json
from django.test import TestCase, Client
from django.urls import reverse
from .models import Score


class ScoreModelAndAPITests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_score_creation_and_ordering(self):
        """Test that scores are ordered highest seconds_wasted first."""
        s1 = Score.objects.create(username="Player1", seconds_wasted=12.5)
        s2 = Score.objects.create(username="Player2", seconds_wasted=45.2)
        s3 = Score.objects.create(username="Player3", seconds_wasted=5.1)

        scores = list(Score.objects.all())
        self.assertEqual(scores[0].username, "Player2")
        self.assertEqual(scores[1].username, "Player1")
        self.assertEqual(scores[2].username, "Player3")

    def test_leaderboard_api_returns_top_10(self):
        """Test GET /api/leaderboard/ returns at most 10 items."""
        for i in range(15):
            Score.objects.create(username=f"User{i}", seconds_wasted=float(i * 2))

        response = self.client.get(reverse('leaderboard_api'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 10)
        # Verify highest score is first
        self.assertEqual(data[0]['username'], "User14")
        self.assertEqual(data[0]['seconds_wasted'], 28.0)

    def test_submit_api_success(self):
        """Test POST /api/submit/ saves a score correctly."""
        payload = {"username": "ProIdler", "seconds": 33.456}
        response = self.client.post(
            reverse('submit_score_api'),
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Score.objects.count(), 1)
        score = Score.objects.first()
        self.assertEqual(score.username, "ProIdler")
        self.assertEqual(score.seconds_wasted, 33.46)

    def test_submit_api_blank_username_default(self):
        """Test POST /api/submit/ defaults empty username."""
        payload = {"username": "   ", "seconds": 10.0}
        response = self.client.post(
            reverse('submit_score_api'),
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        score = Score.objects.first()
        self.assertEqual(score.username, "Anonymous Idler")

    def test_100_row_cap_enforcement(self):
        """Test that the database never exceeds 100 rows and evicts the lowest score."""
        # Insert 100 scores: values 1.0 to 100.0
        for i in range(1, 101):
            Score.objects.create(username=f"User{i}", seconds_wasted=float(i))

        self.assertEqual(Score.objects.count(), 100)

        # Submit 101st score with a high value (150.0)
        payload = {"username": "HighScorer", "seconds": 150.0}
        response = self.client.post(
            reverse('submit_score_api'),
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Score.objects.count(), 100)

        # The lowest score (User1 with 1.0) should have been deleted
        self.assertFalse(Score.objects.filter(username="User1").exists())
        self.assertTrue(Score.objects.filter(username="HighScorer").exists())
