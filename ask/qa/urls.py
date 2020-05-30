from django.urls import path
from qa.views import index, popular_question, question_detail, ask, test
urlpatterns = [
    path('', index, name='index'),
    path('login/', test, name='login'),
    path('signup/', test,name='signup'),
    path('question/<int:question_id>/', question_detail, name='question'),
    path('ask/', ask, name='ask'),
    path('popular/', popular_question, name='popular'),
    # path('new/', test, name='new'),
]