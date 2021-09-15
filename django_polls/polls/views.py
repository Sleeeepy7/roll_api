import datetime
import logging

from rest_framework import viewsets, decorators, response

from django_filters.rest_framework import DjangoFilterBackend


from .models import Poll, Question, Vote
from .serializers import PollSerializer, QuestionSerializer, VoteSerializer
from .filters import VoteFilter
from .permissions import PollPermission, QuestionPermission


logger = logging.getLogger(__name__)


class PollViewSet(viewsets.ModelViewSet):
    """
    REST API for polls.
    """
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    permission_classes = (PollPermission, )


class QuestionViewSet(viewsets.ModelViewSet):
    """
    REST API for poll questions.
    """
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = (QuestionPermission, )


class VoteViewSet(viewsets.ModelViewSet):
    """
    REST API for votes on poll.
    """
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    filter_backends = (DjangoFilterBackend, )
    http_method_names = ('get', 'post')
    filterset_class = VoteFilter

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            return serializer.save(user=self.request.user)

        return super().perform_create(serializer)
