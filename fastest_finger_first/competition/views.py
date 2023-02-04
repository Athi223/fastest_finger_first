# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import Question
from . import forms
import requests
from random import shuffle

@staff_member_required
def staff(request):
	return render(request, "competition/staff.html")

@staff_member_required
def populate_questions(request, amount=20):
	response = requests.get(f"https://opentdb.com/api.php?amount={amount}&category=18&type=multiple")
	if response.status_code == 200:
		questions = []
		parsed_questions = response.json()
		for parsed_question in parsed_questions["results"]:
			answers = [ parsed_question["correct_answer"] ]
			answers.extend(parsed_question["incorrect_answers"])
			shuffle(answers)
			questions.append(Question(
				question=parsed_question["question"],
				option0=answers[0],
				option1=answers[1],
				option2=answers[2],
				option3=answers[3],
				correct=answers.index(parsed_question["correct_answer"])
			))
		objs = Question.objects.bulk_create(questions)
		return HttpResponse(201, "Questions added successfully!")
	return HttpResponse(500, "Failed to add questions!")

@staff_member_required
def get_question(request):
	question = Question.objects.get(pk=request.GET["number"])
	return JsonResponse({
		"question": question.question,
		"option0": question.option0,
		"option1": question.option1,
		"option2": question.option2,
		"option3": question.option3
	})

@login_required
def index(request):
	return render(request, "competition/room.html")

def signin(request):
	form = forms.LoginForm()
	message = ''
	if request.method == 'POST':
		form = forms.LoginForm(request.POST)
		if form.is_valid():
			user = authenticate(
				username=form.cleaned_data['username'],
				password=form.cleaned_data['password'],
			)
			if user is not None:
				login(request, user)
				if user.is_staff:
					return redirect("/staff")
				return redirect("/")
			else:
				message = 'Login failed!'
	return render(
		request, 'competition/login.html', context={'form': form, 'message': message})


def signout(request):
	logout(request)
	return redirect('/')
