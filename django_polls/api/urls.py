from django.conf.urls import include, url

from rest_framework import permissions
from rest_framework.routers import DefaultRouter
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


from polls.views import PollViewSet, QuestionViewSet, VoteViewSet

schema_view = get_schema_view(
   openapi.Info(
      title="Poll API",
      default_version='v1',
      description="Fabrique test task"
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

router = DefaultRouter()
router.register(r'polls', PollViewSet)
router.register(r'questions', QuestionViewSet)
router.register(r'votes', VoteViewSet)
#urls
urlpatterns = [
    url(r'^v1/', include((router.urls, 'v1'), namespace='v1')),
    url(
        r'^swagger(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0),
        name='schema-json'
    ),
]
