from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from .serializers import UserProfileSerializer
from .models import Profile

# Create your views here.
class UserViewSet(CreateModelMixin, 
                  RetrieveModelMixin, 
                  UpdateModelMixin, GenericViewSet):
    queryset = Profile.objects.all()
    serializer_class = UserProfileSerializer

    @action(detail=False)
    def me(self, request):
        user = Profile.objects.get(user=request.user.id)
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)
