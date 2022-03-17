import datetime

from rest_framework import serializers

from .models import Question, Answer, UserAnswer

class AnswersListField(serializers.RelatedField):
    def to_representation(self, value):
        return '%s' % (value.text)


class DateField(serializers.RelatedField):
    def to_representation(self, value):
        return value.strftime('%d/%m/%Y')


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
    user = serializers.CharField(source='user.email')
    # answers = serializers.StringRelatedField(many=True)
    answers = AnswersListField(many=True, read_only=True)
    date = DateField(read_only=True)

    def create(self, validated_data):
        try:
            print(validated_data)
            answers = validated_data.pop('answers') if 'answers' in validated_data else []
            user = validated_data.pop('user')
            comment = validated_data.pop('comment') if 'comment' in validated_data else ''
            if not (answers or comment):
                raise serializers.ValidationError()

            user_answer = UserAnswer.objects.create(user=user,
                                                    comment=comment,
                                                    **validated_data)
            print(user_answer)
            for answer in answers:
                user_answer.answers.add(answer)
            user_answer.save()

        except Exception as e:
            raise serializers.ValidationError(e)

        return user_answer

    def validate_user(self, value):
        if UserAnswer.objects.filter(user=value):
            raise serializers.ValidationError('This user already answered the survey')
        return value

    class Meta:
        model = UserAnswer
        fields = ['user', 'date', 'answers', 'comment']
