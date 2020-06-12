from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_GET
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout

from qa.models import Question, Answer
from qa.forms import AskForm, AnswerForm, SignupForm, LoginForm

# Create your views here.

def test(request, *args, **kwargs):
    return HttpResponse('OK')


def paginate(request, qs):
    """create pageination"""
    try:
        page_number = int(request.GET.get('page',1))
    except ValueError:
        raise Http404
    paginator = Paginator(qs, 10)
    try:
        # if the last page that the user called is empty, the last full page is displayed
        page_content = paginator.get_page(page_number)
    except EmptyPage:
        page_content = paginator.get_page(paginator.num_pages)
    return paginator, page_content

@require_GET
def index(request):
    """Home page
    The last question asked is the first on the list.
    The page displays 10 questions
    
    """
    # take question sorted by time add
    qs = Question.objects.new()
    paginator, page = paginate(request, qs)
    return render(request, 'list.html', 
                 {'title': 'Latest',
                  'paginator': paginator,
                  'page': page,
                  'questions': page.object_list,})
    

@require_GET   
def popular_question(request):
    """list of "popular" questions.
    Sorting in decreasing order by field rating

    """
    # take question sorted by rating
    qs = Question.objects.popular()
    paginator, page = paginate(request, qs)
    return render(request, 'list.html',
                  {'title': 'Popular',
                   'paginator': paginator,
                   'page': page,
                   'questions': page.object_list,})



def question_detail(request, question_id):
    """One question page. 
    This page displays the title, text of the question 
    and all the answers to this question.
    
    """
    question = get_object_or_404(Question, pk=question_id)
    answers = question.answer_set.all()
    form = AnswerForm(request.POST)

    if request.method == 'POST' and form.is_valid():
        form._user = request.user
        answers = form.save()
        url = question.get_url()
        return HttpResponseRedirect(url)
    else:
        form = AnswerForm(initial={'question': question_id})

    return render(request, 'question_detail.html',
                  {'questions': question,
                   'answers': answers,
                   'user': request.user,
                   'form': form,})


@login_required(login_url='/login')
def ask(request):
    """With a GET request - the AskForm form is displayed, 
    with a POST request the form should create a new question and redirect to the question page

    """
    form = AskForm(request.POST)
    if request.method == 'POST' and form.is_valid():
        form._user = request.user
        question = form.save()
        url = question.get_url()
        return HttpResponseRedirect(url)
    else:
        form = AskForm()
    return render(request, 'ask.html', { 'form': form })

def user_login(request):
    """With a GET request, a form for entering data should be displayed, with a POST request,
    a login is made to the site, the redirect to the main page is returned. 
    The user should receive an authorization cookie named sessionid.

    """
    form = LoginForm(request.POST)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')

    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form,})


def user_sign(request):
    """With a GET request, a form for entering data should be displayed,
    with a POST request a new user is created, the user created is logged in to the site,
    the redirect is returned to the main page. The user must receive an authorization cookie

    """
    form = SignupForm(request.POST)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form, })

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/login')
