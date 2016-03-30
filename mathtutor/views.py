from django.shortcuts import render, render_to_response
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import auth
from .models import Constants, Quiz, QuizGroup, SubCategory, LearnItem
from django.utils import timezone
from django.http import HttpResponseRedirect
from mathtutor.decorators import check_category_access

constants = Constants()
# Create your views here.

def partial_access_check(user):
    return user.student.check_access()['partial']

def full_access_check(user):
    return user.student.check_access()['full']

@login_required(login_url='/login/')
def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('m:info'))
    else:
        return render(request, 'login.html',)

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('m:index'))

def noaccess(request):
    activation = request.user.student.access_date()
    end_date = activation + Constants.investment_time
    end_date_bool = timezone.localtime(timezone.now())
    if timezone.localtime(timezone.now()) < activation:
        auth.logout(request)
        context = {
            'activation': activation,
            'end_date_bool': end_date_bool,
            'tooSoon': True,
            "Constants": Constants,
        }
        return render(request, "mathtutor/registration/noaccess.html", context)
    else:
        return HttpResponseRedirect(reverse('m:index'))

@login_required
@user_passes_test(full_access_check, login_url="/noaccess/", redirect_field_name=None)
def dashboard(request):
    student = request.user.student
    categories = Constants.categories[student.group]
    for c in categories:
        c['results']=student.get_quiz_progress(c['key'])
    context = {
        'student': student,
        'categories': categories,
        "Constants": Constants,
    }
    return render(request, 'mathtutor/dashboard.html', context)

def post_surveys(request):
	pass

@login_required
@user_passes_test(full_access_check, login_url="/noaccess/", redirect_field_name=None)
def quiz_or_practice(request, category):
    student = request.user.student
    context = {
        'student': student,
        'category': filter(lambda c: c['key']==category, Constants.categories[student.group]),
        'Constants': Constants,
    }
    return render(request, 'mathtutor/quiz_or_practice.html', context)

@login_required
@user_passes_test(full_access_check, login_url="/noaccess/", redirect_field_name=None)
def list_quizes(request, category):
    student = request.user.student
    quizGroup = QuizGroup.objects.get(group=student.group)
    quizListObjects = quizGroup.quiz_set.filter(q_category=category)
    quizList = quizListObjects.values()
    for quizObj in quizListObjects:
        results = quizObj.get_results(request.user)
        name = quizObj.get_display_name()
        quiz = filter(lambda q: q['q_id']==quizObj.q_id, quizList)[0]
        quiz['display_name'] = name
        quiz['results'] = results
        quiz['url'] = quizObj.get_url()
    context = {
        'student': student,
        'category': filter(lambda c: c['key']==category, Constants.categories[student.group]),
        'quizList': quizList,
        "Constants": Constants,
    }
    return render(request, "mathtutor/quiz_list.html", context)


@login_required
@user_passes_test(full_access_check, login_url="/noaccess/", redirect_field_name=None)
def practice(request, category, which, itemId=None):
    student = request.user.student
    quizGroup = QuizGroup.objects.get(group=student.group)
    learnItems = []
    for subCategory in SubCategory.objects.all():
        learnItems.append(subCategory.get_list_of_items(quizGroup, category, which))
    context = {
        'student': student,
        'category': filter(lambda c: c['key']==category, Constants.categories[student.group]),
        'learnItems': learnItems,
        "Constants": Constants,
        }
    if itemId == None:
        return render(request, "mathtutor/practice_list.html", context)
    else:
        context['learnItem'] = LearnItem.objects.get(id=itemId)
        return render(request, "mathtutor/practice_item.html", context)

@login_required
@user_passes_test(partial_access_check, login_url="/noaccess/", redirect_field_name=None)
def parent_survey(request):
    context = {
        'user': request.user,
        'student': request.user.student,
        'parent_address_form': Constants.parent_forms[0]['qid'],
        'parent_survey_english': Constants.parent_forms[1]['qid'],
        'parent_survey_spanish': Constants.parent_forms[2]['qid'],
    }
    return render_to_response('mathtutor/info.html', context)

def glossary(request, itemId=None):
	pass





