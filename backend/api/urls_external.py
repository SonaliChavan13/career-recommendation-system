from django.urls import path
from .views_external import *

urlpatterns = [
    path('external/jobs/', ExternalJobDataView.as_view(), name='external_jobs'),
    path('external/trends/', MarketTrendsView.as_view(), name='market_trends'),
    path('external/skill-demand/', SkillDemandView.as_view(), name='skill_demand'),
]