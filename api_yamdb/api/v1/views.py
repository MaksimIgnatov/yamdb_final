from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import filters, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import Category, Genre, Review, Title
from users.utils import gen_token_and_send_code

from .filters import TitleFilter
from .mixins import CreateListDestroyViewSet
from .permissions import AdminOrReadOnly, IsAdmin, IsOwnerOrReadOnly
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, GetAuthTokenSerializer,
                          ReviewSerializer, SignUpSerializer,
                          TitleCreateSerializer, TitleReadSerializer,
                          UserProfileSerializer, UserSerializer)

User = get_user_model()


class CategoryViewSet(CreateListDestroyViewSet):
    queryset = Category.objects.all().order_by('id')
    serializer_class = CategorySerializer
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(CreateListDestroyViewSet):
    queryset = Genre.objects.all().order_by('id')
    serializer_class = GenreSerializer
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(ModelViewSet):
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')).order_by('id')
    serializer_class = TitleCreateSerializer
    permission_classes = (AdminOrReadOnly,)
    filter_class = filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update'):
            return TitleCreateSerializer
        return TitleReadSerializer


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        return title.reviews.all().order_by('id')

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly)

    def get_review(self):
        title_id = self.kwargs['title_id']
        review_id = self.kwargs['review_id']
        return get_object_or_404(Review, pk=review_id, title_id=title_id)

    def get_queryset(self):
        return self.get_review().comments.all().order_by('id')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user,
                        review=self.get_review())


class UserViewSet(ModelViewSet):
    """ViewSet модели User."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
    http_method_names = ('get', 'post', 'delete', 'patch')

    @action(
        detail=False,
        methods=('get', 'patch'),
        permission_classes=(IsAuthenticated,),
    )
    def me(self, request):
        serializer = UserProfileSerializer(
            request.user, partial=True, data=request.data
        )
        serializer.is_valid(raise_exception=True)
        if request.method == 'PATCH':
            serializer.save(partial=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([AllowAny])
def signup(request):
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.data["email"]
    username = serializer.data["username"]
    user, _ = User.objects.get_or_create(email=email, username=username)
    user.confirmation_code = gen_token_and_send_code(user)
    user.save()
    return Response(serializer.data, status=status.HTTP_200_OK)


class GetAuthTokenView(APIView):
    """Получение и обновление токена."""

    def post(self, request):
        serializer = GetAuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        confirmation_code = serializer.validated_data.get('confirmation_code')
        user = get_object_or_404(User, username=username)
        if default_token_generator.check_token(user, confirmation_code):
            token = str(AccessToken.for_user(user))
            return Response({'token': token}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
