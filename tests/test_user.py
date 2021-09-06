import requests
import requests
import pytest
from requests.auth import HTTPBasicAuth

from settings import API_URL, ADMIN_USERNAME, ADMIN_PASSWORD

basicAuth = HTTPBasicAuth(ADMIN_PASSWORD, ADMIN_PASSWORD)

textPollData = {
    'poll': {
        'name': 'Text poll',
        'description': 'Test poll with text questions',
        'startDate': '2020-05-01',
        'finishDate': '2020-06-30'
    },
    'questions': [
        {
            'type': 'TEXT',
            'text': 'Your name'
        },
        {
            'type': 'TEXT',
            'text': 'Your age'
        },
        {
            'type': 'TEXT',
            'text': 'Your job'
        },
    ]
}

choicePollData = {
    'poll': {
        'name': 'Choice poll',
        'description': 'Test poll with choice questions',
        'startDate': '2020-05-01',
        'finishDate': '2020-06-30'
    },
    'questions': [
        {
            'type': 'CHOICE',
            'text': 'Choose your gender',
            'options': ['Male', 'Female']
        },
        {
            'type': 'CHOICE',
            'text': 'Choose favourite pony',
            'options': ['Pony', 'Unicorn', 'Pegasus']
        },
        {
            'type': 'MULTIPLE_CHOICE',
            'text': 'Select any colors you like',
            'options': ['White', 'Violet', 'Blue', 'Yellow', 'Pink']
        },
    ]
}

completedPollData = {
    'poll': {
        'name': 'Completed poll',
        'description': 'Finished poll that users should never see',
        'startDate': '2020-01-01',
        'finishDate': '2020-03-30'
    },
    'questions': []
}

def createPoll(pollData):
    res = requests.post(API_URL + '/admin/polls', auth=basicAuth, json=pollData['poll'])
    assert res.status_code == 200
    data = res.json()
    poll_id = data['id']

    for question in pollData['questions']:
        res = requests.post(API_URL + '/admin/polls/%d/questions' % poll_id, auth=basicAuth, json=question)
        assert res.status_code == 200

    return poll_id

def deletePollFinalizer(id):
    def finalizer():
        requests.delete(API_URL + '/admin/polls/%d' % id, auth=basicAuth)
    return finalizer


@pytest.fixture(scope='class')
def textPollId(request):
    id = createPoll(textPollData)
    request.addfinalizer(deletePollFinalizer(id))
    return id

@pytest.fixture(scope='class')
def choicePollId(request):
    id = createPoll(choicePollData)
    request.addfinalizer(deletePollFinalizer(id))
    return id

@pytest.fixture(scope='class')
def completedPollId(request):
    id = createPoll(completedPollData)
    request.addfinalizer(deletePollFinalizer(id))
    return id


USER_ID = 101
OTHER_USER_ID = 102

class TestUser:
    def test_available_polls(self, textPollId, choicePollId, completedPollId):
        res = requests.get(API_URL + '/polls')
        assert res.status_code == 200
        polls = res.json()
        pollIds = [p['id'] for p in polls]
        assert textPollId in pollIds
        assert choicePollId in pollIds
        assert completedPollId not in pollIds

    def test_submit_closed_poll(self, completedPollId):
        res = requests.get(API_URL + '/polls/%d' % completedPollId)
        assert res.status_code == 404

        submitData = {
            'userId': USER_ID,
            'answers': {}
        }
        res = requests.post(API_URL + '/polls/%d' % completedPollId, json=submitData)
        assert res.status_code == 404

    def test_submit_uncomplete_poll(self, textPollId):
        res = requests.get(API_URL + '/polls/%d' % textPollId)
        assert res.status_code == 200
        poll = res.json()

        submitData = {
            'userId': USER_ID,
            'answers': {}
        }
        question = poll['questions'][0]
        submitData['answers'][str(question['id'])] = 'Test'

        res = requests.post(API_URL + '/polls/%d' % textPollId, json=submitData)
        assert res.status_code == 400

    def test_submit_text_poll(self, textPollId):
        res = requests.get(API_URL + '/polls/%d' % textPollId)
        assert res.status_code == 200
        poll = res.json()

        userId = USER_ID
        submitData = {
            'userId': userId,
            'answers': {}
        }
        for question in poll['questions']:
            submitData['answers'][str(question['id'])] = 'User %d answer' % userId

        res = requests.post(API_URL + '/polls/%d' % textPollId, json=submitData)
        assert res.status_code == 200

    def test_duplicated_submit(self, textPollId):
        res = requests.get(API_URL + '/polls/%d' % textPollId)
        assert res.status_code == 200
        poll = res.json()

        userId = USER_ID
        submitData = {
            'userId': userId,
            'answers': {}
        }
        for question in poll['questions']:
            submitData['answers'][str(question['id'])] = 'User %d answer' % userId

        res = requests.post(API_URL + '/polls/%d' % textPollId, json=submitData)
        assert res.status_code == 400

    def test_submit_choice_poll(self, choicePollId):
        res = requests.get(API_URL + '/polls/%d' % choicePollId)
        assert res.status_code == 200
        poll = res.json()

        submitData = {
            'userId': USER_ID,
            'answers': {}
        }
        for question in poll['questions']:
            if question['type'] == 'CHOICE':
                submitData['answers'][str(question['id'])] = 1
            elif question['type'] == 'MULTIPLE_CHOICE':
                submitData['answers'][str(question['id'])] = [1, 2]

        res = requests.post(API_URL + '/polls/%d' % choicePollId, json=submitData)
        assert res.status_code == 200

    def test_submit_text_poll_by_other_user(self, textPollId):
        res = requests.get(API_URL + '/polls/%d' % textPollId)
        assert res.status_code == 200
        poll = res.json()

        userId = OTHER_USER_ID
        submitData = {
            'userId': userId,
            'answers': {}
        }
        for question in poll['questions']:
            submitData['answers'][str(question['id'])] = 'User %d answer' % userId

        res = requests.post(API_URL + '/polls/%d' % textPollId, json=submitData)
        assert res.status_code == 200

    def test_polls_by_user(self, textPollId, choicePollId):
        res = requests.get(API_URL + '/pollsByUser/%d' % USER_ID)
        assert res.status_code == 200
        polls = res.json()
        assert len(polls) >= 2
        pollIds = [p['pollId'] for p in polls]
        assert textPollId in pollIds
        assert choicePollId in pollIds

    def test_polls_by_other_user(self, textPollId):
        res = requests.get(API_URL + '/pollsByUser/%d' % OTHER_USER_ID)
        assert res.status_code == 200
        polls = res.json()
        assert len(polls) >= 1
        pollIds = [p['pollId'] for p in polls]
        assert textPollId in pollIds
