from rest_framework import serializers
from rest_framework.serializers import ValidationError


def validateQuestionType(value):
    if not value in ['TEXT', 'CHOICE', 'MULTIPLE_CHOICE']:
        raise ValidationError('Invalid question type')


class PollSerializer(serializers.Serializer):
    'Опрос'
    id = serializers.IntegerField(required=False)
    name = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=300)
    startDate = serializers.DateField()
    finishDate = serializers.DateField()

class QuestionSerializer(serializers.Serializer):
    'Вопрос'
    id = serializers.IntegerField(required=False)
    type = serializers.CharField(max_length=30, validators=[validateQuestionType])
    text = serializers.CharField(max_length=300)

class OptionSerializer(serializers.Serializer):
    'Вариант ответа'
    id = serializers.IntegerField(required=False)
    index = serializers.IntegerField(required=False)
    text = serializers.CharField(max_length=100)

class UserOptionSerializer(serializers.Serializer):
    'Вариант ответа для пользователя'
    index = serializers.IntegerField()
    text = serializers.CharField(max_length=100)

class SubmissionSerializer(serializers.Serializer):
    'Заполненный опрос'
    id = serializers.IntegerField()
    submitTime = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%S')

