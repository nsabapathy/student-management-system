from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.routers import students
from app.database.connection import db

app = FastAPI(title="Student Management System API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_db_client():
    await db.connect_db()

@app.on_event("shutdown")
async def shutdown_db_client():
    await db.close_db()

# Include routers
app.include_router(students.router, prefix="/api/v1", tags=["students"])

@app.get("/health")
async def health_check():
    return {"status": "healthy"}