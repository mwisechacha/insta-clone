from django.shortcuts import render, HttpResponse
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import (PostSerializer, PostImageSerializer, LikeSerializer, 
                          CommentSerializer, UpdatePostSerializer)
from .permissions import IsOwnerOrReadOnly
from .models import Post, PostImage, Like, Comment

# Create your views here.
def index(request):
    return HttpResponse('hello')

class PostViewSet(ModelViewSet):
    queryset = Post.objects.prefetch_related('images').all()
    serializer_class = PostSerializer
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE', 'POST']:
            return [IsAuthenticated(), IsOwnerOrReadOnly()]
        return [IsOwnerOrReadOnly()]
    
    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return UpdatePostSerializer
        return PostSerializer
    

    def get_serializer_context(self):
        return {'request': self.request}

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)
    
        
class PostImageViewSet(ModelViewSet):
    serializer_class = PostImageSerializer

    def get_serializer_context(self):
        return {'post_id': self.kwargs['post_pk']}

    def get_queryset(self):
        return PostImage.objects.filter(post_id=self.kwargs['post_pk'])
    
class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE', 'POST']:
            return [IsAuthenticated(), IsOwnerOrReadOnly()]
        return [IsOwnerOrReadOnly()]

    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs['post_pk'])
    
    def get_serializer_context(self):
        return {'post_id': self.kwargs['post_pk']}
    
    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

class LikeToggleViewSet(ModelViewSet):
    serializer_class = LikeSerializer
    # http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE', 'POST']:
            return [IsAuthenticated(), IsOwnerOrReadOnly()]
        return [IsOwnerOrReadOnly()]

    def get_queryset(self):
        return Like.objects.filter(post_id=self.kwargs['post_pk'])

    def get_serializer_context(self):
        return {'post_id': self.kwargs['post_pk']}

    def create(self, request, *args, **kwargs):
        if self.get_queryset().exists():
            self.get_queryset().delete()
            return Response({'message': 'unliked'}, status=status.HTTP_200_OK)
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=self.request.user)
            return Response({'message': 'liked'}, status=status.HTTP_201_CREATED)
        
    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)
    