# chat/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("staff/", views.staff, name="staff"),
    path("signin/", views.signin, name="signin"),
    path("signout/", views.signout, name="signout"),
    path("populate_questions/", views.populate_questions, name="populate_questions"),
    path("get_question/", views.get_question, name="get_question"),
]
