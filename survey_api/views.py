from django.shortcuts import render, redirect

from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers import QuestionSerializer, AnswerSerializer, UserAnswerSerializer
from .models import Question, Answer


def index(request):
    return redirect('questions')

class QuestionAPIView(generics.ListAPIView):
    """
        Endpoint to allow users to request the question's list
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
        try:
            data = request.data.copy()
            print(data)
            """
                Creating a new data queryset to extract properly 
                the answers of each user into a ManyToMany type
            """
            new_data = [{'user': request.user.id,
                        'answers': [Answer.objects.get(question=answer['question'],
                                                        letter=answer['answer']).id
                                    for answer in data if 'answer' in answer],
                        'comment': data[0]['comment'] if 'comment' in data[0] else ''}]
            serializer = UserAnswerSerializer(data=new_data, many=True)
            if serializer.is_valid():
                print(serializer.data)
                serializer.save()
                return Response({'status': 'success', 'data': serializer.data},
                                status=status.HTTP_200_OK)
            else:
                return Response({'status': 'error', 'message': serializer.errors},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as ex:
            print(ex)
            return Response({'status': 'error',
                             'message': 'Inalid answer format or data. '
                                        'You have to insert a valid answer of each question'},
                            status=status.HTTP_400_BAD_REQUEST)

        # question_number = data.get('question')

        # if question_number:
        #     user_answer = UserAnswer.objects.filter(user=request.user)
        #     question = Question.objects.get(number=int(question_number))
        #
        #     if not user_answer:
        #         data['date'] = date.today()
        #         data['user'] = request.user.id
        #         data['answer'] = Answer.objects.get(question=question,
        #                                             letter=data['answer']).id if 'answer' in data else None


            # else:
            #     if question.is_comment:
            #         user_answer[0].update(comment=data['comment'])
            #     else:
            #         try:
            #             answer = Answer.objects.get(question=int(question_number),
            #                                         letter=data['answer'])
            #             user_answer[0].answer.add(answer)
            #         except Exception as ex:
            #             print(ex)
            #             return Response('There was an error, you have '
            #                             'to insert a valid question and answer.')
            #
            #     user_answer[0].save()
            #
            #     return Response({"status": "success"},
            #                     status=status.HTTP_200_OK)