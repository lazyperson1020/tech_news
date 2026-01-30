from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from api import views

router = DefaultRouter()
router.register(r'articles', views.ArticleViewSet, basename='article')
router.register(r'bookmarks', views.BookmarkViewSet, basename='bookmark')
router.register(r'profiles', views.UserProfileViewSet, basename='profile')
router.register(r'preferences', views.UserPreferenceViewSet, basename='preference')
router.register(r'chat', views.ChatViewSet, basename='chat')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/register/', views.register, name='register'),
    path('api/login/', TokenObtainPairView.as_view(), name='login'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/analytics/', views.analytics, name='analytics'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

