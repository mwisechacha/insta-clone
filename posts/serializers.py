from rest_framework import serializers
from .models import Post, PostImage, Like



class PostImageSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        post_id = self.context['post_id']
        return PostImage.objects.create(post_id=post_id, **validated_data)
    class Meta:
        model = PostImage
        fields = ['id', 'image']

class LikeSerializer(serializers.ModelSerializer):
    def create(self, validate_data):
        post_id = self.context['post_id']
        return Like.objects.create(post_id=post_id, **validate_data)
    class Meta:
        model = Like
        fields = ['id', 'user']

class PostSerializer(serializers.ModelSerializer):
    images = PostImageSerializer(many=True, read_only=True)
    liked_by = serializers.SerializerMethodField()

    def get_liked_by(self, obj):
        return obj.liked_users()
    class Meta:
        model = Post
        fields = ['id', 'caption', 'images','user', 'likes', 'liked_by']



