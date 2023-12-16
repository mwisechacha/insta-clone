from django.shortcuts import render
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet
from .serializers import UserSerializer
from .models import Profile

# Create your views here.
class UserViewSet(CreateModelMixin, 
                  RetrieveModelMixin, 
                  UpdateModelMixin, GenericViewSet):
    queryset = Profile.objects.all()
    serializer_class = UserSerializer
