
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DeviceTypeViewSet, ObjectViewSet, DeviceViewSet, UserViewSet #ObjectDevicesView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


router = DefaultRouter()
router.register(r'device-types', DeviceTypeViewSet)
router.register(r'objects', ObjectViewSet)
router.register(r'devices', DeviceViewSet)
router.register(r'users', UserViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]