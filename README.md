# Propylon Document Manager Assessment

This project is a web application for secure document storage and versioning, built as part of the Propylon Document Management Technical Assessment. It consists of a Django REST Framework API backend and a React frontend client. The application allows authenticated users to upload, store, and retrieve files at user-specified URLs, with support for multiple versions and content-addressable storage.

---

## Features

- **Store files of any type and name** at any user-specified URL.
- **Multiple file versions**: Upload new revisions to the same URL and retrieve any version.
- **Content Addressable Storage**: Retrieve files by their content hash.
- **Authentication required**: Only authenticated users can interact with the API.
- **User isolation**: Users cannot access files uploaded by other users.
- **Comprehensive API test suite** using pytest and factory-boy.
- **Frontend**: React app for login, upload, and file version management.

---

## Project Structure

```
.
├── client/doc-manager/        # React frontend application
├── src/propylon_document_manager/
│   ├── file_versions/         # Django app for file versioning
│   └── site/                  # Django project settings and URLs
├── tests/                     # Pytest-based backend test suite
├── requirements/              # Python requirements files
├── Makefile                   # Development and management commands
├── README.md                  # This file
└── ...
```

---

## Getting Started

### Backend (API) Setup

1. **Install Python 3.11**  
   Ensure Python 3.11 is installed on your system.

2. **Create and activate the virtual environment**  
   ```sh
   make build
   source .env_python3.11/bin/activate
   ```

3. **Install dependencies**  
   (Handled by `make build`, but you can also run:)
   ```sh
   pip install -r requirements/dev.txt
   ```

4. **Apply migrations**  
   ```sh
   make makemigrations
   make migrate
   ```

5. **Load fixture data (optional)**  
   ```sh
   make fixture
   ```

6. **Create a user**
   - **Normal user (Django shell):**
     ```sh
     python manage.py shell
     ```
     ```python
     from propylon_document_manager.file_versions.models import User
     User.objects.create_user(email="user@example.com", password="yourpassword")
     ```
   - **Superuser (admin access):**
     ```sh
     python manage.py createsuperuser
     ```
     Enter your email and password when prompted.

7. **Run the development server**  
   ```sh
   make serve
   ```
   The API will be available at [http://localhost:8002/](http://localhost:8002/).

---

### Frontend (React Client) Setup

1. **Install Node.js v18.19.0**  
   Use [nvm](https://github.com/nvm-sh/nvm) and run:
   ```sh
   nvm use
   ```

2. **Install dependencies**  
   ```sh
   cd client/doc-manager
   npm install
   ```

3. **Start the React development server**  
   ```sh
   npm start
   ```
   The frontend will be available at [http://localhost:3000/](http://localhost:3000/).

---

## Usage

- **Login:**  
  Use your email and password to log in via the frontend.
- **Upload Files:**  
  Upload any file and specify its storage path (URL).
- **View File Versions:**  
  See all your uploaded files and their versions.
- **Download/View:**  
  Download or view any version of your files.
- **Delete:**  
  Remove your own file versions.
- **Content Addressable Retrieval:**  
  Retrieve a file version by its content hash using the `/api/file_versions/by_hash/<hash>/` endpoint.

---

## API Endpoints

- `POST /auth-token/`  
  Obtain an authentication token (send `email` and `password`).

- `GET /api/file_versions/`  
  List all file versions for the authenticated user.

- `POST /api/file_versions/`  
  Upload a new file version.

- `GET /api/file_versions/by_path/?path=<url>&version=<n>`  
  Retrieve a specific version of a file by path and version number.

- `GET /api/file_versions/by_hash/<content_hash>/`  
  Retrieve a file version by its content hash.

- `DELETE /api/file_versions/<id>/`  
  Delete a file version you own.

---

## Testing

- **Run all backend tests:**
  ```sh
  make test
  ```
  or
  ```sh
  pytest
  ```

- **Test coverage:**  
  The test suite covers authentication, file upload, versioning, access control, and retrieval by path and hash.

---

## Permissions & Security

- Only authenticated users can access the API.
- Users can only access their own files.
- Superusers can access the Django admin at `/admin/` (if enabled).
- All endpoints are protected by token authentication.

---

## Notes

- **Media files** are stored in `src/propylon_document_manager/media/` by default.
- **Database**: Uses SQLite by default; you can change this in the Django settings.
- **Production**: For deployment, review and adjust settings in `src/propylon_document_manager/site/settings/production.py`.

---

## Improvements & Stretch Goals

- [ ] Per-version read/write permissions (not implemented).
- [ ] UI for diffing file versions (not implemented).
- [ ] More advanced admin features.

---

## Repository & Delivery

- All development should be committed with clear history.
- Do **not** include virtual environment or node_modules in your submission.
- If submitting via GitHub, use a **private repository** and share access as instructed.

---

## Contact

For questions or to coordinate delivery, contact marina.saric@rws.com.

---

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)