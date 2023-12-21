from rest_framework import serializers
from .models import Post, PostImage, Like, Comment


class UserField(serializers.Field):
    def to_representation(self, value):
        return value.username if value else None
    
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
    
    username = UserField(source='user')

    class Meta:
        model = Like
        fields = ['id', 'username']

class CommentSerializer(serializers.ModelSerializer):
    username = UserField(source='user')

    def create(self, validated_data):
        post_id = self.context['post_id']
        return Comment.objects.create(post_id=post_id, **validated_data)
    class Meta:
        model = Comment
        fields = ['id', 'body', 'username']

class PostSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    images = PostImageSerializer(many=True, read_only=True)
    liked_by = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True)
    user_id = serializers.IntegerField(read_only=True)

    def get_liked_by(self, obj):
        return obj.liked_users()
    
    class Meta:
        model = Post
        fields = ['id', 'caption', 'images','user_id', 'likes', 'liked_by', 'comments']





