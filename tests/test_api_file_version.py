import pytest
import io
from rest_framework.test import APIClient
from .factories import UserFactory

@pytest.mark.django_db
def test_auth_required():
    client = APIClient()
    response = client.get("/api/file_versions/")
    assert response.status_code == 401

@pytest.mark.django_db
def test_file_upload_and_list(user):
    client = APIClient()
    client.force_authenticate(user=user)
    with open(__file__, "rb") as f:
        response = client.post(
            "/api/file_versions/",
            {"file": f, "path": "/documents/test/file.py"},
            format="multipart"
        )
    assert response.status_code == 201
    data = response.json()
    assert data["file_name"] == "test_api_file_version.py"
    response = client.get("/api/file_versions/")
    assert response.status_code == 200
    assert len(response.json()) == 1

@pytest.mark.django_db
def test_file_versioning(user):
    client = APIClient()
    client.force_authenticate(user=user)
    path = "/documents/test/file.txt"
    for i in range(3):
        with open(__file__, "rb") as f:
            client.post(
                "/api/file_versions/",
                {"file": f, "path": path},
                format="multipart"
            )
    response = client.get("/api/file_versions/")
    assert len(response.json()) == 3
    # check version numbers
    versions = [fv["version_number"] for fv in response.json()]
    assert sorted(versions) == [1, 2, 3]

@pytest.mark.django_db
def test_file_access_control(user):
    client = APIClient()
    client.force_authenticate(user=user)
    with open(__file__, "rb") as f:
        client.post(
            "/api/file_versions/",
            {"file": f, "path": "/documents/secret/file.py"},
            format="multipart"
        )
    # another user should not see this file
    other_user = UserFactory()
    client.force_authenticate(user=other_user)
    response = client.get("/api/file_versions/")
    assert len(response.json()) == 0

@pytest.mark.django_db
def test_fetch_specific_version(user):
    client = APIClient()
    client.force_authenticate(user=user)
    path = "/documents/test/versioned.txt"
    # upload two versions
    for content in [b"first", b"second"]:
        f = io.BytesIO(content)
        f.name = "versioned.txt"
        client.post(
            "/api/file_versions/",
            {"file": f, "path": path},
            format="multipart"
        )
    # fetch first version
    response = client.get(f"/api/file_versions/by_path/?path={path}&version=1")
    assert response.status_code == 200
    assert response.json()["version_number"] == 1
    # fetch second version
    response = client.get(f"/api/file_versions/by_path/?path={path}&version=2")
    assert response.status_code == 200
    assert response.json()["version_number"] == 2

@pytest.mark.django_db
def test_unauthenticated_cannot_upload_or_fetch():
    client = APIClient()
    f = io.BytesIO(b"data")
    f.name = "unauth.txt"
    response = client.post(
        "/api/file_versions/",
        {"file": f, "path": "/documents/unauth/unauth.txt"},
        format="multipart"
    )
    assert response.status_code in (401, 403)
    response = client.get("/api/file_versions/")
    assert response.status_code in (401, 403)

@pytest.mark.django_db
def test_fetch_nonexistent_version_returns_404(user):
    client = APIClient()
    client.force_authenticate(user=user)
    path = "/documents/test/missing.txt"
    response = client.get(f"/api/file_versions/by_path/?path={path}&version=1")
    assert response.status_code == 404