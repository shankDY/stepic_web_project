from django.db import models
from django.contrib.auth.models import User


# Create your models here.

#custom Model_manager
class QuestionManager(models.Manager):
    #sorted by question time add
    def new(self):
        return self.order_by("-added_at")
    #sorted by rating
    def popular(self):
        return self.order_by("-rating")

# model for question
class Question(models.Model):
    # custom Model_manager
    objects = QuestionManager()
    title = models.CharField(max_length=60)
    text = models.TextField()
    #date ad question
    added_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    likes = models.ManyToManyField(User, related_name="question_like_user")

    def __str__(self):
        return self.title
    
    #urls_path
    def get_url(self):
        return f"/question/{self.pk}/"


# model for answer
class Answer(models.Model):
    objects = models.Manager()
    text = models.TextField()
    #date ad answer
    added_at = models.DateTimeField(auto_now_add=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.text