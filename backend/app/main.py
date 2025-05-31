from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.core.config import settings
from app.routers.students import router as student_router
from app.database.connection import db

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Connect to the database
    await db.connect_db()
    yield
    # Shutdown: Close the database connection
    await db.close_db()

app = FastAPI(title="Student Management System API", lifespan=lifespan)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(student_router, prefix="/api/v1/students", tags=["students"])

@app.get("/health")
async def health_check():
    return {"status": "healthy"}