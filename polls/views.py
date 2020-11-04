"""import."""
from django.views import generic
from django.utils import timezone
from datetime import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from .models import Question, Choice, Vote
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

import logging

log = logging.getLogger("polls")
logging.basicConfig(level=logging.INFO)

def get_client_ip(request):
    """Get the client's ip address."""

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

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
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')

@receiver(user_logged_in)
def update_choice_login(request, **kwargs):
    """Update your last vote when login."""
    for question in Question.objects.all():
        try:
            question.last_vote = str(request.user.vote_set.get(question=question).selected_choice)
            question.save()
        except(Vote.DoesNotExist):
            pass
        
@receiver(user_logged_in)
def log_user_logged_in(sender, request, user, **kwargs):
    """Log when user login."""

    ip = get_client_ip(request)
    date = datetime.now()
    log.info('Login user: %s , IP: %s , Date: %s', user, ip, str(date))

@receiver(user_logged_out)
def log_user_logged_out(sender, request, user, **kwargs):
    """Log when user logout."""

    ip = get_client_ip(request)
    date = datetime.now()
    log.info('Logout user: %s , IP: %s , Date: %s', user, ip, str(date))

@receiver(user_login_failed)
def log_user_login_failed(sender, request, credentials, **kwargs):
    """Log when fail to login."""

    ip = get_client_ip(request)
    date = datetime.now()
    log.warning('Login user(failed): %s , IP: %s , Date: %s', credentials['username'], ip, str(date))

class DetailView(LoginRequiredMixin,generic.DetailView):
    """View for detail page."""

    model = Question
    template_name = 'polls/detail.html'

    def get(self, request, *args, **kwargs):
        """
        If question does not exist or can't be vote, redirect to index page.
        """
        try:
            question = Question.objects.get(pk=kwargs['pk'])
            if not question.can_vote():
                error = "Poll ended, so no vote acceptable."
                return HttpResponseRedirect(reverse('polls:index'), messages.error(request, error))
        except ObjectDoesNotExist:
            error = "Poll does not exist."
            return HttpResponseRedirect(reverse('polls:index'), messages.error(request, error))
        self.object = self.get_object()
        context = self.get_context_data(object=self.get_object())
        template_name = 'polls/detail.html'
        return render(request, context=context, template_name=template_name)

    def get_queryset(self):
        """
        Get the queryset of question by sorting with pub date.
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')

class ResultsView(generic.DetailView):
    """View for result."""

    model = Question
    template_name = 'polls/results.html'

@login_required()
def vote(request, question_id):
    """
    Vote for each question by using question_id.
    """
    user = request.user
    question = get_object_or_404(Question, pk=question_id)
    if not question.can_vote():
        error = "Poll ended so no vote accepted."
        return HttpResponseRedirect(reverse('polls:index'), messages.error(request, error))
        
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "No choice selected.context=",
        })
    else:
        Vote.objects.update_or_create(user=user, question=question, defaults={'selected_choice': selected_choice})
        for choice in question.choice_set.all():
            choice.votes = Vote.objects.filter(question=question).filter(selected_choice=choice).count()
            choice.save()
        if Vote.objects.filter(question=question).filter(selected_choice=choice).count():
            selected_choice.votes += 1
            selected_choice.save()
        for question in Question.objects.all():
            question.last_vote = str(request.user.vote_set.get(question=question).selected_choice)
            question.save()

        date = datetime.now()
        log = logging.getLogger("polls")
        log.info("User: %s, Poll's ID: %d, Date: %s.", user, question_id, str(date))
        url = reverse('polls:results', args=(question.id,))
        return HttpResponseRedirect(url)
