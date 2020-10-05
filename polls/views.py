from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, reverse
from polls.models import Question, Choice
from django.views import generic
# Create your views here.
def index(request):
    latest_question_list = Question.objects.all().order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['select'])
    except(KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice"
        })
    else:
        selected_choice.votes +=1
        selected_choice.save()
    return HttpResponseRedirect(reverse('polls:result', args=(question.id,)))

def result(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/result.html', {'question': question})


def reset(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    reset_list = question.choice_set.all()
    for i in reset_list:
        i.votes = 0
        i.save()
    return HttpResponseRedirect(reverse('polls:result', args=(question_id,)))
