def seed_users_and_course(client):
    student = client.post(
        "/users",
        json={"name": "Student", "email": "student@example.com", "role": "student"},
    ).json()
    admin = client.post(
        "/users",
        json={"name": "Admin", "email": "admin@example.com", "role": "admin"},
    ).json()
    course = client.post(
        "/courses",
        json={"title": "Biology", "code": "BIO101", "requester_role": "admin"},
    ).json()
    return student, admin, course


def test_student_can_enroll_and_deregister(client):
    student, _, course = seed_users_and_course(client)

    enroll = client.post(
        "/enrollments",
        json={
            "user_id": student["id"],
            "course_id": course["id"],
            "requester_role": "student",
        },
    )
    assert enroll.status_code == 201

    deregister = client.delete(
        "/enrollments",
        json={
            "user_id": student["id"],
            "course_id": course["id"],
            "requester_role": "student",
        },
    )
    assert deregister.status_code == 204


def test_student_role_restrictions(client):
    student, _, course = seed_users_and_course(client)

    response = client.post(
        "/enrollments",
        json={"user_id": student["id"], "course_id": course["id"], "requester_role": "admin"},
    )
    assert response.status_code == 403

    response = client.delete(
        "/enrollments",
        json={"user_id": student["id"], "course_id": course["id"], "requester_role": "admin"},
    )
    assert response.status_code == 403


def test_enrollment_business_rules(client):
    student, _, course = seed_users_and_course(client)

    first = client.post(
        "/enrollments",
        json={"user_id": student["id"], "course_id": course["id"], "requester_role": "student"},
    )
    assert first.status_code == 201

    duplicate = client.post(
        "/enrollments",
        json={"user_id": student["id"], "course_id": course["id"], "requester_role": "student"},
    )
    assert duplicate.status_code == 409

    missing_user = client.post(
        "/enrollments",
        json={"user_id": 999, "course_id": course["id"], "requester_role": "student"},
    )
    assert missing_user.status_code == 404

    missing_course = client.post(
        "/enrollments",
        json={"user_id": student["id"], "course_id": 999, "requester_role": "student"},
    )
    assert missing_course.status_code == 404

    missing_enrollment = client.delete(
        "/enrollments",
        json={"user_id": student["id"], "course_id": 999, "requester_role": "student"},
    )
    assert missing_enrollment.status_code == 404


def test_get_student_enrollments(client):
    student, _, course = seed_users_and_course(client)
    client.post(
        "/enrollments",
        json={"user_id": student["id"], "course_id": course["id"], "requester_role": "student"},
    )

    response = client.get(f"/enrollments/students/{student['id']}")
    assert response.status_code == 200
    assert len(response.json()) == 1

    missing_user = client.get("/enrollments/students/999")
    assert missing_user.status_code == 404


def test_admin_enrollment_oversight_and_force_deregister(client):
    student, _, course = seed_users_and_course(client)
    client.post(
        "/enrollments",
        json={"user_id": student["id"], "course_id": course["id"], "requester_role": "student"},
    )

    forbidden_all = client.get("/enrollments", params={"requester_role": "student"})
    assert forbidden_all.status_code == 403

    all_enrollments = client.get("/enrollments", params={"requester_role": "admin"})
    assert all_enrollments.status_code == 200
    assert len(all_enrollments.json()) == 1

    forbidden_by_course = client.get(
        f"/enrollments/courses/{course['id']}", params={"requester_role": "student"}
    )
    assert forbidden_by_course.status_code == 403

    by_course = client.get(
        f"/enrollments/courses/{course['id']}", params={"requester_role": "admin"}
    )
    assert by_course.status_code == 200
    assert len(by_course.json()) == 1

    missing_course = client.get("/enrollments/courses/999", params={"requester_role": "admin"})
    assert missing_course.status_code == 404

    forbidden_force = client.delete(
        "/enrollments/force",
        json={"user_id": student["id"], "course_id": course["id"], "requester_role": "student"},
    )
    assert forbidden_force.status_code == 403

    forced = client.delete(
        "/enrollments/force",
        json={"user_id": student["id"], "course_id": course["id"], "requester_role": "admin"},
    )
    assert forced.status_code == 204

    missing_force = client.delete(
        "/enrollments/force",
        json={"user_id": student["id"], "course_id": course["id"], "requester_role": "admin"},
    )
    assert missing_force.status_code == 404
