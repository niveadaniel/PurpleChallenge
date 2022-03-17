from django.contrib import admin

from .models import Question, Answer, UserAnswer


@admin.register(Question)
class Question(admin.ModelAdmin):
    list_display = ['number', 'text', 'is_comment']


@admin.register(Answer)
class Answer(admin.ModelAdmin):
    list_display = ['letter', 'text', 'question']


@admin.register(UserAnswer)
class UserAnswer(admin.ModelAdmin):
    list_display = ['user', 'date', 'get_answers', 'comment']

    def get_answers(self, obj):
        return ",\n".join([a.text for a in obj.answers.all()])
