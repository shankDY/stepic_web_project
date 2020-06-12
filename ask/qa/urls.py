from django.urls import path
from qa.views import index, popular_question, question_detail, ask, test, user_login, user_sign, user_logout
urlpatterns = [
    path('', index, name='index'),
    path('login/', user_login, name='login'),
    path('signup/', user_sign,name='signup'),
    path('question/<int:question_id>/', question_detail, name='question'),
    path('ask/', ask, name='ask'),
    path('popular/', popular_question, name='popular'),
    path('logout/',user_logout, name='logout')
]