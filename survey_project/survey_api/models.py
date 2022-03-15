from django.db import models
from rest_framework.authtoken.admin import User


class Question(models.Model):
    text = models.TextField(verbose_name='Question', blank=False, null=False)


class Answer(models.Model):
    text = models.CharField(verbose_name='Answer', max_length=30)
    question = models.ForeignKey(Question, verbose_name='Question', on_delete=models.CASCADE)


class UserAnswer(models.Model):
    user = models.ForeignKey(User, verbose_name='User', on_delete=models.CASCADE)
    answer = models.ManyToManyField(Answer, verbose_name='Answer', blank=True,
                                    null=True)
    date = models.DateField(editable=False)
