"""import."""
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .models import Choice, Question
from django.contrib import messages
from django.contrib.auth.decorators import login_required

class IndexView(generic.ListView):
    """Index view class."""

    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Get a last five published questions.

        last five published questions.

        Returns:
            the last five published questions.
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-end_date')[:5]

@login_required(login_url='/account/login')
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

# def signup(request):
#     """Register a new user."""
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get('username')
#             raw_passwd = form.cleaned_data.get('password')
#             user = authenticate(username=username,password=raw_passwd)
#             login(request, user)
#             return redirect('polls')
#         # what if form is not valid?
#         # we should display a message in signup.html
#     else:
#         form = UserCreationForm()
#     return render(request, 'registration/signup.html', {'form': form})
