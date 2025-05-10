from django.shortcuts import render

from rest_framework.mixins import RetrieveModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action

from ..models import FileVersion
from .serializers import FileVersionSerializer

# class FileVersionViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
#     authentication_classes = []
#     permission_classes = []
#     serializer_class = FileVersionSerializer
#     queryset = FileVersion.objects.all()
#     lookup_field = "id"

class FileVersionViewSet(viewsets.ModelViewSet):
    serializer_class = FileVersionSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = FileVersion.objects.all()

    def get_queryset(self):
        # Only return files owned by the authenticated user
        return FileVersion.objects.filter(owner=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    
    @action(detail=False, methods=['get'])
    def by_path(self, request):
        path = request.query_params.get('path')
        version = request.query_params.get('version')
        if not path:
            return Response({'detail': 'path is required'}, status=status.HTTP_400_BAD_REQUEST)
        qs = FileVersion.objects.filter(owner=request.user, path=path)
        if version is not None:
            qs = qs.filter(version_number=version)
        else:
            qs = qs.order_by('-version_number')
        file_version = qs.first()
        if not file_version:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(file_version)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='by_hash/(?P<content_hash>[0-9a-fA-F]{64})')
    def by_hash(self, request, content_hash=None):
        file_version = FileVersion.objects.filter(owner=request.user, content_hash=content_hash).first()
        if not file_version:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(file_version)
        return Response(serializer.data)
