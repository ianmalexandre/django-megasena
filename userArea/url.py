from django.urls import include, path, re_path

from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'abc', views.UserModelViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('game/verify/', views.GameVerifyView.as_view(), name='verifyGame'),
    path('game/', views.GamesAPIView.as_view(), name='Game'),
    re_path(r'user/(?P<pk>\d+)?', views.UserAPIViewSet.as_view(), name='User'),
]
