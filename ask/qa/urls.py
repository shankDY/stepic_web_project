from django.urls import path
import views
urlpatterns = [
    path(r'^$',views.test,name='index'),
    path(r'^login/$',views.test,name='login'),
    path(r'^signup/$',views.test,name='signup'),
    path(r'^question/<\d+>/$',views.test,name='question'),
    path(r'^ask/',views.test,name='ask'),
    path(r'^popular/$',views.test,name='popular'),
    path(r'^new/$',views.test,name='new'),
]