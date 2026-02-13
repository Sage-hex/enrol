# Line-by-Line Implementation Notes

This document explains, file by file, what was implemented and why.

## `app/models.py`
1. Imported `BaseModel`, `EmailStr`, and `Literal` to define strongly typed domain models.
2. Created `User` with `id`, `name`, `email`, and `role` (`student`/`admin`).
3. Created `Course` with `id`, `title`, and `code`.
4. Created `Enrollment` with `id`, `user_id`, and `course_id`.

## `app/schemas.py`
1. Defined input/output schemas separate from domain models.
2. Added validation for non-empty `name`, `title`, and `code`.
3. Enforced valid `email` format with `EmailStr`.
4. Enforced role enum values with `Literal`.
5. Added `requester_role` to restricted operations to model role in request data.

## `app/core/store.py`
1. Implemented `InMemoryStore` with dictionaries for users/courses/enrollments.
2. Added incremental ID generators for each entity type.
3. Added a `reset()` method for deterministic test setup.
4. Exposed a singleton `store` used across routers.

## `app/dependencies.py`
1. Added role-check helpers:
   - `require_admin`
   - `require_student`
2. Each helper raises `403` when role requirements are violated.

## `app/routers/users.py`
1. Added `POST /users` to create users.
2. Added duplicate email guard (`409`).
3. Added `GET /users` to retrieve all users.
4. Added `GET /users/{user_id}` with not-found handling (`404`).

## `app/routers/courses.py`
1. Added public `GET /courses` and `GET /courses/{course_id}`.
2. Added admin-only `POST /courses` with unique code check (`409`).
3. Added admin-only `PUT /courses/{course_id}` with uniqueness and not-found checks.
4. Added admin-only `DELETE /courses/{course_id}` and cleanup of related enrollments.

## `app/routers/enrollments.py`
1. Added student-only `POST /enrollments`.
2. Enforced:
   - user existence
   - course existence
   - no duplicate enrollment
3. Added student-only `DELETE /enrollments` for deregistration.
4. Added `GET /enrollments/students/{user_id}` for student-specific enrollment retrieval.
5. Added admin-only `GET /enrollments` for all enrollments.
6. Added admin-only `GET /enrollments/courses/{course_id}`.
7. Added admin-only `DELETE /enrollments/force` for forced deregistration.

## `app/main.py`
1. Created FastAPI app instance with title/version metadata.
2. Registered user, course, and enrollment routers.
3. Added `GET /health` for basic service health checks.

## `tests/conftest.py`
1. Created `TestClient` fixture.
2. Reset in-memory store automatically before each test.

## `tests/test_users.py`
1. Covered user creation success.
2. Covered user validation failures.
3. Covered user listing and retrieval by ID.
4. Covered not-found and duplicate-email behavior.

## `tests/test_courses.py`
1. Covered public course endpoints.
2. Covered admin-only restrictions for create/update/delete.
3. Covered validation and code uniqueness constraints.
4. Covered not-found behavior for get/update/delete.

## `tests/test_enrollments.py`
1. Covered student enrollment and deregistration flow.
2. Covered role restrictions for student-only operations.
3. Covered duplicate, missing user, missing course, and missing enrollment rules.
4. Covered admin oversight endpoints and force deregistration.

## `README.md`
1. Documented features and project structure.
2. Documented install, run, and test commands.
3. Clarified in-memory behavior and no-auth scope.
