from django.contrib.auth.models import User
from django.core.cache import cache
from django.db.models import Count, Q
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from .models import (
    Article,
    ArticleLike,
    Bookmark,
    ChatMessage,
    SearchQuery,
    UserPreference,
    UserProfile,
)
from .serializers import (
    ArticleSerializer,
    BookmarkSerializer,
    ChatMessageSerializer,
    RegisterSerializer,
    SearchQuerySerializer,
    UserPreferenceSerializer,
    UserProfileSerializer,
)
from .services import AIService, NewsService


@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response(
            {
                "message": "User registered successfully",
                "user": {"id": user.id, "username": user.username, "email": user.email},
            },
            status=status.HTTP_201_CREATED,
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["get", "put", "patch"])
    def me(self, request):
        profile = request.user.profile

        if request.method == "GET":
            serializer = self.get_serializer(profile)
            return Response(serializer.data)

        serializer = self.get_serializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.filter(is_approved=True)
    serializer_class = ArticleSerializer

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

    def get_queryset(self):
        queryset = Article.objects.filter(is_approved=True)
        category = self.request.query_params.get("category")
        source = self.request.query_params.get("source")
        search = self.request.query_params.get("search")

        if category:
            queryset = queryset.filter(category=category)
        if source:
            queryset = queryset.filter(source=source)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(content__icontains=search)
            )

        return queryset

    @action(detail=False, methods=["post"], permission_classes=[IsAuthenticated])
    def record_search(self, request):
        """Record a user's search query to update preferences."""
        query = request.data.get("query", "").strip()
        if not query:
            return Response(
                {"error": "Query is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        sq, created = SearchQuery.objects.get_or_create(user=request.user, query=query)
        if not created:
            # Update existing search: increment count
            sq.count = sq.count + 1
            sq.save(update_fields=["count", "last_searched"])

        serializer = SearchQuerySerializer(sq)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views += 1
        instance.save(update_fields=["views"])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(
        detail=True, methods=["post", "delete"], permission_classes=[IsAuthenticated]
    )
    def like(self, request, pk=None):
        """POST to like an article, DELETE to unlike."""
        article = self.get_object()
        user = request.user
        if request.method == "POST":
            # create like
            try:
                ArticleLike.objects.create(user=user, article=article)
                return Response(
                    {"message": "Liked", "likes_count": article.likes_count},
                    status=status.HTTP_201_CREATED,
                )
            except Exception:
                return Response(
                    {
                        "message": "Already liked or error",
                        "likes_count": article.likes_count,
                    },
                    status=status.HTTP_200_OK,
                )

        # DELETE -> remove like
        try:
            like = ArticleLike.objects.get(user=user, article=article)
            like.delete()
            return Response(
                {"message": "Unliked", "likes_count": article.likes_count},
                status=status.HTTP_200_OK,
            )
        except ArticleLike.DoesNotExist:
            return Response(
                {"error": "Not liked", "likes_count": article.likes_count},
                status=status.HTTP_404_NOT_FOUND,
            )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def summarize(self, request, pk=None):
        article = self.get_object()

        if article.summary:
            return Response({"summary": article.summary})

        ai_service = AIService()
        summary = ai_service.summarize_article(article.content)

        if summary:
            article.summary = summary
            article.save()
            return Response({"summary": summary})

        return Response(
            {"error": "Could not generate summary"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    @action(detail=False, methods=["get"])
    def trending(self, request):
        articles = self.get_queryset().order_by("-views")[:10]
        serializer = self.get_serializer(articles, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["post"], permission_classes=[IsAdminUser])
    def fetch_news(self, request):
        category = request.query_params.get("category", "general")

        news_service = NewsService()
        articles_data = news_service.fetch_news(category)

        created_count = 0
        all_articles = []
        for article_data in articles_data:
            article, created = Article.objects.get_or_create(
                title=article_data["title"],
                defaults={
                    "content": article_data["content"],
                    "source": article_data["source"],
                    "source_url": article_data["source_url"],
                    "image_url": article_data["image_url"],
                    "category": article_data["category"],
                },
            )
            if created:
                created_count += 1
            all_articles.append(article)

        serializer = self.get_serializer(all_articles, many=True)
        return Response(
            {
                "count": created_count,
                "total": len(all_articles),
                "articles": serializer.data,
            }
        )


class BookmarkViewSet(viewsets.ModelViewSet):
    serializer_class = BookmarkSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Bookmark.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=["post"])
    def remove(self, request):
        article_id = request.data.get("article_id")
        try:
            bookmark = Bookmark.objects.get(user=request.user, article_id=article_id)
            bookmark.delete()
            return Response({"message": "Bookmark removed"}, status=status.HTTP_200_OK)
        except Bookmark.DoesNotExist:
            return Response(
                {"error": "Bookmark not found"}, status=status.HTTP_404_NOT_FOUND
            )


class UserPreferenceViewSet(viewsets.ModelViewSet):
    queryset = UserPreference.objects.all()
    serializer_class = UserPreferenceSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["get", "put"])
    def me(self, request):
        preference = request.user.preferences

        if request.method == "GET":
            serializer = self.get_serializer(preference)
            return Response(serializer.data)

        serializer = self.get_serializer(preference, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["get"])
    def top_preferences(self, request):
        """Get user's top 5 preferred categories ranked by score."""
        preference = request.user.preferences

        # Handle both dict (new) and list (legacy) formats
        if isinstance(preference.categories, list):
            preference.categories = {}
            preference.save(update_fields=["categories"])

        # Sort categories by score (descending)
        sorted_prefs = sorted(
            preference.categories.items(), key=lambda x: x[1], reverse=True
        )[
            :5
        ]  # Top 5

        # Format response with category label and score
        category_labels = dict(Article.CATEGORY_CHOICES)
        top_prefs = [
            {
                "category_key": key,
                "category_label": category_labels.get(key, key),
                "score": score,
            }
            for key, score in sorted_prefs
        ]

        return Response(
            {
                "total_categories": len(preference.categories),
                "top_preferences": top_prefs,
            }
        )


@api_view(["GET"])
@permission_classes([IsAdminUser])
def analytics(request):
    cache_key = "analytics_data"
    analytics_data = cache.get(cache_key)

    if not analytics_data:
        analytics_data = {
            "total_articles": Article.objects.count(),
            "total_users": User.objects.count(),
            "total_views": sum(Article.objects.values_list("views", flat=True)),
            "articles_by_category": dict(
                Article.objects.values("category")
                .annotate(count=Count("id"))
                .values_list("category", "count")
            ),
            "top_articles": [
                {"title": article.title, "views": article.views}
                for article in Article.objects.order_by("-views")[:5]
            ],
        }
        cache.set(cache_key, analytics_data, 3600)

    return Response(analytics_data)


class ChatViewSet(viewsets.ModelViewSet):
    serializer_class = ChatMessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ChatMessage.objects.filter(user=self.request.user)

    @action(detail=False, methods=["post"])
    def send_message(self, request):
        """Send a message and get a response from the LLM"""
        try:
            user_message = request.data.get("message", "").strip()

            if not user_message:
                return Response(
                    {"error": "Message cannot be empty"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Save user message
            user_msg = ChatMessage.objects.create(
                user=request.user, role="user", content=user_message
            )

            # Get chat history (last 10 messages)
            history = ChatMessage.objects.filter(user=request.user).order_by(
                "created_at"
            )[:20]

            # Format messages for API
            messages = [{"role": msg.role, "content": msg.content} for msg in history]

            # Add system message for context
            system_message = {
                "role": "system",
                "content": (
                    "You are a helpful AI assistant specialized in technology, news, and articles. "
                    "Provide accurate, informative, and concise responses."
                ),
            }

            # Get response from LLM
            ai_service = AIService()
            assistant_response = ai_service.chat([system_message] + messages)

            if not assistant_response:
                return Response(
                    {"error": "Failed to get response from AI service"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            # Save assistant message
            assistant_msg = ChatMessage.objects.create(
                user=request.user, role="assistant", content=assistant_response
            )

            return Response(
                {
                    "user_message": ChatMessageSerializer(user_msg).data,
                    "assistant_message": ChatMessageSerializer(assistant_msg).data,
                },
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=["get"])
    def history(self, request):
        """Get chat history for the current user"""
        messages = self.get_queryset().order_by("-created_at")[:50]  # Last 50 messages
        serializer = self.get_serializer(messages, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["delete"])
    def clear(self, request):
        """Clear chat history for the current user"""
        deleted_count, _ = ChatMessage.objects.filter(user=request.user).delete()
        return Response(
            {
                "message": f"Deleted {deleted_count} messages",
                "deleted_count": deleted_count,
            }
        )
