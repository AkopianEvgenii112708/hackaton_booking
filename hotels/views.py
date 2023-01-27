from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions, generics, response
from .models import Hotel
from . import serializers
from .permissions import IsAuthor, IsAuthorOrAdmin, IsAuthorOrAdminOrPostOwner

from rest_framework.response import Response
from .models import Like, Comment
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend


class PostViewSet(ModelViewSet):
    queryset = Hotel.objects.all()
    filter_backends = (SearchFilter, DjangoFilterBackend)
    search_fields = ('title',)
    filterset_fields = ('owner', 'category')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.PostListSerializer
        elif self.action in ('create', 'update', 'partial_update'):
            return serializers.PostCreateSerializer
        return serializers.PostDetailSerializer

    def get_permissions(self):
        # Удалять может только админ или автор поста
        if self.action == 'destroy':
            return [permissions.IsAuthenticated(), IsAuthorOrAdmin()]
        # Обновлять может только автор поста
        elif self.action in ('update', 'partial_update'):
            return [permissions.IsAuthenticated(), IsAuthor()]
        # Просматривать могут все, но создавать только аутентифицированный пользователь
        return [permissions.IsAuthenticatedOrReadOnly()]

        # ../api/v1/posts/id/get_likes/
    @action(['GET'], detail=True)
    def get_likes(self, request, pk):
        post = self.get_object()
        likes = post.likes.all()
        serializer = serializers.LikeSerializer(instance=likes, many=True)
        return Response(serializer.data, status=200)

    # ../api/v1/posts/id/like/
    @action(['POST', 'DELETE'], detail=True)
    def like(self, request, pk):
        post = self.get_object()
        user = request.user
        if request.method == 'POST':
            if user.liked_posts.filter(post=post).exists():
                return Response('This post is already liked!', status=400)
            Like.objects.create(owner=user, post=post)
            return Response('You liked the post!', status=201)
        else:
            if not user.liked_posts.filter(post=post).exists():
                return Response('You didn\'t liked this post!', status=400)
            user.liked_posts.filter(post=post).delete()
            return Response('Your like is deleted!', status=204)


class LikeCreateView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.LikeSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LikeDeleteView(generics.DestroyAPIView):
    queryset = Like.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsAuthor)


class CommentCreateView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer

    def get_permissions(self):
        if self.request.method in ('PUT', 'PATCH'):
            return [permissions.IsAuthenticated(), IsAuthor()]
        elif self.request.method == 'DELETE':
            return [permissions.IsAuthenticated(),
                    IsAuthorOrAdminOrPostOwner()]
        return [permissions.AllowAny()]
