"""import"""
import datetime
from django.contrib.auth.models import User
from django.http import HttpRequest
from importlib import import_module
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

class VotingTests(TestCase):

    def setUp(self):
        User = get_user_model()
        user = User.objects.create_user("Boom", "puva@gmaail.com", "bbbbbbbb")
        user.first_name = 'Boom'
        user.last_name = "Puvana"
        user.save()

    def test_unauthenticate_vote(self):
        """test if unauthenticate user cant vote."""
        question = create_question(question_text='Past Question.', days=-5, days2=5)
        url = reverse('polls:vote', args=(question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_authenticate_vote(self):
        """test if authenticate user can vote."""
        self.client.login(username="Boom", password="bbbbbbbb")
        question = create_question(question_text='Past Question.', days=-5, days2=5)
        url = reverse('polls:vote', args=(question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
