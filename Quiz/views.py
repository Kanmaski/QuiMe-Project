from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from .forms import CustomUserCreationForm, LoginForm
from .models import CreateQuiz, QuizResult
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.forms import modelformset_factory, Textarea
from django import forms
import random
from django.contrib.auth.decorators import login_required


KeyMaster = list('abcdefghijklmnopqrstuvwxyz')
KeyMaster += list('abcdefghijklmnopqrstuvwxyz'.upper())
# Create your views here.
def home(request):
    return render(request, 'Quiz/home.html')

def signup(request):
    if request.method == 'GET':
        return render(request, 'Quiz/SignUp.html', {'SignUpForm':CustomUserCreationForm() })
    else:
        SignUpForm = CustomUserCreationForm(request.POST)
        if request.POST['password1'] == request.POST['password2']:
            if SignUpForm.is_valid():
                try:
                    NewUser = User.objects.create_user(username = SignUpForm.cleaned_data['UserName'], email = SignUpForm.cleaned_data['Useremail'], password = SignUpForm.cleaned_data['password1'])
                    NewUser.save()
                    login(request, NewUser)
                    return redirect('createquiz')
                except IntegrityError:
                    return render(request,'Quiz/SignUp.html',{'SignUpForm':CustomUserCreationForm(), 'Userexist': 'Username already exist, choose new username'})
            else:
                return render(request,'Quiz/SignUp.html',{'SignUpForm': CustomUserCreationForm(), 'Baddata': 'Bad Input data'})
        else:
            return render(request,'Quiz/SignUp.html',{'SignUpForm':CustomUserCreationForm(), 'Passwordnomatch': 'Password does not match'})

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'Quiz/login.html', {'loginform':LoginForm()})
    else:
        user_login = authenticate(username=request.POST['UserName'], password=request.POST['password'])
        if user_login is not None:
            login(request, user_login)
            return redirect('createquiz')
        else:
            return render(request,'Quiz/login.html',{'loginform':LoginForm(),'loginerror': 'unable to login'})

@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

@login_required
def createquizview(request):
    CreateQuizForm = modelformset_factory(CreateQuiz, exclude=('key', 'creation_date', 'User', 'title'), extra=10, max_num=10, validate_min=5, widgets={'question':Textarea(attrs={'cols':50, 'rows': 4,'style': 'resize: none'}), 'option':Textarea(attrs={'cols':50, 'rows': 4,'style': 'resize: none'})})
    if request.method == 'GET':
        formset=CreateQuizForm(queryset=CreateQuiz.objects.none())
        return render(request, 'Quiz/createquiz.html', {'formset': formset})
    elif request.method == 'POST':
        formset = CreateQuizForm(request.POST)
        key_list = random.choices(KeyMaster, k = 12)
        key = ''
        for i in range(12):
            if i % 4 == 0 and i > 0 and i < 12:
                key += '-'
            key += key_list[i]
        if formset.is_valid:
            for form in formset:
                if form['question'].value() and form['option'].value() and form['answer'].value():
                    createquizinstance = CreateQuiz()
                    createquizinstance.question = form['question'].value()
                    createquizinstance.option= form['option'].value()
                    createquizinstance.answer= form['answer'].value()
                    createquizinstance.key = key
                    createquizinstance.title= request.POST['title']
                    createquizinstance.User= request.user
                    createquizinstance.save()
            return redirect('createquizsuccess', key = key)
        else:
            return render(request, 'Quiz/createquiz.html', {'formset': formset,'error':'could not save, enter valid data'})

@login_required
def createquizsuccess(request, key):
    if request.method == 'GET':
        return render(request, 'Quiz/createquizsuccess.html',{'key': key})


def takequizpreview(request):
    if request.method == 'GET':
        return render(request,'Quiz/takequizpreview.html')
    else:
        return redirect('takequiz', key=request.POST['key'])

def takequiz(request, key):
    quizzes = get_list_or_404(CreateQuiz, key = key)
    if request.method == 'GET':
        return render(request, 'Quiz/takequiz.html', {'quizzes': quizzes})
    else:
        if request.POST is None:
            return render(request, 'Quiz/takequiz.html', {'quizzes': quizzes, 'message':'Failed to answer any question'})
        else:
            pass_fail_result=[]
            selected_answer={}
            for quiz in quizzes:
                selected_answer[quiz.question]=request.POST[quiz.question]
                if quiz.answer.lower() == request.POST[quiz.question].lower():
                    pass_fail_result.append('Pass')
                else:
                    pass_fail_result.append('Fail')
            score=pass_fail_result.count('Pass')/len(pass_fail_result)
            ##save result in DB
            try:
                quiztaker = QuizResult.objects.get(key= key, taker=request.POST['QuizTakerName'])
                return render(request,'Quiz/quizresult.html',{'quizzes': quizzes, 'marks':pass_fail_result, 'Useranswer':selected_answer, 'score':score, 'error':'User has already taken this quiz'})
            except:
                quiztaker = QuizResult(key=key, taker=request.POST['QuizTakerName'], score=score, percentscore=score*100)
                quiztaker.save()
            return render(request,'Quiz/quizresult.html',{'quizzes': quizzes, 'marks':pass_fail_result, 'Useranswer':selected_answer, 'score':score})

def viewresultpreview(request):
    if request.method == 'GET':
        return render(request,'Quiz/viewresultpreview.html')
    else:
        return redirect('viewresult', key=request.POST['key'])


def viewresult(request, key):
    results = QuizResult.objects.filter(key=key).order_by('-percentscore')
    return render(request, 'Quiz/viewresult.html', {'results': results})


def quizresult(request):
    return render(request,'Quiz/quizresult.html')






