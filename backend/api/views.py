from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend, FilterSet
from django.db.models import Q
from django.contrib.auth.models import User
from service.models import DeviceType, Object, Device
from .serializers import DeviceTypeSerializer, ObjectSerializer, DeviceSerializer, UserSerializer

class DeviceTypeViewSet(viewsets.ModelViewSet):
    queryset = DeviceType.objects.all()
    serializer_class = DeviceTypeSerializer

class ObjectFilter(FilterSet):
    search = filters.CharFilter(method='custom_search', label='Search')
    
    class Meta:
        model = Object
        fields = []
    
    def custom_search(self, queryset, name, value):
        # Экранируем специальные символы regex и добавляем .* для поиска подстроки
        safe_value = value.replace('\\', '\\\\').replace('.', '\.')
        return queryset.filter(
            name__iregex=f'.*{safe_value}.*'
        )

class ObjectViewSet(viewsets.ModelViewSet):
    queryset = Object.objects.all()
    serializer_class = ObjectSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ObjectFilter

    @action(detail=True, methods=['post'])
    def add_device(self, request, pk=None):
        object = self.get_object()
        serializer = DeviceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(object=object)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
    @action(detail=True, methods=['get'])
    def devices(self, request, pk=None):
        obj = self.get_object()
        devices = obj.devices.all()
        serializer = DeviceSerializer(devices, many=True)
        return Response(serializer.data)

class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'model', 'ip', 'object']
    
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer    

    @action(detail=False, methods=['get'], url_path='is-superuser/(?P<username>[^/.]+)')
    def is_superuser(self, request, username=None):
        try:
            user = User.objects.get(username=username)
            return Response({
                'username': username,
                'is_superuser': user.is_superuser,
                'registred': True
            })
        except User.DoesNotExist:
            return Response({
                'username': username,
                'registred': False,
                'error': 'User not found'
            }, status=404)