from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.core.paginator import Paginator, EmptyPage
from django.core.exceptions import ObjectDoesNotExist

from qa.models import Question, Answer


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
    try:
        question = Question.objects.get(pk=question_id)
    except ObjectDoesNotExist:
        raise Http404
    answer = question.answer_set.all()
    return render(request, 'question_detail.html',
                  {'questions': question,
                   'answers': answer,})