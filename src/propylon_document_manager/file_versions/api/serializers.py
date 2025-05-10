from rest_framework import serializers

from ..models import FileVersion

class FileVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileVersion
        fields = ['id', 'file_name', 'version_number', 'file', 'path', 'created_at', 'content_hash']
        read_only_fields = ['id', 'created_at', 'version_number', 'file_name', 'content_hash']

    def create(self, validated_data):
        user = self.context['request'].user
        path = validated_data['path']
        file_name = validated_data['file'].name

        validated_data.pop('owner', None)

        # Find the latest version number for this user/path
        latest = FileVersion.objects.filter(owner=user, path=path).order_by('-version_number').first()
        version_number = (latest.version_number + 1) if latest else 1

        return FileVersion.objects.create(
            owner=user,
            file_name=file_name,
            version_number=version_number,
            **validated_data
        )
