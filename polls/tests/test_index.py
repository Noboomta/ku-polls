import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from ..models import Question


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

class QuestionIndexViewTests(TestCase):
    """Question view testting class."""

    def test_no_questions(self):
        """Test if no questions exist, an appropriate message is displayed.

        Test if no questions exist, an appropriate message is displayed.

        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """Test if no with a pub_date in the past are displayed on the index page.

        Test if no with a pub_date in the past are displayed on the index page.

        """
        create_question(question_text="Past question.", days=-30, days2=-25)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_future_question(self):
        """Test if questions with a pub_date in the future aren't displayed on.the index page.

        Test if questions with a pub_date in the future aren't displayed on.the index page.

        """
        create_question(question_text="Future question.", days=30, days2=-25)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """Test if both past and future questions exist, only past questions are displayed.

        Test if both past and future questions exist, only past questions are displayed.

        """
        create_question(question_text="Past question.", days=-30, days2=-25)
        create_question(question_text="Future question.", days=30, days2=31)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_two_past_questions(self):
        """Test if questions index page may display multiple questions.

        Test if questions index page may display multiple questions.

        """
        create_question(question_text="Past question 1.", days=-30, days2=-25)
        create_question(question_text="Past question 2.", days=-5, days2=0)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )
