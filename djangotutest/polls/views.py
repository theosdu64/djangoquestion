from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Question,Choice
from django.template import loader
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import F
from django.views import generic
from django.db.models import Sum, Avg, Count, Max, Min
from django.utils import timezone
from .forms import QuestionForm


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[
            :10
        ]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["create_question_form"] = QuestionForm()
        return context
    
    def post(self, request, *args, **kwargs):
        form = QuestionForm(request.POST)

        if form.is_valid():
            question_text = form.cleaned_data["question_text"]
            q = Question.objects.create(
                question_text=question_text,
                pub_date=timezone.now()
            )
            for c in range(1,6):
                choice_text = {form.cleaned_data.get(f'choice{c}')}
                if choice_text:
                    q.choice_set.create(choice_text=choice_text)

            return redirect("polls:index")

        context = self.get_context_data()
        context["create_question_form"] = form
        return self.render_to_response(context)
    
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
    
    last_question_id = Question.objects.aggregate(Max("id"))["id__max"]
    last_question_text = Question.objects.get(id=last_question_id).question_text

    stats.update(
        vgVoteParSondage = int(vote_par_sondage / nbSondage),
        lastQuestion=last_question_text
    )
    stats.update(
        Question.objects.aggregate(
            total_questions=Count("id"),
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
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))


class DetailView(generic.DetailView) : 
    ...

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())