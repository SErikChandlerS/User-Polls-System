from django.urls import include, path
from rest_framework import routers
from main import views as main_views

router = routers.DefaultRouter()
router.register(r'candidate', main_views.CandidateViewSet)

app_name = 'api'
urlpatterns = [
    path('', include(router.urls)),
    path('vote/', main_views.CastVoteView.as_view(), name='vote')
]
