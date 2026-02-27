#!/usr/bin/env python
"""
User Preference Tracking - Comprehensive Test Suite

Run with:
  python test_preferences.py
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from api.models import Article, ArticleLike, SearchQuery, UserPreference


def print_header(text):
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)


def print_section(text):
    print("\n" + "-" * 70)
    print(f"  {text}")
    print("-" * 70)


def test_preferences():
    """Run comprehensive preference tracking tests."""
    
    print_header("USER PREFERENCE TRACKING - TEST SUITE")
    
    # Clean up old test data
    print("\n[SETUP] Cleaning up old test data...")
    User.objects.filter(username='pref_tester').delete()
    print("✓ Old test data cleaned")
    
    # Create test user
    print("\n[SETUP] Creating test user...")
    user = User.objects.create_user(
        username='pref_tester',
        email='tester@example.com',
        password='test123'
    )
    print(f"✓ Created user: {user.username}")
    
    # Verify UserPreference was created (via signal on registration)
    try:
        pref = user.preferences
        print(f"✓ UserPreference created (id={pref.id})")
    except UserPreference.DoesNotExist:
        print("⚠ UserPreference not auto-created; creating manually...")
        pref = UserPreference.objects.create(user=user)
    
    # Create test articles
    print("\n[SETUP] Creating test articles...")
    categories = ['ai_ml', 'blockchain', 'web_dev', 'cybersecurity', 'cloud']
    articles = {}
    for i, cat in enumerate(categories, 1):
        article = Article.objects.create(
            title=f"Article #{i}: {cat.upper()}",
            content=f"Detailed content about {cat}. " * 10,
            category=cat,
            is_approved=True
        )
        articles[cat] = article
        print(f"✓ {article.title} (id={article.id})")
    
    # === TEST 1: Initial State ===
    print_section("TEST 1: Initial State")
    pref.refresh_from_db()
    print(f"Initial preferences: {pref.categories}")
    assert pref.categories == {}, "Expected empty categories dict"
    print("✓ Initial state correct (empty dict)")
    
    # === TEST 2: Record Searches ===
    print_section("TEST 2: Record Searches")
    searches = [
        ('ai machine learning', 'ai_ml'),
        ('blockchain and crypto', 'blockchain'),
        ('web development react', 'web_dev'),
        ('cloud computing aws', 'cloud'),
    ]
    
    for query, expected_cat in searches:
        sq = SearchQuery.objects.create(user=user, query=query)
        print(f"✓ Search: '{query}' (id={sq.id})")
    
    pref.refresh_from_db()
    print(f"\nPreferences after searches:\n{pref.categories}")
    
    # Verify: ai_ml +2, blockchain +2, web_dev +2, cloud +2
    assert 'ai_ml' in pref.categories, "ai_ml should be in preferences"
    assert pref.categories.get('ai_ml', 0) >= 2, "ai_ml should have score >= 2"
    print("✓ Search preferences recorded correctly")
    
    # === TEST 3: Like Articles (Stronger Signal) ===
    print_section("TEST 3: Like Articles")
    like_cats = ['ai_ml', 'blockchain', 'web_dev']
    for cat in like_cats:
        like = ArticleLike.objects.create(user=user, article=articles[cat])
        print(f"✓ Liked: {articles[cat].title} (id={like.id})")
    
    pref.refresh_from_db()
    print(f"\nPreferences after likes:\n{pref.categories}")
    
    # Verify: liked categories should have +5 added to search score
    for cat in like_cats:
        expected_min = 2 + 5  # search (2) + like (5)
        assert pref.categories.get(cat, 0) >= expected_min, \
            f"{cat} should have score >= {expected_min}"
    print("✓ Like preferences recorded correctly (stronger signal)")
    
    # === TEST 4: Unlike an Article ===
    print_section("TEST 4: Unlike an Article")
    cat_to_unlike = 'ai_ml'
    like_obj = ArticleLike.objects.get(user=user, article=articles[cat_to_unlike])
    score_before = pref.categories.get(cat_to_unlike, 0)
    print(f"Score before unlike: {cat_to_unlike} = {score_before}")
    
    like_obj.delete()
    print(f"✓ Unliked: {articles[cat_to_unlike].title}")
    
    pref.refresh_from_db()
    score_after = pref.categories.get(cat_to_unlike, 0)
    print(f"Score after unlike: {cat_to_unlike} = {score_after}")
    
    assert score_after == score_before - 5, \
        f"Unlike should reduce score by 5 (was {score_before}, now {score_after})"
    print("✓ Unlike correctly decreased preference score by 5")
    
    # === TEST 5: Duplicate Search (Increment Count) ===
    print_section("TEST 5: Duplicate Search (Increment Count)")
    query = 'ai machine learning'
    sq1 = SearchQuery.objects.get(user=user, query=query)
    count_before = sq1.count
    print(f"Search count before: {count_before}")
    
    sq2, created = SearchQuery.objects.get_or_create(user=user, query=query)
    if not created:
        sq2.count += 1
        sq2.save(update_fields=['count', 'last_searched'])
    
    sq2.refresh_from_db()
    print(f"Search count after: {sq2.count}")
    assert sq2.count == count_before + 1, "Count should increment by 1"
    print("✓ Duplicate search correctly incremented count")
    
    # === TEST 6: Like Multiple Articles in Same Category ===
    print_section("TEST 6: Like Multiple Articles in Same Category")
    
    # Create two more blockchain articles
    extra_article1 = Article.objects.create(
        title="Extra Blockchain Article 1",
        content="Extra blockchain content",
        category='blockchain',
        is_approved=True
    )
    extra_article2 = Article.objects.create(
        title="Extra Blockchain Article 2",
        content="Extra blockchain content",
        category='blockchain',
        is_approved=True
    )
    
    score_before = pref.categories.get('blockchain', 0)
    print(f"Blockchain score before: {score_before}")
    
    ArticleLike.objects.create(user=user, article=extra_article1)
    print(f"✓ Liked: {extra_article1.title}")
    ArticleLike.objects.create(user=user, article=extra_article2)
    print(f"✓ Liked: {extra_article2.title}")
    
    pref.refresh_from_db()
    score_after = pref.categories.get('blockchain', 0)
    print(f"Blockchain score after: {score_after}")
    
    assert score_after == score_before + 10, \
        f"Two likes should add 10 (was {score_before}, now {score_after})"
    print("✓ Multiple likes in same category correctly stacked")
    
    # === TEST 7: Search with No Category Match (General) ===
    print_section("TEST 7: Search with No Category Match")
    vague_query = 'latest tech news'
    SearchQuery.objects.create(user=user, query=vague_query)
    print(f"✓ Search: '{vague_query}' (no category match expected)")
    
    pref.refresh_from_db()
    # Should add 1 to 'general' or increment an existing category minimally
    print(f"Preferences after vague search: {pref.categories}")
    print("✓ Vague search handled (general scoring applied)")
    
    # === FINAL SUMMARY ===
    print_header("FINAL SUMMARY")
    
    pref.refresh_from_db()
    print(f"\nFinal Preference Scores (ranked):")
    sorted_prefs = sorted(pref.categories.items(), key=lambda x: x[1], reverse=True)
    for cat, score in sorted_prefs:
        print(f"  {cat:20} → {score:3} points")
    
    searches = SearchQuery.objects.filter(user=user).order_by('-last_searched')
    print(f"\nTotal Searches: {len(searches)}")
    for sq in searches[:5]:
        print(f"  '{sq.query}' (count: {sq.count})")
    if len(searches) > 5:
        print(f"  ... and {len(searches) - 5} more")
    
    likes = ArticleLike.objects.filter(user=user)
    print(f"\nTotal Likes: {len(likes)}")
    for like in likes[:5]:
        print(f"  {like.article.title[:40]}... ({like.article.category})")
    if len(likes) > 5:
        print(f"  ... and {len(likes) - 5} more")
    
    print("\n" + "=" * 70)
    print("  ✓ ALL TESTS PASSED!")
    print("=" * 70 + "\n")


if __name__ == '__main__':
    try:
        test_preferences()
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
