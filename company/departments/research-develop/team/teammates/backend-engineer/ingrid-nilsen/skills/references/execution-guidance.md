# Execution Guidance

## Execution Guidance

### Dependency Injection System

```python
from fastapi import Depends, FastAPI, HTTPException, Request, Response
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

app = FastAPI()
security = HTTPBearer()

# Database session dependency (per-request scope)
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise

# Authentication dependency
async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> User:
    """Extract and validate JWT token, return user."""
    try:
        payload = jwt.decode(
            credentials.credentials,
            SECRET_KEY,
            algorithms=["RS256"],
            audience="api",
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user_id = payload.get("sub")
    user = await db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user

# Role-based authorization dependency (sub-dependency)
def require_role(required_role: str):
    async def role_checker(user: Annotated[User, Depends(get_current_user)]) -> User:
        if user.role != required_role and user.role != "admin":
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return user
    return role_checker

# Usage in endpoints
@app.get("/users/{user_id}")
async def get_user(
    user_id: str,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(require_role("admin"))],
):
    user = await db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse.model_validate(user)

# Dependency override for testing
def override_get_db():
    session = MagicMock(spec=AsyncSession)
    yield session

app.dependency_overrides[get_db] = override_get_db
```

### Pydantic v2 Models

```python
from pydantic import (
    BaseModel, Field, field_validator, model_validator,
    EmailStr, ConfigDict, computed_field
)
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"

class CreateUserRequest(BaseModel):
    """Request model for creating a user."""
    name: str = Field(
        min_length=2,
        max_length=100,
        examples=["John Doe"],
        description="User's full name",
    )
    email: EmailStr = Field(
        max_length=255,
        examples=["john@example.com"],
        description="User's email address",
    )
    password: str = Field(
        min_length=12,
        max_length=128,
        examples=["SecureP@ssw0rd!"],
        description="User's password (min 12 characters)",
    )
    role: UserRole = Field(
        default=UserRole.USER,
        description="User role (defaults to 'user')",
    )

    @field_validator("name")
    @classmethod
    def name_alphanumeric(cls, v: str) -> str:
        if not v.replace(" ", "").isalnum():
            raise ValueError("Name must contain only letters and spaces")
        return v.strip()

    @field_validator("password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.islower() for c in v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        if not any(c in "!@#$%^&*()" for c in v):
            raise ValueError("Password must contain at least one special character")
        return v

class UserResponse(BaseModel):
    """Response model — excludes sensitive fields."""
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    email: str
    role: UserRole
    created_at: datetime

    # Computed field (not stored in DB)
    @computed_field
    @property
    def display_name(self) -> str:
        return f"{self.name} ({self.role.value})"

# Model serialization with nested models
class OrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    user: UserResponse  # Nested model
    items: list[OrderItemResponse]
    total_amount: float
    status: str
    created_at: datetime

    # Custom serialization
    def model_dump(self, **kwargs):
        # Exclude None values by default
        kwargs.setdefault("exclude_none", True)
        return super().model_dump(**kwargs)

# Generic response wrapper
class APIResponse[T](BaseModel):
    """Generic API response with metadata."""
    data: T
    meta: dict[str, Any] = Field(
        default_factory=dict,
        examples=[{"page": 1, "total": 100}],
    )
```

### Async Endpoint Patterns

```python
from fastapi import FastAPI, BackgroundTasks
from typing import Annotated
from sqlalchemy import select
import httpx
import asyncio

app = FastAPI()

# Correct async endpoint — all I/O is async
@app.get("/users/{user_id}/orders")
async def get_user_orders(
    user_id: str,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    # Async database query
    result = await db.execute(
        select(Order).where(Order.user_id == user_id)
    )
    orders = result.scalars().all()

    # Parallel async HTTP calls
    async with httpx.AsyncClient() as client:
        tasks = [
            client.get(f"https://inventory-api/products/{order.product_id}")
            for order in orders
        ]
        responses = await asyncio.gather(*tasks, return_exceptions=True)

    # Process results
    order_details = []
    for order, response in zip(orders, responses):
        if isinstance(response, Exception):
            order_details.append({"order": order, "product_info": None})
            continue
        product_data = response.json()
        order_details.append({"order": order, "product_info": product_data})

    return order_details

# When you MUST call blocking code, use run_in_executor
import aiofiles

@app.get("/files/{filename}")
async def read_file(filename: str):
    # Offload blocking file I/O to thread pool
    loop = asyncio.get_event_loop()
    content = await loop.run_in_executor(
        None,  # Default ThreadPoolExecutor
        lambda: open(f"/data/{filename}", "r").read()
    )
    return {"content": content}

# Async context manager for resource management
class DatabaseTransaction:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def __aenter__(self):
        return self.session

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            await self.session.rollback()
        else:
            await self.session.commit()

# Common async mistakes to AVOID:
# ❌ Don't mix sync and async incorrectly
# def sync_function():
#     time.sleep(1)  # Blocks the event loop!
#
# @app.get("/bad")
# async def bad_endpoint():
#     sync_function()  # This blocks ALL other requests
#
# ✅ Instead, use async libraries or run_in_executor
```

### Background Tasks with Celery

```python
# celery_app.py
from celery import Celery
from celery.schedules import crontab

celery_app = Celery(
    "worker",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/1",
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,

    # Retry configuration
    task_acks_late=True,  # Acknowledge after task completion
    task_reject_on_worker_lost=True,

    # Rate limiting
    worker_prefetch_multiplier=1,  # Fair task distribution

    # Periodic tasks
    beat_schedule={
        "cleanup-expired-sessions": {
            "task": "tasks.cleanup_expired_sessions",
            "schedule": crontab(hour=3, minute=0),  # Daily at 3 AM
        },
        "generate-daily-report": {
            "task": "tasks.generate_daily_report",
            "schedule": crontab(hour=6, minute=0),
        },
    },
)

# tasks.py
from celery_app import celery_app
from tenacity import retry, stop_after_attempt, wait_exponential

@celery_app.task(
    bind=True,
    max_retries=3,
    default_retry_delay=60,
)
@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=60),
    reraise=True,
)
def send_welcome_email(self, user_id: str, email: str):
    """Send welcome email with retry on failure."""
    try:
        response = email_service.send(
            to=email,
            template="welcome",
            context={"user_id": user_id},
        )
        return {"status": "sent", "message_id": response.message_id}
    except EmailServiceError as exc:
        # Retry with exponential backoff
        raise self.retry(exc=exc, countdown=2 ** self.request.retries)

@celery_app.task(bind=True)
def process_image_upload(self, file_path: str, user_id: str):
    """Long-running image processing task."""
    # Idempotency check
    if ImageResult.objects.filter(file_path=file_path).exists():
        return {"status": "already_processed"}

    # Process image
    result = image_processor.resize(file_path, target_size=(800, 600))

    # Store result
    ImageResult.objects.create(
        file_path=file_path,
        user_id=user_id,
        processed_path=result.path,
    )

    return {"status": "processed", "path": result.path}

# FastAPI endpoint that triggers Celery task
@app.post("/users/{user_id}/upload-image")
async def upload_image(
    user_id: str,
    file: UploadFile,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    # Save file
    file_path = f"/uploads/{user_id}/{file.filename}"
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    # Trigger background task
    task = process_image_upload.delay(file_path, user_id)

    return {
        "task_id": task.id,
        "status_url": f"/tasks/{task.id}/status",
    }

# Task status endpoint
@app.get("/tasks/{task_id}/status")
async def get_task_status(task_id: str):
    result = celery_app.AsyncResult(task_id)

    return {
        "task_id": task_id,
        "status": result.status,
        "result": result.result if result.ready() else None,
    }
```

### Middleware Configuration

```python
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import time
import logging

app = FastAPI()

# 1. CORS — must be first
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://app.company.com"],  # Never use ["*"] in production
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type", "X-Request-ID"],
    max_age=3600,  # Cache preflight for 1 hour
)

# 2. Trusted hosts (prevent Host header attacks)
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["api.company.com", "api-staging.company.com"],
)

# 3. Custom request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    start_time = time.perf_counter()

    # Add request ID to response
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id

    # Log request details
    duration = time.perf_counter() - start_time
    logging.info(
        f"{request.method} {request.url.path} - "
        f"{response.status_code} - {duration*1000:.1f}ms - "
        f"request_id={request_id}"
    )

    return response

# 4. Request size limit middleware
@app.middleware("http")
async def limit_request_size(request: Request, call_next):
    content_length = request.headers.get("content-length")
    if content_length and int(content_length) > 10 * 1024 * 1024:  # 10MB
        return Response(
            status_code=413,
            content='{"code":"payload_too_large","message":"Request body too large"}',
            media_type="application/json",
        )
    return await call_next(request)
```

### OpenAPI Auto-Generation

```python
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI(
    title="User Management API",
    description="API for managing users, orders, and authentication",
    version="1.0.0",
    docs_url="/docs",  # Swagger UI
    redoc_url="/redoc",  # ReDoc
    openapi_url="/openapi.json",

    # Custom OpenAPI schema
    openapi_tags=[
        {
            "name": "users",
            "description": "User management operations",
            "externalDocs": {
                "description": "User API documentation",
                "url": "https://docs.company.com/api/users",
            },
        },
    ],
)

# Custom OpenAPI schema with security schemes
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = app.openapi()

    # Add security schemes
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        },
    }

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# Generate client SDK
# pip install openapi-python-client
# openapi-python-client generate --url http://localhost:8000/openapi.json
```
