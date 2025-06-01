# Student Management API

A FastAPI-based REST API for managing students with JWT authentication and MongoDB database.

## Features

- JWT-based authentication
- Complete CRUD operations for students
- MongoDB integration with Motor (async driver)
- Input validation with Pydantic
- Age validation (< 18) and grade validation (≤ 12)
- Comprehensive error handling
- Auto-generated API documentation

## Requirements

- Python 3.8+
- MongoDB 4.0+

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd student_management_backend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create environment file:
```bash
cp .env.example .env
```

5. Update `.env` file with your MongoDB URI and JWT secret:
```
MONGODB_URI=mongodb://localhost:27017
DATABASE_NAME=student_management
JWT_SECRET_KEY=your-super-secret-jwt-key-here-change-this-in-production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Running the Application

1. Start MongoDB service (if running locally)

2. Run the FastAPI application:
```bash
uvicorn app.main:app --reload
```

The API will be available at: http://localhost:8000

## API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

All endpoints are prefixed with `/v1` for API versioning.

### Authentication
- `POST /v1/auth/register` - Register a new user
- `POST /v1/auth/login` - Login and get JWT token

### Students (Protected Routes)
- `GET /v1/students/` - Get all students
- `POST /v1/students/` - Create a new student
- `GET /v1/students/{id}` - Get student by ID
- `PUT /v1/students/{id}` - Update student by ID
- `DELETE /v1/students/{id}` - Delete student by ID

## Usage Examples

### 1. Register a new user
```bash
curl -X POST "http://localhost:8000/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "email": "admin@example.com",
    "password": "password123"
  }'
```

### 2. Login and get token
```bash
curl -X POST "http://localhost:8000/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "password123"
  }'
```

### 3. Create a student (with token)
```bash
curl -X POST "http://localhost:8000/v1/students/" \
  -H "Content-Type: application