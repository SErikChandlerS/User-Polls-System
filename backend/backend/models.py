from django.db import models
from django.core import ValidationError


def validateQuestionType(value):
    if not value in ['TEXT', 'CHOICE', 'MULTIPLE_CHOICE']:
        raise ValidationError('Invalid question type')

OPTION_TYPES = ['CHOICE', 'MULTIPLE_CHOICE']


class Poll(models.Model):
    'Опрос'
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    startDate = models.DateField()
    finishDate = models.DateField()

class Question(models.Model):
    'Вопрос'
    poll = models.ForeignKey('Poll', on_delete=models.CASCADE)
    type = models.CharField(max_length=30, validators=[validateQuestionType])
    text = models.CharField(max_length=300)

    @property
    def hasOptionType(self):
        return self.type in OPTION_TYPES

class Option(models.Model):
    'Вариант ответа'
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    index = models.PositiveIntegerField()
    text = models.CharField(max_length=100)

class Submission(models.Model):
    'Заполненный опрос'
    userId = models.IntegerField(db_index=True)
    poll = models.ForeignKey('Poll', on_delete=models.CASCADE)
    submitTime = models.DateTimeField(auto_now_add=True)

# При записи ответа на вопрос мы копируем тип и текст вопроса.
# Также копируется текст вариантов ответа (для соотв. вопросов).
# Это позволит сохранить вопросы и варианты ответов такими, какими они были на момент прохождения опроса.
class Answer(models.Model):
    'Ответ на вопрос'
    submission = models.ForeignKey('Submission', on_delete=models.CASCADE)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    questionType = models.CharField(max_length=30, validators=[validateQuestionType])
    questionText = models.CharField(max_length=300)
    answerText = models.CharField(max_length=300)
    


# Обновить структуру таблиц:
# python manage.py makemigrations backend
# python manage.py migrate
