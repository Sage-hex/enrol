from fastapi import FastAPI

from app.routers import users, courses, enrollments

app = FastAPI(title="Course Enrollment Management API", version="1.0.0")

app.include_router(users.router)
app.include_router(courses.router)
app.include_router(enrollments.router)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
