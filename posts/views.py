from django.shortcuts import render, HttpResponse
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet, GenericViewSet
from rest_framework.mixins import RetrieveModelMixin, CreateModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import PostSerializer, PostImageSerializer, LikeSerializer, CommentSerializer
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from .models import Post, PostImage, Like, Comment

# Create your views here.
def index(request):
    return HttpResponse('hello')

class PostViewSet(ModelViewSet):
    queryset = Post.objects.prefetch_related('images').all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action == 'update':
            permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['POST'], permission_classes=[IsAuthenticated])
    def like_post(self, request, pk=None):
        post = self.get_object()
        (like, created) = Like.objects.get_or_create(post=post, user=request.user)
        if created:
            post.likes += 1
            post.save()
        serializer = LikeSerializer(like)
        return Response(serializer.data)
    
    @action(detail=True, methods=['POST'], permission_classes=[IsAuthenticated])
    def unlike_post(self, request, pk=None):
        post = self.get_object()
        try:
            like = Like.objects.get(post=post, user=request.user)
            like.delete()
            post.likes -= 1
            post.save()
            return Response(status=204)
        except Like.DoesNotExist:
            return Response(status=404)
        
    @action(detail=True, methods=['POST'], permission_classes=[IsAuthenticated])
    def comment_post(self, request, pk=None):
        post = self.get_object()
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, post=post)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)
        
    @action(detail=True, methods=['POST'], permission_classes=[IsAuthenticated])
    def uncomment_post(self, request, pk=None):
        post = self.get_object()
        try:
            comment = Comment.objects.get(post=post, user=request.user)
            comment.delete()
            return Response(status=204)
        except Comment.DoesNotExist:
            return Response(status=404)
        
class PostImageViewSet(ModelViewSet):
    serializer_class = PostImageSerializer

    def get_serializer_context(self):
        return {'post_id': self.kwargs['post_pk']}

    def get_queryset(self):
        return PostImage.objects.filter(post_id=self.kwargs['post_pk'])
    
class LikeViewSet(ReadOnlyModelViewSet):
    serializer_class = LikeSerializer

    def get_serializer_context(self):
        return {'post_id': self.kwargs['post_pk']}

    def get_queryset(self):
        return Like.objects.filter(post_id=self.kwargs['post_pk'])
    
class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_class = [IsOwnerOrReadOnly]

    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs['post_pk'])
    
    def get_serializer_context(self):
        return {'post_id': self.kwargs['post_pk']}
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)