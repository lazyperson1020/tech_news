from django.urls import path
from .views import FetchNewsView, NewsSourceListView

urlpatterns = [
    path('fetch/', FetchNewsView.as_view(), name='fetch-news'),
    path('sources/', NewsSourceListView.as_view(), name='news-sources'),
]