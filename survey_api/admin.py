from django.contrib import admin

from .models import Question, Answer


@admin.register(Question)
class Question(admin.ModelAdmin):
    list_display = ['number', 'text', 'is_comment']


@admin.register(Answer)
class Answer(admin.ModelAdmin):
    list_display = ['letter', 'text', 'question']
