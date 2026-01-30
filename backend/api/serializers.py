from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, Article, Bookmark, UserPreference, ChatMessage

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_staff']
        read_only_fields = ['id', 'is_staff']

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'bio', 'h_index', 'credentials', 'experience', 
                  'profile_picture', 'is_author', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True, min_length=8)
    is_author = serializers.BooleanField(default=False)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'first_name', 'last_name', 'is_author']
    
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords don't match")
        return data
    
    def create(self, validated_data):
        validated_data.pop('password2')
        is_author = validated_data.pop('is_author', False)
        
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        
        UserProfile.objects.create(user=user, is_author=is_author)
        UserPreference.objects.create(user=user)
        
        return user

class ArticleSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)
    is_bookmarked = serializers.SerializerMethodField()
    
    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'summary', 'author', 'author_name', 
                  'source', 'source_url', 'image_url', 'category', 'is_approved', 
                  'views', 'published_at', 'updated_at', 'is_bookmarked']
        read_only_fields = ['id', 'views', 'published_at', 'updated_at', 'author']
    
    def get_is_bookmarked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Bookmark.objects.filter(user=request.user, article=obj).exists()
        return False

class BookmarkSerializer(serializers.ModelSerializer):
    article = ArticleSerializer(read_only=True)
    article_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Bookmark
        fields = ['id', 'article', 'article_id', 'created_at']
        read_only_fields = ['id', 'article', 'created_at']
    
    def create(self, validated_data):
        article_id = validated_data.pop('article_id')
        validated_data['article_id'] = article_id
        return super().create(validated_data)

class UserPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPreference
        fields = ['id', 'categories', 'notification_enabled', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ['id', 'role', 'content', 'created_at']
        read_only_fields = ['id', 'created_at']

