
import django_filters
from .models import Vote

class VoteFilter(django_filters.FilterSet):

    class Meta:
        model = Vote
        fields = {
            'user': ['exact', 'isnull'],
            'poll': ['exact'],
        }
