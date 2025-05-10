from propylon_document_manager.file_versions.models import FileVersion
from .factories import UserFactory

def test_file_versions():
    file_name = "new_file"
    file_version = 1
    owner = UserFactory()
    FileVersion.objects.create(
        file_name=file_name,
        version_number=file_version,
        owner=owner
    )
    files = FileVersion.objects.all()
    assert files.count() == 1
    assert files[0].file_name == file_name
    assert files[0].version_number == file_version
