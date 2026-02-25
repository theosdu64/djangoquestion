from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Question,Choice
from django.template import loader
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.db.models import F
from django.views import generic
from django.db.models import Sum, Avg, Count, Max, Min

class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by("-pub_date")[:5]
    
class AllView(generic.ListView):
    template_name = "polls/all.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by("-pub_date")[:5]
    
def statistics(request):
    stats = {}
    
    vote_par_sondage = Choice.objects.aggregate(total=Sum("votes"))['total'] or 0
    nbSondage = Question.objects.count()
    
    stats.update(
        vgVoteParSondage = int(vote_par_sondage / nbSondage)
    )
    stats.update(
        Question.objects.aggregate(
            total_questions=Count("id"),
            lastQuestion=Max("pub_date")
        )
    )
    stats.update(
        Choice.objects.aggregate(
            total_choices=Count("id"),
            nb_vote=Sum("votes"),
        )
    )
    return render(request, 'polls/statistics.html', {"stats": stats})   

class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

class FrequencyView(generic.DetailView):
    model = Question
    template_name = "polls/frequency.html"

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))