from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HIRADocumentViewSet, HIRAGroupViewSet, HIRAActivityViewSet

router = DefaultRouter()
router.register(r'documents', HIRADocumentViewSet, basename='hira-document')
router.register(r'groups', HIRAGroupViewSet, basename='hira-group')
router.register(r'activities', HIRAActivityViewSet, basename='hira-activity')

urlpatterns = [
    path('', include(router.urls)),
]