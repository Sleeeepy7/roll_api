
from django.contrib.auth import get_user_model
from django.db import models

import datetime


class Choice(models.Model):
    question = models.ForeignKey(
        'Question', related_name='choices', on_delete=models.CASCADE
    )
    text = models.CharField(max_length=64, default='Enter value')


class Question(models.Model):
    """
    Question model.
    """
    class Type:
        TEXT = 'TEXT'
        CHOICE = 'CHOICE'
        MULTICHOICE = 'MULTICHOICE'

        choices = (
            (TEXT, 'TEXT'),
            (CHOICE, 'CHOICE'),
            (MULTICHOICE, 'MULTICHOICE'),
        )

    poll = models.ForeignKey('Poll', on_delete=models.CASCADE)
    text = models.CharField(max_length=256)
    type = models.CharField(
        max_length=11, choices=Type.choices, default=Type.TEXT
    )


class Poll(models.Model):
    """
    Poll model.
    """
    title = models.CharField(max_length=256)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField(max_length=1024)


class Vote(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, blank=True, null=True)
    date = models.DateField(default=datetime.date.today(), editable=False)


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    vote = models.ForeignKey(Vote, related_name='answers', on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    value = models.CharField(max_length=128, blank=True, null=True)
