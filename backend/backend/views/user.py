from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from django.http import Http404
from datetime import date
import json

from ..models import Poll, Submission, Answer
from ..serializers import PollSerializer, QuestionSerializer, UserOptionSerializer, SubmissionSerializer


class Polls(APIView):
    def get(self, request):
        today = date.today()
        pollSet = Poll.objects.filter(startDate__lte=today, finishDate__gt=today)
        return Response(PollSerializer(pollSet, many=True).data)


class PollById(APIView):
    def get(self, request, id):
        try:
            today = date.today()
            poll = Poll.objects.get(id=id)
            if poll.startDate > today or poll.finishDate < today:
                raise Poll.DoesNotExist()

            result = PollSerializer(poll).data
            result['questions'] = []
            for question in poll.question_set.all():
                questionDict = QuestionSerializer(question).data
                if question.hasOptionType:
                    questionDict['options'] = UserOptionSerializer(question.option_set.all(), many=True).data
                result['questions'].append(questionDict)
            
            return Response(result)

        except Poll.DoesNotExist:
            raise Http404()
        except Exception as ex:
            raise ParseError(ex)

    def post(self, request, id):
        try:
            today = date.today()
            poll = Poll.objects.get(id=id)
            if poll.startDate > today or poll.finishDate < today:
                raise Poll.DoesNotExist()

            if not 'userId' in request.data:
                raise Exception('userId is missing')
            if not type(request.data['userId']) is int:
                raise Exception('Invalid userId')
            if not 'answers' in request.data:
                raise Exception('answers are missing')
            if not type(request.data['answers']) is dict:
                raise Exception('Invalid answers')

            userId = request.data['userId']
            answerDict = request.data['answers']

            if Submission.objects.filter(userId=userId, poll=poll).count() > 0:
                raise Exception('This user already has submitted to this poll')

            def makeAnswer(question):
                if not str(question.id) in answerDict:
                    raise Exception('Answer to question %d is missing' % question.id)
                
                answerData = answerDict[str(question.id)]
                answer = Answer(
                    question=question,
                    questionType=question.type,
                    questionText=question.text)

                invalidAnswerException = Exception('Invalid answer to question %d' % question.id)
                invalidIndexException = Exception('Invalid option index in answer to question %d' % question.id)
                if question.type == 'TEXT':
                    if not type(answerData) is str:
                        raise invalidAnswerException
                    answer.answerText = answerData

                if question.type == 'CHOICE':
                    if not type(answerData) is int:
                        raise invalidAnswerException
                    foundOption = question.option_set.filter(index=answerData).first()
                    if foundOption:
                        answer.answerText = foundOption.text
                    else:
                        raise invalidIndexException

                if question.type == 'MULTIPLE_CHOICE':
                    if not type(answerData) is list:
                        raise invalidAnswerException
                    optionList = question.option_set.all()
                    resultList = []
                    for index in answerData:
                        foundOption = next((o for o in optionList if o.index == index), None)
                        if foundOption:
                            resultList.append(foundOption.text)
                        else:
                            raise invalidIndexException
                    answer.answerText = json.dumps(resultList)
                
                return answer

            answerList = [makeAnswer(question) for question in poll.question_set.all()]
            if len(answerList) != poll.question_set.count():
                raise Exception('Not enough answers')

            submis = Submission(userId=userId, poll=poll)
            submis.save()
            for answer in answerList:
                answer.submission = submis
                answer.save()

            return Response('Accepted')

        except Poll.DoesNotExist:
            raise Http404()
        except Exception as ex:
            raise ParseError(ex)


class PollsByUser(APIView):
    def get(self, request, id):
        try:
            result = []
            for submission in Submission.objects.filter(userId=id).order_by('submitTime'):
                submissionDict = SubmissionSerializer(submission).data
                submissionDict['pollId'] = submission.poll_id
                submissionDict['answers'] = []
                for answer in submission.answer_set.all():
                    answerText = answer.answerText
                    if answer.questionType == 'MULTIPLE_CHOICE':
                        answerText = json.loads(answerText)
                    
                    submissionDict['answers'].append({
                        'question': {
                            'id': answer.question_id,
                            'type': answer.questionType,
                            'text': answer.questionText
                        },
                        'answer': answerText
                    })

                result.append(submissionDict)

            return Response(result)

        except Exception as ex:
            raise ParseError(ex)
