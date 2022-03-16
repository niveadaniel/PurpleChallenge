from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models


class Question(models.Model):
    text = models.TextField(verbose_name='Question', blank=False, null=False)
    number = models.IntegerField(blank=False, null=False)
    is_comment = models.BooleanField(default=False)

    class Meta:
        unique_together = ['text', 'number']

    def __str__(self):
        return self.text


class Answer(models.Model):
    text = models.CharField(verbose_name='Answer', max_length=30)
    question = models.ForeignKey(Question, related_name='answers',
                                 verbose_name='Question', on_delete=models.CASCADE)
    letter = models.CharField(max_length=1, null=False, blank=False)

    def __str__(self):
        return '{}: {}'.format(self.letter, self.text)

    def validate_unique(self, *args, **kwargs):
        super().validate_unique(*args, **kwargs)
        if self.__class__.objects. \
                filter(question=self.question, letter=self.letter). \
                exists():
            raise ValidationError(
                message='Answer with this letter and question already exists.',
                code='unique_together',
            )


class UserAnswer(models.Model):
    user = models.ForeignKey(User, verbose_name='User', on_delete=models.CASCADE)
    answer = models.ManyToManyField(Answer, verbose_name='Answer', blank=True)
    date = models.DateField(editable=False)
    comment = models.TextField(null=False, blank=True)



