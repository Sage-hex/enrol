from app.models import User, Course, Enrollment


class InMemoryStore:
    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self.users: dict[int, User] = {}
        self.courses: dict[int, Course] = {}
        self.enrollments: dict[int, Enrollment] = {}
        self._user_id = 1
        self._course_id = 1
        self._enrollment_id = 1

    def next_user_id(self) -> int:
        current = self._user_id
        self._user_id += 1
        return current

    def next_course_id(self) -> int:
        current = self._course_id
        self._course_id += 1
        return current

    def next_enrollment_id(self) -> int:
        current = self._enrollment_id
        self._enrollment_id += 1
        return current


store = InMemoryStore()
