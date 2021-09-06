import requests
from requests.auth import HTTPBasicAuth

from settings import API_URL, ADMIN_USERNAME, ADMIN_PASSWORD

basicAuth = HTTPBasicAuth(ADMIN_PASSWORD, ADMIN_PASSWORD)


class TestAdmin:
    pollId = None

    def get_first_poll(self):
        res = requests.get(API_URL + '/admin/polls', auth=basicAuth)
        assert res.status_code == 200
        data = res.json()
        return data[0]['id']

    def test_no_auth(self):
        res = requests.get(API_URL + '/admin/polls')
        assert res.status_code == 401

    def test_auth(self):
        res = requests.get(API_URL + '/admin/polls', auth=basicAuth)
        assert res.status_code == 200
        data = res.json()
        assert type(data) is list

    def test_create_poll(self):
        poll = {
            'name': 'Test',
            'description': 'Test description',
            'startDate': '2020-05-01',
            'finishDate': '2020-06-30'
        }
        res = requests.post(API_URL + '/admin/polls', auth=basicAuth, json=poll)
        assert res.status_code == 200
        data = res.json()
        TestAdmin.pollId = data['id']

    def test_create_poll_with_invalid_dates(self):
        poll = {
            'name': 'Test invalid dates',
            'description': 'Test description',
            'startDate': '2020-05-01',
            'finishDate': '2020-03-01'
        }
        res = requests.post(API_URL + '/admin/polls', auth=basicAuth, json=poll)
        assert res.status_code == 400

    def test_poll_by_id(self):
        res = requests.get(API_URL + '/admin/polls/%d' % TestAdmin.pollId, auth=basicAuth)
        assert res.status_code == 200
        data = res.json()
        assert data['id'] == TestAdmin.pollId

    def test_poll_by_invalid_id(self):
        id = 98765
        res = requests.get(API_URL + '/admin/polls/%d' % id, auth=basicAuth)
        assert res.status_code == 404

    def test_edit_poll(self):
        res = requests.get(API_URL + '/admin/polls/%d' % TestAdmin.pollId, auth=basicAuth)
        assert res.status_code == 200
        prevPoll = res.json()

        edit = {
            'name': 'Test edited',
            'description': 'Description updated',
            'finishDate': '2020-07-20'            
        }
        res = requests.patch(API_URL + '/admin/polls/%d' % TestAdmin.pollId, auth=basicAuth, json=edit)
        assert res.status_code == 200
        updatedPoll = res.json()
        assert prevPoll['id'] == updatedPoll['id']
        assert prevPoll['name'] != updatedPoll['name']
        assert prevPoll['description'] != updatedPoll['description']
        assert prevPoll['finishDate'] != updatedPoll['finishDate']

    def test_edit_poll_start_date(self):
        res = requests.get(API_URL + '/admin/polls/%d' % TestAdmin.pollId, auth=basicAuth)
        assert res.status_code == 200
        prevPoll = res.json()

        edit = {
            'startDate': '2020-04-01'
        }
        res = requests.patch(API_URL + '/admin/polls/%d' % TestAdmin.pollId, auth=basicAuth, json=edit)
        assert res.status_code == 200
        updatedPoll = res.json()
        assert prevPoll['startDate'] == updatedPoll['startDate']

    def test_delete_poll(self):
        res = requests.delete(API_URL + '/admin/polls/%d' % TestAdmin.pollId, auth=basicAuth)
        assert res.status_code == 200
        TestAdmin.pollId = None

    def test_delete_nonexistent_poll(self):
        id = 98765
        res = requests.delete(API_URL + '/admin/polls/%d' % id, auth=basicAuth)
        assert res.status_code == 404

