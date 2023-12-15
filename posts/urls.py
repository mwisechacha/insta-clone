from django.urls import path
from django.urls.conf import include
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('posts', views.PostViewSet, basename='posts')

post_router = routers.NestedDefaultRouter(router, 'posts', lookup='post')
post_router.register('images', views.PostImageViewSet, basename='post-images')
post_router.register('likes', views.LikeViewSet, basename='post-likes')
post_router.register('comments', views.CommentViewSet, basename='post-comments')

# URLConf
urlpatterns = router.urls + post_router.urls



