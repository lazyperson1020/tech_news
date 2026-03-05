from django.contrib import admin

from .models import Article, Bookmark, ChatMessage, UserPreference, UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "is_author", "h_index", "created_at")
    list_filter = ("is_author", "created_at")
    search_fields = ("user__username", "credentials")


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "author",
        "source",
        "category",
        "is_approved",
        "views",
        "published_at",
    )
    list_filter = ("category", "source", "is_approved", "published_at")
    search_fields = ("title", "content")
    readonly_fields = ("views", "published_at", "updated_at")


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ("user", "article", "created_at")
    list_filter = ("created_at",)
    search_fields = ("user__username", "article__title")


@admin.register(UserPreference)
class UserPreferenceAdmin(admin.ModelAdmin):
    list_display = ("user", "notification_enabled", "created_at")
    list_filter = ("notification_enabled", "created_at")
    search_fields = ("user__username",)


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "content_preview", "created_at")
    list_filter = ("role", "created_at", "user")
    search_fields = ("user__username", "content")
    readonly_fields = ("created_at",)

    def content_preview(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content

    content_preview.short_description = "Content"
