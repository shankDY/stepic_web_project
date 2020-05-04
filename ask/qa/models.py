from django.db import models
from django.contrib.auth.models import User


# Create your models here.

#custom Query_manager
class QuestionManager(models.Manager):

    #возвращает поcледние добавленные вопросы(сортировка по времени добавления, начиная с самого последнего)
    def new(self):
        return self.order_by("-added_at")

    #Сортировка по рейтингу(по убыванию)
    def popular(self):
        return self.order_by("-rating")

# модель для вопроса
class Question(models.Model):
    #default query_manager
    questions = models.Manager()
    # custom query_manager
    objects = QuestionManager()

    title = models.CharField(max_length=60)
    text = models.CharField(max_length=255)
    #дата добавления вопроса
    added_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name="question_like_user")

    #Вывод на печать
    def __str__(self):
        return self.title
    
    #возвращение пути модели
    def get_url(self):
        return f"/question/{self.pk}"


# модель для ответа
class Answer(models.Model):
    text = models.CharField(max_length=60)
    #дата добавления ответа
    added_at = models.DateTimeField(auto_now_add=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    author = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.text