def setup_admin_and_student(client):
    admin = client.post(
        "/users",
        json={"name": "Admin", "email": "admin@example.com", "role": "admin"},
    )
    student = client.post(
        "/users",
        json={"name": "Student", "email": "student@example.com", "role": "student"},
    )
    return admin.json(), student.json()


def test_public_course_access(client):
    setup_admin_and_student(client)
    client.post(
        "/courses",
        json={"title": "Math", "code": "MTH101", "requester_role": "admin"},
    )

    all_courses = client.get("/courses")
    assert all_courses.status_code == 200
    assert len(all_courses.json()) == 1

    one_course = client.get("/courses/1")
    assert one_course.status_code == 200
    assert one_course.json()["code"] == "MTH101"


def test_admin_only_create_update_delete_course(client):
    setup_admin_and_student(client)

    forbidden_create = client.post(
        "/courses",
        json={"title": "Math", "code": "MTH101", "requester_role": "student"},
    )
    assert forbidden_create.status_code == 403

    created = client.post(
        "/courses",
        json={"title": "Math", "code": "MTH101", "requester_role": "admin"},
    )
    assert created.status_code == 201

    forbidden_update = client.put(
        "/courses/1",
        json={"title": "Math II", "code": "MTH102", "requester_role": "student"},
    )
    assert forbidden_update.status_code == 403

    updated = client.put(
        "/courses/1",
        json={"title": "Math II", "code": "MTH102", "requester_role": "admin"},
    )
    assert updated.status_code == 200
    assert updated.json()["title"] == "Math II"

    forbidden_delete = client.delete("/courses/1", params={"requester_role": "student"})
    assert forbidden_delete.status_code == 403

    deleted = client.delete("/courses/1", params={"requester_role": "admin"})
    assert deleted.status_code == 204


def test_course_validation_and_uniqueness(client):
    setup_admin_and_student(client)

    invalid = client.post(
        "/courses",
        json={"title": " ", "code": " ", "requester_role": "admin"},
    )
    assert invalid.status_code == 422

    client.post(
        "/courses",
        json={"title": "Math", "code": "MTH101", "requester_role": "admin"},
    )
    duplicate = client.post(
        "/courses",
        json={"title": "Math 2", "code": "MTH101", "requester_role": "admin"},
    )
    assert duplicate.status_code == 409


def test_course_not_found(client):
    setup_admin_and_student(client)

    get_response = client.get("/courses/999")
    assert get_response.status_code == 404

    update_response = client.put(
        "/courses/999",
        json={"title": "x", "code": "x", "requester_role": "admin"},
    )
    assert update_response.status_code == 404

    delete_response = client.delete("/courses/999", params={"requester_role": "admin"})
    assert delete_response.status_code == 404
