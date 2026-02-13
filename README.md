# Course Enrollment Management API (FastAPI)

A RESTful API for managing users, courses, and enrollments with role-based behavior (`student` vs `admin`) using in-memory storage.

## Features

- User management (create/list/get)
- Public course access (list/get)
- Admin-only course management (create/update/delete)
- Student enrollment/deregistration
- Admin enrollment oversight and force deregistration
- Pydantic validation for request payloads
- Full automated tests for all endpoints

## Project Structure

```text
app/
  core/
    store.py
  routers/
    users.py
    courses.py
    enrollments.py
  dependencies.py
  main.py
  models.py
  schemas.py
tests/
  conftest.py
  test_users.py
  test_courses.py
  test_enrollments.py
docs/
  LINE_BY_LINE.md
requirements.txt
README.md
```

## Run the API

1. Create a virtual environment and activate it.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Start the app:

```bash
uvicorn app.main:app --reload
```

API base URL: `http://127.0.0.1:8000`

Interactive docs:
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Run the tests

```bash
pytest
```

## Notes

- Data is stored in memory and resets when the process restarts.
- Authentication is intentionally omitted per assignment requirements.
- Role is provided in request data (`requester_role`) for role-restricted operations.
