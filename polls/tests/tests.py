"""import."""
import datetime
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from .models import Question

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

class QuestionModelTests(TestCase):
    """Main class to testing the Question model."""

    def test_can_vote(self):
        """Test if question can vote.

        Test if the question can vote.

        """
        time_pub = timezone.now() + datetime.timedelta(days=-2)
        time_end = timezone.now() + datetime.timedelta(days=2)
        available_question = Question(pub_date=time_pub, end_date=time_end)
        unavailable_question = Question(pub_date=time_end, end_date=time_pub)
        self.assertIs(available_question.can_vote(), True)
        self.assertIs(unavailable_question.can_vote(), False)

    def test_is_published(self):
        """Test if question is published.

        Test if the question can vote.

        """
        time = timezone.now() + datetime.timedelta(days=-1)
        past_question = Question(pub_date=time)
        self.assertIs(past_question.is_published(), True)

    def test_was_published_recently_with_future_question(self):
        """Test if future question is not published.

        Test if future question is not published.

        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """Test if old question is published.

        Test if old question is published.

        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """Test if recent question is published recently.

        Test if recent question is published recently.

        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

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
