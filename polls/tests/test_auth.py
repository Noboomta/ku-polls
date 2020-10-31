"""import."""
import datetime
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from polls.models import Question

def create_question(question_text, days, days2):
    """Create question.

    Function that create the Question.

        Args:
            -question_text- Text of the question to create
            -days- Publish day
            -days2- End day
    Returns:
        A Question.
    """
    time = timezone.now() + datetime.timedelta(days=days)
    time2 = timezone.now() + datetime.timedelta(days=days2)
    return Question.objects.create(question_text=question_text, pub_date=time, end_date=time2)

class AuthenticationTests(TestCase):
    """Test of authentication system."""

    def setUp(self):
        User = get_user_model()
        user = User.objects.create_user("Boom", "puva@gmaail.com", "bbbbbbbb")
        user.first_name = 'Boom'
        user.last_name = "Puvana"
        user.save()

    def test_authenticate_user(self):
        """Test if user is logged in."""
        self.client.login(username="Boom", password="12345")
        url = reverse("polls:index")
        response = self.client.get(url)
        self.assertContains(response, "Boom")
        self.assertContains(response, "Puvana")

    def test_unauthenticated_user(self):
        """Test if no logged in user."""
        url = reverse("polls:index")
        response = self.client.get(url)
        self.assertNotContains(response, "Boom")
        self.assertNotContains(response, "Puvana")
