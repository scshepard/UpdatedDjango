from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
#from django.template import RequestContext, loader
from django.http import HttpResponse
from django.utils import timezone

from polls.models import Question, Choice

class IndexView(generic.ListView):
	template_name = 'polls/index.html'
	context_object_name = 'latest_question_list'

	def get_queryset(self):
		"""Return the last five published questions."""
		#return Question.objects.order_by('-pub_date')[:5]
		return Question.objects.filter(
			pub_date__lte=timezone.now()
		).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
	model = Question
	template_name = 'polls/detail.html'
	def get_queryset(self):
		"""
		excludes any questions that aren't published yet.
		"""

		return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
	model = Question
	template_name = 'polls/results.html'

def index(request):
	#return HttpResponse("Hello, world. You're at the polls index.")
	latest_question_list = Question.objects.order_by('-pub_date')[:5]
	#template = loader.get_template('polls/index.html')
	#context = RequestContext(request, {
		#'latest_question_list': latest_question_list,
	#})
	context = {'latest_question_list': latest_question_list}
	# output = ', '.join([p.question_text for p in latest_question_list])
	# return HttpResponse(output)
	#return HttpResponse(template.render(context))
	return render(request,'polls/index.html', context)

def detail(request,question_id):
	#return HttpResponse("You're looking at question %s." % question_id)
	
	#try:
		#question = Question.objects.get(pk=question_id)
	#except Question.DoesNotExist:
		#raise Http404
	
	#return render(request,'polls/detail.html',{'question': question})
	question = get_object_or_404(Question,pk=question_id)
	return render(request,'polls/detail.html',{'question': question})

def results(request,question_id):
	question=get_object_or_404(Question,pk=question_id)
	return render(request,'polls/results.html', {'question': question})
	#response = "You're looking at the resuolts of question %s."
	#return HttpResponse(response % question_id)

def voteOld(request,question_id):
	return HttpResponse("You're voting on question %s." % question_id)

def vote(request, question_id):
	p = get_object_or_404(Question, pk=question_id)
	try:
		selected_choice = p.choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
		# redisplay the question voting form
		return render(request, 'polls/detail.html', {
			'question': p,
			'errror_message': "You didn't select a choice.",
		})
	else:
		selected_choice.votes += 1
		selected_choice.save()
		# always return an HttpResponseRedirect after successfullly dealing
		# with POSt data. This prevents data from being posted twice if a 
		# user hits the Back button
		return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))

# Create your views here.
