from django.shortcuts import render, redirect

from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError

from .serializers import QuestionSerializer, UserAnswerSerializer, ListUserAnswerSerializer
from .models import Question, Answer, UserAnswer


def index(request):
    return redirect('list-questions')

class QuestionAPIView(generics.ListAPIView):
    """
        Endpoint to allow users to request the questions list
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = QuestionSerializer

    def get_queryset(self):
        questions = Question.objects.all()

        return questions


class UserAnswerAPIView(APIView):
    """
        Endpoint to allow users to post the answers
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = UserAnswerSerializer

    def post(self, request):
        if not request.user.is_superuser:
            try:
                data = request.data.copy()
                """
                    Creating a new data queryset to extract properly 
                    the answers of each user into a ManyToMany format
                """
                new_data = {'user': request.user.id, 'answers': []}
                for answer in data:
                    new_data['answers'] += [Answer.objects.get(question=answer['question'],
                                                        letter=answer['answer']).id] if 'answer' in answer else []
                    if Question.objects.get(id=answer['question']).\
                            is_comment and 'comment' in answer:
                                new_data['comment'] = answer['comment']

                serializer = UserAnswerSerializer(data=[new_data], many=True)

                if serializer.is_valid():
                    serializer.save()
                    return Response({'detail': 'Survey completed!'},
                                    status=status.HTTP_200_OK)
                else:
                    return Response({'message': serializer.errors},
                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            except Exception as ex:
                print(ex)
                return Response({'detail': 'Inalid answer format or data. '
                                            'You have to insert a valid answer of each question'},
                                status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail': 'Admin users not allowed to answer the survey.'},
                        status=status.HTTP_400_BAD_REQUEST)

class ListAnswerAPIView(generics.ListAPIView):
    """
        Endpoint to allow users to request the answers list
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = ListUserAnswerSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            answers = UserAnswer.objects.all()
            return answers
        raise ValidationError({"error": ["You don't have enough permission."]})
