
import uuid
import datetime
import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from django.core import management

from polls.models import Poll, Question, Choice


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass


@pytest.fixture(autouse=True)
def initial_data(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        management.call_command('loaddata', 'initial_data.json')


@pytest.fixture
def api_client():
    client = APIClient()
    return client


@pytest.fixture
def admin_api_client():
    client = APIClient()
    client.login(username='Test-Admin', password='1111')
    return client

@pytest.fixture
def poll_data():
    today = datetime.datetime.today()
    start_date = (today - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    end_date = (today + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    return {
        "title": "Test Poll",
        "start_date": start_date,
        "end_date": end_date,
        "description": "Test Poll description",
    }


@pytest.fixture
def poll(poll_data):
    return Poll.objects.create(**poll_data)

@pytest.fixture
def questions_data(poll):
    return (
        {
            "poll": poll.id,
            "text": "Test Poll Text question",
            "type": "TEXT",
            "choices": [
                {"text": "Text 1"},
            ]
        },
        {
            "poll": poll.id,
            "text": "Test Poll Choice question",
            "type": "CHOICE",
            "choices": [
                {"text": "Choice text 1"},
                {"text": "Choice text 2"},
            ]
        },
        {
            "poll": poll.id,
            "text": "Test Poll Multichoice question",
            "type": "MULTICHOICE",
            "choices": [
                {"text": "Choice text 1"},
                {"text": "Choice text 2"},
            ]
        }
    )

@pytest.fixture
def questions(questions_data):
    data = []
    for question in questions_data:
        choices = question.pop('choices')
        question['poll_id'] = question.pop('poll')
        question = Question.objects.create(**question)
        for choice in choices:
            Choice.objects.create(question=question, **choice)
        data.append(question)
    return data


@pytest.fixture
def vote_data(admin_api_client, questions):
    poll_id = None
    answers = []
    for question in questions:
        choices = []
        if question.type in (Question.Type.TEXT, Question.Type.CHOICE):
            choices = [question.choices.first().id]
        elif question.type == Question.Type.MULTICHOICE:
            choices = question.choices.values_list('id', flat=True)

        is_text_question = question.type == Question.Type.TEXT
        for choice in choices:
            answers.append({
                'question_id': question.id,
                'choice_id': choice,
                'value': 'Test value' if is_text_question else None
            })
        poll_id = question.poll.id

    return {
        'poll_id': poll_id,
        'answers': answers
    }
