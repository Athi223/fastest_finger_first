# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from . import forms

@staff_member_required
def staff(request):
	return render(request, "competition/staff.html")

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
