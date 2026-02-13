from typing import Literal

from fastapi import APIRouter, HTTPException, Query, status

from app.core.store import store
from app.dependencies import require_admin, require_student
from app.models import Enrollment
from app.schemas import EnrollmentCreate, EnrollmentDelete, EnrollmentRead

router = APIRouter(prefix="/enrollments", tags=["enrollments"])


@router.post("", response_model=EnrollmentRead, status_code=status.HTTP_201_CREATED)
def enroll_student(payload: EnrollmentCreate) -> EnrollmentRead:
    require_student(payload.requester_role)

    user = store.users.get(payload.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")

    course = store.courses.get(payload.course_id)
    if not course:
        raise HTTPException(status_code=404, detail="course not found")

    for enrollment in store.enrollments.values():
        if enrollment.user_id == payload.user_id and enrollment.course_id == payload.course_id:
            raise HTTPException(status_code=409, detail="student already enrolled in this course")

    enrollment = Enrollment(
        id=store.next_enrollment_id(),
        user_id=payload.user_id,
        course_id=payload.course_id,
    )
    store.enrollments[enrollment.id] = enrollment
    return EnrollmentRead(**enrollment.model_dump())


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
def deregister_student(payload: EnrollmentDelete) -> None:
    require_student(payload.requester_role)

    enrollment_to_delete = None
    for enrollment_id, enrollment in store.enrollments.items():
        if enrollment.user_id == payload.user_id and enrollment.course_id == payload.course_id:
            enrollment_to_delete = enrollment_id
            break

    if enrollment_to_delete is None:
        raise HTTPException(status_code=404, detail="enrollment not found")

    del store.enrollments[enrollment_to_delete]


@router.get("/students/{user_id}", response_model=list[EnrollmentRead])
def get_student_enrollments(user_id: int) -> list[EnrollmentRead]:
    if user_id not in store.users:
        raise HTTPException(status_code=404, detail="user not found")

    return [
        EnrollmentRead(**enrollment.model_dump())
        for enrollment in store.enrollments.values()
        if enrollment.user_id == user_id
    ]


@router.get("", response_model=list[EnrollmentRead])
def get_all_enrollments(requester_role: Literal["student", "admin"] = Query(...)) -> list[EnrollmentRead]:
    require_admin(requester_role)
    return [EnrollmentRead(**enrollment.model_dump()) for enrollment in store.enrollments.values()]


@router.get("/courses/{course_id}", response_model=list[EnrollmentRead])
def get_course_enrollments(
    course_id: int, requester_role: Literal["student", "admin"] = Query(...)
) -> list[EnrollmentRead]:
    require_admin(requester_role)

    if course_id not in store.courses:
        raise HTTPException(status_code=404, detail="course not found")

    return [
        EnrollmentRead(**enrollment.model_dump())
        for enrollment in store.enrollments.values()
        if enrollment.course_id == course_id
    ]


@router.delete("/force", status_code=status.HTTP_204_NO_CONTENT)
def force_deregister_student(payload: EnrollmentDelete) -> None:
    require_admin(payload.requester_role)

    enrollment_to_delete = None
    for enrollment_id, enrollment in store.enrollments.items():
        if enrollment.user_id == payload.user_id and enrollment.course_id == payload.course_id:
            enrollment_to_delete = enrollment_id
            break

    if enrollment_to_delete is None:
        raise HTTPException(status_code=404, detail="enrollment not found")

    del store.enrollments[enrollment_to_delete]
