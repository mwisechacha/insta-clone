from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from .serializers import UserProfileSerializer, UserSerializer
from .models import Profile
from .permissions import IsOwnerOrReadOnly

# Create your views here.
class UserViewSet(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAdminUser]
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE', 'POST']:
            return [IsOwnerOrReadOnly()]
        return [IsAuthenticated()]


    def get_serializer_class(self):
        if self.action == 'me':
            return UserProfileSerializer
        return super().get_serializer_class()
    
    # def retrieve(self, request, *args, **kwargs):
    #     self.permission_classes = [IsAuthenticated]
    #     return super().retrieve(request, *args, **kwargs)


    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
    def me(self, request):
        (user, created) = Profile.objects.get_or_create(user=request.user)
        if request.method == 'GET':
            serializer = UserProfileSerializer(user)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = UserProfileSerializer(user, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            print(serializer.data)
            return Response(serializer.data)
        
    @action(detail=True, methods=['POST'], permission_classes=[IsAuthenticated])
    def follow(self, request, pk=None):
        user_to_follow = self.get_object()
        current_user = Profile.objects.get(user=request.user)

        if user_to_follow.user != request.user:
            user_to_follow.followers.add(current_user.user)
            current_user.following.add(user_to_follow.user)
            return Response({'message': 'followed'}, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'Cannot follow yourself'}, status=status.HTTP_400_BAD_REQUEST)
        

    @action(detail=True, methods=['POST'], permission_classes=[IsAuthenticated])
    def unfollow(self, request, pk=None):
        user_to_unfollow = self.get_object()
        current_user = Profile.objects.get(user=request.user)

        if user_to_unfollow.user != request.user:
            user_to_unfollow.followers.remove(current_user.user)
            current_user.following.remove(user_to_unfollow.user)
            return Response({'message': 'unfollowed'}, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'Cannot unfollow yourself'}, status=status.HTTP_400_BAD_REQUEST)