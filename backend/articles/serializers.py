from rest_framework import serializers
from .models import Article, Category, Bookmark, Comment
from users.serializer import UserSerializer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'icon', 'order']
        read_only_fields = ['id']


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Comment
        fields = ['id', 'article', 'user', 'parent', 'content', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']


class ArticleSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    categories = CategorySerializer(many=True, read_only=True)
    category_ids = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        write_only=True,
        many=True,
        required=False,
        source='categories'
    )
    comments = CommentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Article
        fields = [
            'id', 'slug', 'title', 'content', 'excerpt', 'summary',
            'author', 'source', 'source_name', 'source_url',
            'featured_image', 'featured_image_caption',
            'categories', 'category_ids', 'tags',
            'status', 'is_featured', 'is_breaking',
            'views_count', 'likes_count', 'bookmarks_count', 'shares_count',
            'published_at', 'created_at', 'updated_at', 'comments'
        ]
        read_only_fields = [
            'id', 'slug', 'author', 'views_count', 'likes_count',
            'bookmarks_count', 'shares_count', 'created_at', 'updated_at'
        ]

    def create(self, validated_data):
        categories = validated_data.pop('categories', [])
        article = Article.objects.create(**validated_data)
        article.categories.set(categories)
        return article

    def update(self, instance, validated_data):
        categories = validated_data.pop('categories', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if categories is not None:
            instance.categories.set(categories)
        return instance


class BookmarkSerializer(serializers.ModelSerializer):
    article = ArticleSerializer(read_only=True)
    article_id = serializers.IntegerField(write_only=True, source='article.id')
    
    class Meta:
        model = Bookmark
        fields = ['id', 'article', 'article_id', 'notes', 'created_at']
        read_only_fields = ['id', 'article', 'created_at']
