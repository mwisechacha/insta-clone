from rest_framework_nested import routers
from django.conf.urls import include
from . import views

router = routers.DefaultRouter()
router.register('users', views.UserViewSet, basename='user-details')

# URLConf
urlpatterns = router.urls

