from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework import generics

from .serializers import QuestionSerializer, AnswerSerializer, UserAnswerSerializer
from .models import Question, Answer, UserAnswer


class QuestionAPIView(generics.ListAPIView):

    serializer_class = QuestionSerializer

    def get_queryset(self):
        questions = Question.objects.all()

        return questions
