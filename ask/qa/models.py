from django.db import models
from django.contrib.auth.models import User


# Create your models here.

#custom Query_manager
class QuestionManager(models.Manager):
    def new(self):
        return self.order_by("-added_at")

    def popular(self):
        return self.order_by("-rating")

# model for question
class Question(models.Model):
    #default query_manager
    questions = models.Manager()
    # custom query_manager
    objects = QuestionManager()

    title = models.CharField(max_length=60)
    text = models.CharField(max_length=255)
    #date ad question
    added_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name="question_like_user")

    def __str__(self):
        return self.title
    
    def get_url(self):
        return "/question/{}/".format(self.pk)


# model for answer
class Answer(models.Model):
    text = models.CharField(max_length=60)
    #date ad answer
    added_at = models.DateTimeField(auto_now_add=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.text