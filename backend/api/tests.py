from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient

from .models import Article


class ArticleTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            "testuser", "test@example.com", "password123"
        )

    def test_create_article(self):
        article = Article.objects.create(
            title="Test Article",
            content="Test content",
            category="ai_ml",
            author=self.user,
        )
        self.assertEqual(article.title, "Test Article")
        self.assertEqual(article.views, 0)

    def test_get_articles(self):
        Article.objects.create(title="Article 1", content="Content 1", category="ai_ml")
        response = self.client.get("/api/articles/")
        self.assertEqual(response.status_code, 200)


class UserTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_register_user(self):
        data = {
            "username": "newuser",
            "email": "new@example.com",
            "password": "securepass123",
            "password2": "securepass123",
        }
        response = self.client.post("/api/register/", data)
        self.assertEqual(response.status_code, 201)
