from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WorkPermitViewSet

router = DefaultRouter()
router.register(r'', WorkPermitViewSet, basename='work-permit')

urlpatterns = [
    path('', include(router.urls)),
]