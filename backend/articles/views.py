from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone

from .models import Article, Category, Bookmark, Comment
from .serializers import (
    ArticleSerializer,
    CategorySerializer,
    BookmarkSerializer,
    CommentSerializer
)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """Viewset for technology categories"""
    queryset = Category.objects.filter(is_active=True).order_by('order')
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['order', 'name']


class ArticleViewSet(viewsets.ModelViewSet):
    """Viewset for article management"""
    queryset = Article.objects.filter(status='published').order_by('-published_at')
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_fields = ['categories', 'source', 'is_featured', 'is_breaking']
    search_fields = ['title', 'content', 'summary', 'tags']
    ordering_fields = ['published_at', 'views_count', 'likes_count']
    lookup_field = 'slug'

    def get_queryset(self):
        """Filter based on user permissions"""
        if self.request.user.is_authenticated:
            # Show draft articles only to their authors and staff
            if self.request.user.is_staff:
                return Article.objects.all().order_by('-published_at')
            return Article.objects.filter(
                status__in=['published', 'featured']
            ).order_by('-published_at')
        return super().get_queryset()

    def perform_create(self, serializer):
        """Set author on creation"""
        serializer.save(author=self.request.user)

    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured articles"""
        featured = Article.objects.filter(
            status='published',
            is_featured=True
        ).order_by('-published_at')[:5]
        serializer = self.get_serializer(featured, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def trending(self, request):
        """Get trending articles by views"""
        trending = Article.objects.filter(
            status='published'
        ).order_by('-views_count')[:10]
        serializer = self.get_serializer(trending, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def like(self, request, slug=None):
        """Like an article"""
        article = self.get_object()
        article.likes_count += 1
        article.save()
        return Response({
            'message': 'Article liked',
            'likes_count': article.likes_count
        })

    @action(detail=True, methods=['post'])
    def unlike(self, request, slug=None):
        """Unlike an article"""
        article = self.get_object()
        if article.likes_count > 0:
            article.likes_count -= 1
            article.save()
        return Response({
            'message': 'Article unliked',
            'likes_count': article.likes_count
        })

    @action(detail=True, methods=['post'])
    def view(self, request, slug=None):
        """Track article view"""
        article = self.get_object()
        article.views_count += 1
        article.save()
        return Response({
            'message': 'View recorded',
            'views_count': article.views_count
        })

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def generate_summary(self, request, slug=None):
        """Generate AI summary for article"""
        article = self.get_object()
        
        # If summary already exists, return it
        if article.summary:
            return Response({
                'summary': article.summary,
                'message': 'Summary already generated'
            })
        
        # Here you would call your AI service
        # For now, return a placeholder
        summary = f"This is an AI-generated summary of: {article.title[:50]}..."
        article.summary = summary
        article.save()
        
        return Response({
            'summary': article.summary,
            'message': 'Summary generated'
        })


class BookmarkViewSet(viewsets.ModelViewSet):
    """Viewset for user bookmarks"""
    serializer_class = BookmarkSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at']

    def get_queryset(self):
        """Get bookmarks for current user only"""
        return Bookmark.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Set user on creation"""
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def my_bookmarks(self, request):
        """Get all bookmarks for current user"""
        bookmarks = self.get_queryset().order_by('-created_at')
        serializer = self.get_serializer(bookmarks, many=True)
        return Response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    """Viewset for article comments"""
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['article']
    ordering_fields = ['created_at']

    def get_queryset(self):
        """Get only approved comments"""
        return Comment.objects.filter(is_approved=True).order_by('-created_at')

    def perform_create(self, serializer):
        """Set user on creation"""
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def pending(self, request):
        """Get pending comments (for moderators)"""
        if not request.user.is_staff:
            return Response(
                {'error': 'Permission denied'},
                status=status.HTTP_403_FORBIDDEN
            )
        pending = Comment.objects.filter(is_approved=False)
        serializer = self.get_serializer(pending, many=True)
        return Response(serializer.data)
