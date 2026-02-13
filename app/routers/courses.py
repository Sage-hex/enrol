from fastapi import APIRouter, HTTPException, Query, status

from app.core.store import store
from app.dependencies import require_admin
from app.models import Course
from app.schemas import CourseCreate, CourseRead, CourseUpdate

router = APIRouter(prefix="/courses", tags=["courses"])


@router.get("", response_model=list[CourseRead])
def get_courses() -> list[CourseRead]:
    return [CourseRead(**course.model_dump()) for course in store.courses.values()]


@router.get("/{course_id}", response_model=CourseRead)
def get_course(course_id: int) -> CourseRead:
    course = store.courses.get(course_id)
    if not course:
        raise HTTPException(status_code=404, detail="course not found")
    return CourseRead(**course.model_dump())


@router.post("", response_model=CourseRead, status_code=status.HTTP_201_CREATED)
def create_course(payload: CourseCreate) -> CourseRead:
    require_admin(payload.requester_role)
    for course in store.courses.values():
        if course.code == payload.code:
            raise HTTPException(status_code=409, detail="course code must be unique")

    data = payload.model_dump(exclude={"requester_role"})
    course = Course(id=store.next_course_id(), **data)
    store.courses[course.id] = course
    return CourseRead(**course.model_dump())


@router.put("/{course_id}", response_model=CourseRead)
def update_course(course_id: int, payload: CourseUpdate) -> CourseRead:
    require_admin(payload.requester_role)

    course = store.courses.get(course_id)
    if not course:
        raise HTTPException(status_code=404, detail="course not found")

    for existing in store.courses.values():
        if existing.code == payload.code and existing.id != course_id:
            raise HTTPException(status_code=409, detail="course code must be unique")

    updated = Course(
        id=course_id,
        title=payload.title,
        code=payload.code,
    )
    store.courses[course_id] = updated
    return CourseRead(**updated.model_dump())


@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(course_id: int, requester_role: str = Query(...)) -> None:
    require_admin(requester_role)

    if course_id not in store.courses:
        raise HTTPException(status_code=404, detail="course not found")

    del store.courses[course_id]

    enrollment_ids = [
        enrollment_id
        for enrollment_id, enrollment in store.enrollments.items()
        if enrollment.course_id == course_id
    ]
    for enrollment_id in enrollment_ids:
        del store.enrollments[enrollment_id]
