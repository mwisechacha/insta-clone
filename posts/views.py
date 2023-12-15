from django.shortcuts import render, HttpResponse
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet, GenericViewSet
from rest_framework.mixins import RetrieveModelMixin, CreateModelMixin, DestroyModelMixin
from .serializers import PostSerializer, PostImageSerializer, LikeSerializer, CommentSerializer
from .models import Post, PostImage, Like, Comment

# Create your views here.
def index(request):
    return HttpResponse('hello')

class PostViewSet(ModelViewSet):
    queryset = Post.objects.prefetch_related('images').all()
    serializer_class = PostSerializer

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

    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs['post_pk'])
    
    def get_serializer_context(self):
        return {'post_id': self.kwargs['post_pk']}