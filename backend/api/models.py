from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    bio = models.TextField(blank=True, null=True)
    h_index = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    credentials = models.CharField(max_length=255, blank=True, null=True)
    experience = models.TextField(blank=True, null=True)
    profile_picture = models.FileField(
        upload_to="profiles/", blank=True, null=True
    )  # Use FileField instead of ImageField
    is_author = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    class Meta:
        ordering = ["-created_at"]


class Article(models.Model):
    SOURCE_CHOICES = [
        ("newsapi", "NewsAPI"),
        ("tavily", "Tavily"),
        ("user", "User Generated"),
    ]

    CATEGORY_CHOICES = [
        ("ai_ml", "AI/ML"),
        ("blockchain", "Blockchain"),
        ("web_dev", "Web Development"),
        ("app_dev", "App Development"),
        ("cybersecurity", "Cybersecurity"),
        ("cloud", "Cloud Computing"),
        ("general", "General Tech"),
    ]

    title = models.CharField(max_length=500)
    content = models.TextField()
    summary = models.TextField(blank=True, null=True)
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="articles"
    )
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES, default="newsapi")
    source_url = models.URLField(max_length=1000, blank=True, null=True)
    image_url = models.URLField(max_length=1000, blank=True, null=True)
    category = models.CharField(
        max_length=20, choices=CATEGORY_CHOICES, default="general"
    )
    is_approved = models.BooleanField(default=True)
    views = models.IntegerField(default=0)
    published_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-published_at"]
        indexes = [
            models.Index(fields=["-published_at"]),
            models.Index(fields=["category"]),
        ]

    def __str__(self):
        return self.title

    @property
    def likes_count(self):
        """Get the total number of likes for this article."""
        return self.likes.count()


class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookmarks")
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name="bookmarks"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "article")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} bookmarked {self.article.title}"


class UserPreference(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="preferences"
    )
    # store category preference scores as a mapping: {category_key: score}
    categories = models.JSONField(default=dict)
    notification_enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Preferences"

    class Meta:
        verbose_name_plural = "User Preferences"

    def increment_category(self, category_key: str, value: int = 1):
        """Increment the preference score for a category and save.

        Creates the category key if missing.
        """
        if not isinstance(self.categories, dict):
            self.categories = {}
        self.categories[category_key] = int(self.categories.get(category_key, 0)) + int(
            value
        )
        # keep only non-negative scores
        if self.categories.get(category_key, 0) <= 0:
            self.categories.pop(category_key, None)
        self.save(update_fields=["categories", "updated_at"])


class ChatMessage(models.Model):
    ROLE_CHOICES = [
        ("user", "User"),
        ("assistant", "Assistant"),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="chat_messages"
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]
        indexes = [
            models.Index(fields=["user", "-created_at"]),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.role}: {self.content[:50]}"


class ArticleLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "article")

    def __str__(self):
        return f"{self.user.username} liked {self.article.title}"


class SearchQuery(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="searches")
    query = models.CharField(max_length=500)
    count = models.IntegerField(default=1)
    last_searched = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [models.Index(fields=["user", "-last_searched"])]

    def __str__(self):
        return f"{self.user.username} searched: {self.query} ({self.count})"


# Signals: update preference scores on like or search


@receiver(post_save, sender=ArticleLike)
def handle_article_like(sender, instance, created, **kwargs):
    if not created:
        return
    # boost the category score when a user likes an article
    pref, _ = UserPreference.objects.get_or_create(user=instance.user)
    category = instance.article.category or "general"
    # liking is a stronger signal
    pref.increment_category(category, value=5)


@receiver(post_delete, sender=ArticleLike)
def handle_article_unlike(sender, instance, **kwargs):
    # reduce the category score when user unlikes
    try:
        pref = instance.user.preferences
        category = instance.article.category or "general"
        pref.increment_category(category, value=-5)
    except UserPreference.DoesNotExist:
        pass


@receiver(post_save, sender=SearchQuery)
def handle_search_query(sender, instance, created, **kwargs):
    # Only process on initial creation; skip updates to avoid recursion
    if not created:
        return

    # improved keyword matching against categories
    pref, _ = UserPreference.objects.get_or_create(user=instance.user)
    q = (instance.query or "").lower()

    # mapping of category keys to keywords/synonyms
    category_keywords = {
        "ai_ml": [
            "ai",
            "artificial intelligence",
            "machine learning",
            "neural",
            "transformer",
            "llm",
            "gpt",
        ],
        "blockchain": [
            "blockchain",
            "bitcoin",
            "ethereum",
            "crypto",
            "web3",
            "nft",
            "defi",
            "smart contract",
        ],
        "web_dev": [
            "web",
            "react",
            "vue",
            "angular",
            "javascript",
            "html",
            "css",
            "frontend",
            "backend",
            "nodejs",
        ],
        "app_dev": [
            "app",
            "mobile",
            "ios",
            "android",
            "flutter",
            "react native",
            "swift",
        ],
        "cybersecurity": [
            "security",
            "cybersecurity",
            "hacking",
            "exploit",
            "vulnerability",
            "penetration",
            "encryption",
        ],
        "cloud": [
            "cloud",
            "aws",
            "azure",
            "gcp",
            "serverless",
            "kubernetes",
            "docker",
            "container",
        ],
        "general": ["tech", "technology", "software", "programming", "development"],
    }

    matched = False
    for category, keywords in category_keywords.items():
        for keyword in keywords:
            if keyword in q:
                pref.increment_category(category, value=2)
                matched = True
                break

    # if no category matched, increment general
    if not matched:
        pref.increment_category("general", value=1)
