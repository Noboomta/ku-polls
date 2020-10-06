"""import."""
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .models import Choice, Question
from django.contrib import messages

class IndexView(generic.ListView):
    """Index view class."""

    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions.
        (not including those set to be published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-end_date')[:5]

def detail_view(request, pk):
    """View for detail."""
    question = Question.objects.get(pk=pk)
    if not (question.can_vote()):
        messages.warning(request, "This question is expired.")
        return redirect('polls:index')
    return render(request, "polls/detail.html", {"question": question})

class ResultsView(generic.DetailView):
    """View for result."""

    model = Question
    template_name = 'polls/results.html'

def vote(request, question_id):
    """View for vote."""
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
