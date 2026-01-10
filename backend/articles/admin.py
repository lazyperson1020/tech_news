from django.contrib import admin
from .models import Article, Category, Bookmark, Comment

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active', 'order']
    list_filter = ['is_active']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'source', 'status', 'is_featured', 'published_at']
    list_filter = ['status', 'source', 'is_featured', 'is_breaking']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['categories']
    date_hierarchy = 'published_at'

@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ['user', 'article', 'created_at']
    search_fields = ['user__username', 'article__title']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'article', 'is_approved', 'created_at']
    list_filter = ['is_approved']
    search_fields = ['user__username', 'content']