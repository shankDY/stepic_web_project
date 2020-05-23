from django.test import TestCase
from django.contrib.auth.models import User

from qa.models import Question, QuestionManager, Answer

# from views import Question

class TestModels(TestCase):
    def test_import(self):
        import qa.models

class TestUser(TestCase):
    def test_user(self):
        user = User(username='x', password='y')
        try:
            user.save()
        except:
            assert False, "Failed to create user model, check db connection"



class TestQuestionManager(TestCase):
    def test_question_manager(self):
        mgr = Question.objects
        assert isinstance(mgr, QuestionManager), "Question.objects is not an QuestionManager"
        assert hasattr(mgr, 'new'), "QuestionManager has no 'new' queryset method"
        assert hasattr(mgr, 'popular'), "QuestionManager has no 'popular' queryset method"


class TestQuestionAndAnswer(TestCase):
    def test_question(self):
        user, _ = User.objects.get_or_create(username='x', password='y')
        try:
            question = Question(title='qwe', text='qwe', author=user)
            question.save()
        except:
            assert False, "Failed to create question model, check db connection"
        try:
            answer = Answer(text='qwe', question=question, author=user)
            question.save()
            answer.save()
        except:
            assert False, "Failed to create answer model, check db connection"