from rest_framework import serializers

from .models import Question, Answer, UserAnswer


class AnswerSerializer(serializers.ModelSerializer):
    answer = serializers.CharField(source='letter')

    class Meta:
        model = Answer
        fields = ['question', 'answer']


class QuestionSerializer(serializers.ModelSerializer):
    answers = serializers.StringRelatedField(many=True)
    question = serializers.CharField(source='text')

    class Meta:
        model = Question
        fields = ['number', 'question', 'answers']


class UserAnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserAnswer
        fields = '__all__'