from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from .tasks import fetch_news_from_all_sources
from .models import NewsSource

class FetchNewsView(APIView):
    permission_classes = [permissions.IsAdminUser]
    
    def post(self, request):
        """Trigger news fetching from all sources"""
        fetch_news_from_all_sources.delay()
        return Response({'message': 'News fetching initiated'}, status=status.HTTP_202_ACCEPTED)


class NewsSourceListView(APIView):
    permission_classes = [permissions.IsAdminUser]
    
    def get(self, request):
        """List all news sources"""
        sources = NewsSource.objects.all()
        data = [{
            'id': source.id,
            'name': source.name,
            'api_type': source.api_type,
            'is_active': source.is_active,
            'last_fetch': source.last_fetch
        } for source in sources]
        return Response(data)