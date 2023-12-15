from django.shortcuts import render, HttpResponse
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.mixins import RetrieveModelMixin
from .serializers import PostSerializer, PostImageSerializer, LikeSerializer
from .models import Post, PostImage, Like

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
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

    def get_serializer_context(self):
        return {'post_id': self.kwargs['post_pk']}

    def get_queryset(self):
        return Like.objects.filter(post_id=self.kwargs['post_pk'])
