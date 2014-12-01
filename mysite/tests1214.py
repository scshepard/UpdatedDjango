from django.test import TestCase

# Create your tests here.
import datetime

from django.utils import timezone
from django.test import TestCase

from polls.models import Question
from django.core.urlresolvers import reverse

class QuestionMethodTests(TestCase):

	def test_was_published_recently_with_future_question(self):
		"""
		was_published_recently() should return False for questions whose
		pug_date is in the future
		"""
		time = timezone.now() + datetime.timedelta(days=30)
		future_question = Question(pub_date = time)
		self.assertEqual(future_question.was_published_recently(), False)

	def test_was_published_recently_with_old_question(self):
		"""
		was_published_recently() should return False for questions whos
		pub_date is older than 1 day
		"""
		time = timezone.now() - datetime.timedelta(days=30)
		old_question = Question(pub_date = time)
		self.assertEqual(old_question.was_published_recently(), False)

	def test_was_published_recently_with_recent_question(self):
		"""
		was_published_recently() should return True for questions whose
		pub_date is within the last day
		"""
		time = timezone.now() - datetime.timedelta(hours=1)
		recent_question = Question(pub_date=time)
		self.assertEqual(recent_question.was_published_recently(), True)

	def create_question(question_text,days):
		"""
		creates a question with the given 'question_text' published the given
		numbr of 'days' offset to now (negative for questions published
		in the past, positive for questions that have yet to be published.
		"""
		time = timezone.now() + datetime.timedelta(days=days)
		return Question.objects.create(question_text=question_text,
						pub_date=time)

class QuestionViewTests(TestCase):
	def test_index_view_with_no_qustions(self):
		"""
		if no questions exist, an appropriate message should be displayed.
		"""
		response = self.client.get(reverse('polls:index'))
		self.assertEqual(response.status_code,200)
		self.assertContains(response, "No polls are available")
		self.assserQuerysetEqual(response.context['lastest_question_list'],[])