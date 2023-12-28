from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer, UserSerializer as BaseUserSerializer
from rest_framework import serializers
from .models import Profile

class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name']

class UserProfileSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)
    followers = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    following = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = Profile
        fields = ['id', 'user_id','phone', 'profile_picture', 'birth_date', 'bio', 'pronouns', 'followers', 'following']

class UserSerializer(BaseUserSerializer):
    profile = UserProfileSerializer()
    class Meta(BaseUserSerializer.Meta):
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'profile']

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile')
        profile = instance.profile

        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.save()

        profile.phone = profile_data.get('phone', profile.phone)    
        profile.birth_date = profile_data.get('birth_date', profile.birth_date)
        profile.bio = profile_data.get('bio', profile.bio)
        profile.pronouns = profile_data.get('pronouns', profile.pronouns)
        profile.save()

        return instance
    
