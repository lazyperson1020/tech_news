import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from rest_framework.test import APIClient
from api.models import Article, Bookmark, ArticleLike, UserProfile


def test_get_articles_empty(db):
    client = APIClient()
    response = client.get('/api/articles/')
    assert response.status_code == 200
    assert response.json() == []


def test_article_lifecycle(db):
    client = APIClient()
    # register and login user via API
    reg_resp = client.post('/api/register/', {
        'username': 'tester',
        'email': 't@example.com',
        'password': 'secret123',
        'password2': 'secret123'
    })
    assert reg_resp.status_code == 201

    login_resp = client.post('/api/login/', {'username': 'tester', 'password': 'secret123'})
    assert login_resp.status_code == 200
    token = login_resp.json().get('access')
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    # create article via endpoint
    create_resp = client.post('/api/articles/', {
        'title': 'API article',
        'content': 'Some content',
        'category': 'ai_ml'
    })
    assert create_resp.status_code == 201
    art_id = create_resp.json()['id']

    # retrieve and view counter
    get_resp = client.get(f'/api/articles/{art_id}/')
    assert get_resp.status_code == 200
    assert get_resp.json()['views'] == 1

    # like and unlike
    like_resp = client.post(f'/api/articles/{art_id}/like/')
    assert like_resp.status_code in (200, 201)
    assert 'likes_count' in like_resp.json()

    unlike_resp = client.delete(f'/api/articles/{art_id}/like/')
    assert unlike_resp.status_code == 200

    # record search
    search_resp = client.post('/api/articles/record_search/', {'query': 'django'})
    assert search_resp.status_code == 201
    assert search_resp.json()['query'] == 'django'

    # trending should work
    trend_resp = client.get('/api/articles/trending/')
    assert trend_resp.status_code == 200

    # bookmark article
    bm_resp = client.post('/api/bookmarks/', {'article': art_id})
    assert bm_resp.status_code == 201
    remove_resp = client.post('/api/bookmarks/remove/', {'article_id': art_id})
    assert remove_resp.status_code == 200


def test_profile_and_preferences(db):
    u = User.objects.create_user('me', 'me@example.com', 'pw')
    client = APIClient()
    login = client.post('/api/login/', {'username': 'me', 'password': 'pw'})
    token = login.json().get('access')
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    # get profile
    p = client.get('/api/profiles/me/')
    assert p.status_code == 200

    # update preferences
    pref = client.get('/api/userpreferences/me/')
    assert pref.status_code == 200
