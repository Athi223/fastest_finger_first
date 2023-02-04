from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Allotment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    questions = models.TextField(default="[]")

class Question(models.Model):
    question = models.TextField()
    option0 = models.TextField()
    option1 = models.TextField()
    option2 = models.TextField()
    option3 = models.TextField()
    correct = models.IntegerField()
