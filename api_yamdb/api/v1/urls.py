from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    GetAuthTokenView, ReviewViewSet, TitleViewSet, UserViewSet,
                    signup)

v1_router = DefaultRouter()

v1_router.register('categories', CategoryViewSet, basename='categories')
v1_router.register('genres', GenreViewSet, basename='genres')
v1_router.register('titles', TitleViewSet, basename='titles')
v1_router.register(r'titles/(?P<title_id>\d+)/reviews',
                   ReviewViewSet,
                   basename='reviews')
v1_router.register((r'titles/(?P<title_id>\d+)/reviews/'
                    r'(?P<review_id>\d+)/comments'),
                   CommentViewSet,
                   basename='comments')
v1_router.register('users', UserViewSet)


urlpatterns = [
    path('auth/signup/', signup, name='sign_up'),
    path('auth/token/', GetAuthTokenView.as_view(), name='get_token'),
    path('', include(v1_router.urls)),
]
