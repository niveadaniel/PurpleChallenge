from django.shortcuts import render, redirect

from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.response import Response

from .serializers import QuestionSerializer, AnswerSerializer, UserAnswerSerializer
from .models import Question, Answer, UserAnswer


def index(request):
    return redirect('questions')

class QuestionAPIView(generics.ListAPIView):

    serializer_class = QuestionSerializer

    def get_queryset(self):
        questions = Question.objects.all()

        return questions


class AnswerAPIView(APIView):
    serializer_class = AnswerSerializer

    def post(self, request):
        serializer = AnswerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data},
                            status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)