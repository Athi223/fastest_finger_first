from django.contrib import admin
from .models import Allotment, Question

# Register your models here.
@admin.register(Allotment)
class AllotmentAdmin(admin.ModelAdmin):
    pass

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    pass
