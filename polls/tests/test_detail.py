"""import."""
import datetime
from django.urls import reverse
from django.test import TestCase
from django.utils import timezone
from ..models import Question


def create_question(question_text, pub, end):
    """Create question.

    Function that create the Question.

        Args:
            -question_text- Text of the question to create
            -days- Publish day
            -days2- End day
    Returns:
        A Question.
    """
    time = timezone.now() + datetime.timedelta(days=pub)
    time2 = timezone.now() + datetime.timedelta(days=end)
    return Question.objects.create(question_text=question_text, pub_date=time, end_date=time2)


class QuestionDetailViewTests(TestCase):
    """Test of class detail view."""

    def test_future_question(self):
        """The test of future question."""
        future_question = create_question(question_text='Future question.', pub=3, end=4)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_past_question(self):
        """The test of the past question(already expired)."""
        past_question = create_question(question_text='Past question.', pub=-4, end=-3)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)