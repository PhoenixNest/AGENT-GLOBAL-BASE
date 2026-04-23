---
name: frontend-web-react-react-fastapi
description: 'Frontend Web skill: React Fastapi'
---

# React + FastAPI Integration

**Category:** Full-Stack Engineering (Python/React)
**Owner:** Full-Stack Engineer (Sora Kim)

## Overview

Integrates React frontends with Python FastAPI backends, leveraging React Query for async state management, async task queues with Celery and Redis, file upload handling with multipart forms and presigned URLs, and biometric authentication flows with WebAuthn. Bridges Python backend capabilities with modern React frontend patterns.

## Competency Dimensions

| Dimension                 | Description                                                                                   | Proficiency Indicators                                                                                                                         |
| ------------------------- | --------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| React Query               | Query caching, mutations, optimistic updates, query invalidation, infinite queries            | Configures React Query with appropriate stale times; implements optimistic updates with rollback; uses query invalidation for data consistency |
| FastAPI Integration       | CORS configuration, authentication headers, error response mapping, OpenAPI client generation | Configures FastAPI CORS for React origin; maps FastAPI error responses to React error states; generates TypeScript clients from OpenAPI spec   |
| Async Task Queues         | Celery task management, task status polling, progress reporting, result retrieval             | Implements task status polling with React Query; handles task failure states; displays progress indicators for long-running tasks              |
| File Upload               | Multipart form data, presigned S3 URLs, upload progress, chunked uploads                      | Implements direct-to-S3 upload with presigned URLs; displays upload progress; handles upload retry on failure                                  |
| Biometric Auth (WebAuthn) | Registration ceremony, authentication ceremony, credential management, fallback flows         | Implements WebAuthn registration and authentication; handles platform authenticator (Touch ID/Face ID); provides fallback to password auth     |

## Execution Guidance

### React Query Integration with FastAPI

```typescript
// queryClient configuration
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5, // 5 minutes
      gcTime: 1000 * 60 * 30, // 30 minutes (formerly cacheTime)
      retry: (failureCount, error) => {
        if (error?.response?.status === 404) return false;
        if (error?.response?.status === 401) return false;
        return failureCount < 2;
      },
      refetchOnWindowFocus: false,
    },
    mutations: {
      retry: false,
    },
  },
});

// API client with error handling
import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  headers: { 'Content-Type': 'application/json' },
});

// Request interceptor: attach auth token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('auth_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor: map FastAPI errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.data?.detail) {
      // FastAPI validation error format
      const detail = error.response.data.detail;
      if (Array.isArray(detail)) {
        // Pydantic validation errors
        return Promise.reject({
          type: 'validation',
          errors: detail.map((e: any) => ({
            field: e.loc.join('.'),
            message: e.msg,
          })),
        });
      }
      // Simple error message
      return Promise.reject({
        type: 'api',
        message: detail,
        code: error.response.data.code,
      });
    }
    return Promise.reject({ type: 'network', message: 'Network error' });
  }
);

// User queries
const userKeys = {
  all: ['users'] as const,
  detail: (id: string) => ['users', id] as const,
  me: ['users', 'me'] as const,
};

export function useUser(id: string) {
  return useQuery({
    queryKey: userKeys.detail(id),
    queryFn: () => api.get(`/api/users/${id}`).then((r) => r.data),
  });
}

export function useUsers(page = 1, search?: string) {
  return useQuery({
    queryKey: [...userKeys.all, { page, search }],
    queryFn: () =>
      api
        .get('/api/users', {
          params: { page, search, page_size: 20 },
        })
        .then((r) => r.data),
  });
}

// Mutations with optimistic updates
export function useCreateUser() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: CreateUserInput) => api.post('/api/users', data).then((r) => r.data),

    // Optimistic update
    onMutate: async (newUser) => {
      // Cancel outgoing refetches
      await queryClient.cancelQueries({ queryKey: userKeys.all });

      // Snapshot current value
      const previous = queryClient.getQueryData(userKeys.all);

      // Optimistically update
      queryClient.setQueryData(userKeys.all, (old: any[] = []) => [
        ...old,
        { ...newUser, id: 'temp-id', created_at: new Date().toISOString() },
      ]);

      return { previous };
    },

    // Rollback on error
    onError: (_err, _newUser, context) => {
      if (context?.previous) {
        queryClient.setQueryData(userKeys.all, context.previous);
      }
    },

    // Refetch after mutation
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: userKeys.all });
    },
  });
}

// Infinite query for scrollable lists
export function useInfiniteUsers() {
  return useInfiniteQuery({
    queryKey: ['users', 'infinite'],
    queryFn: ({ pageParam = 1 }) =>
      api.get('/api/users', { params: { page: pageParam, page_size: 20 } }).then((r) => r.data),
    getNextPageParam: (lastPage, allPages) => {
      return lastPage.has_more ? allPages.length + 1 : undefined;
    },
    initialPageParam: 1,
  });
}
```

### Celery + Redis Async Task Queue

**FastAPI endpoint for task submission:**

```python
# tasks.py (Celery tasks)
from celery import Celery
import time

celery_app = Celery(
    "worker",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/1",
)

@celery_app.task(bind=True)
def process_data_export(self, user_id: str, filters: dict):
    """Long-running data export task."""
    total_records = get_record_count(filters)

    for i in range(0, total_records, 1000):
        # Update progress
        progress = min(100, int((i / total_records) * 100))
        self.update_state(
            state="PROGRESS",
            meta={"current": i, "total": total_records, "progress": progress},
        )

        # Process batch
        batch = fetch_records(filters, offset=i, limit=1000)
        export_batch(batch)

        time.sleep(0.1)  # Simulate work

    # Generate download URL
    download_url = generate_download_link(user_id)

    return {"status": "complete", "download_url": download_url}
```

**FastAPI endpoints for task management:**

```python
# routes/tasks.py
from fastapi import APIRouter, HTTPException
from celery.result import AsyncResult
from tasks import celery_app

router = APIRouter(prefix="/api/tasks", tags=["tasks"])

@router.get("/{task_id}")
async def get_task_status(task_id: str):
    result = AsyncResult(task_id, app=celery_app)

    response = {
        "task_id": task_id,
        "status": result.status,
    }

    if result.status == "PROGRESS":
        response["progress"] = result.info
    elif result.status == "SUCCESS":
        response["result"] = result.result
    elif result.status == "FAILURE":
        response["error"] = str(result.result)

    return response

@router.post("/export")
async def start_export(request: ExportRequest, user: User = Depends(get_current_user)):
    task = process_data_export.delay(user.id, request.filters.dict())

    return {
        "task_id": task.id,
        "status_url": f"/api/tasks/{task.id}",
    }
```

**React component for task polling:**

```typescript
// TaskStatusMonitor component
export function TaskStatusMonitor({ taskId, onComplete }: TaskStatusMonitorProps) {
  const { data, isLoading } = useQuery({
    queryKey: ['tasks', taskId],
    queryFn: () => api.get(`/api/tasks/${taskId}`).then((r) => r.data),
    refetchInterval: (query) => {
      const status = query.state.data?.status;
      return status === 'SUCCESS' || status === 'FAILURE' ? false : 2000; // Poll every 2s
    },
  });

  if (isLoading) return <LoadingSpinner />;

  if (data.status === 'PROGRESS') {
    return (
      <ProgressBar
        value={data.progress?.progress || 0}
        label={`Processing: ${data.progress?.current}/${data.progress?.total}`}
      />
    );
  }

  if (data.status === 'SUCCESS') {
    onComplete?.(data.result);
    return (
      <Alert variant="success">
        Export complete! <a href={data.result.download_url}>Download</a>
      </Alert>
    );
  }

  if (data.status === 'FAILURE') {
    return <Alert variant="error">Export failed: {data.error}</Alert>;
  }

  return <Spinner />;
}
```

### File Upload with Presigned URLs

**FastAPI presigned URL generation:**

```python
import boto3
from fastapi import APIRouter, Depends

router = APIRouter(prefix="/api/uploads", tags=["uploads"])
s3_client = boto3.client("s3")

@router.post("/presign")
async def generate_presigned_url(
    request: PresignRequest,
    user: User = Depends(get_current_user),
):
    """Generate presigned URL for direct S3 upload."""

    # Validate file type
    allowed_types = {"image/jpeg", "image/png", "image/webp", "application/pdf"}
    if request.content_type not in allowed_types:
        raise HTTPException(400, f"Unsupported content type: {request.content_type}")

    # Validate file size
    max_size = 50 * 1024 * 1024  # 50MB
    if request.file_size > max_size:
        raise HTTPException(400, f"File too large: {request.file_size} bytes")

    # Generate unique key
    file_key = f"uploads/{user.id}/{uuid4().hex}_{request.filename}"

    # Generate presigned URL (valid for 1 hour)
    presigned_url = s3_client.generate_presigned_url(
        "put_object",
        Params={
            "Bucket": settings.S3_BUCKET,
            "Key": file_key,
            "ContentType": request.content_type,
        },
        ExpiresIn=3600,
    )

    return {
        "upload_url": presigned_url,
        "file_key": file_key,
        "headers": {
            "Content-Type": request.content_type,
        },
    }

@router.post("/complete")
async def complete_upload(
    request: CompleteUploadRequest,
    user: User = Depends(get_current_user),
):
    """Register uploaded file in database after direct S3 upload."""
    # Verify file exists in S3
    try:
        s3_client.head_object(Bucket=settings.S3_BUCKET, Key=request.file_key)
    except ClientError:
        raise HTTPException(400, "File not found in S3")

    # Save to database
    file_record = FileRecord(
        user_id=user.id,
        s3_key=request.file_key,
        filename=request.filename,
        content_type=request.content_type,
        size=request.file_size,
    )
    db.add(file_record)
    db.commit()

    # Generate download URL
    download_url = s3_client.generate_presigned_url(
        "get_object",
        Params={"Bucket": settings.S3_BUCKET, "Key": request.file_key},
        ExpiresIn=3600,
    )

    return {"file_id": file_record.id, "download_url": download_url}
```

**React upload component:**

```typescript
export function FileUpload({ onUpload }: FileUploadProps) {
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState(0);

  const handleFile = async (file: File) => {
    setUploading(true);
    setProgress(0);

    try {
      // Step 1: Get presigned URL
      const { upload_url, file_key, headers } = await api
        .post('/api/uploads/presign', {
          filename: file.name,
          content_type: file.type,
          file_size: file.size,
        })
        .then((r) => r.data);

      // Step 2: Upload directly to S3
      await axios.put(upload_url, file, {
        headers,
        onUploadProgress: (e) => {
          setProgress(Math.round((e.loaded / e.total) * 100));
        },
      });

      // Step 3: Complete upload (register in database)
      const result = await api
        .post('/api/uploads/complete', {
          file_key,
          filename: file.name,
          content_type: file.type,
          file_size: file.size,
        })
        .then((r) => r.data);

      onUpload?.(result);
    } catch (error) {
      console.error('Upload failed:', error);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div>
      <input type="file" onChange={(e) => e.target.files?.[0] && handleFile(e.target.files[0])} />
      {uploading && <ProgressBar value={progress} />}
    </div>
  );
}
```

### Biometric Authentication with WebAuthn

**FastAPI WebAuthn endpoints:**

```python
from webauthn import (
    generate_registration_options,
    verify_registration_response,
    generate_authentication_options,
    verify_authentication_response,
)
from webauthn.helpers.structs import (
    PublicKeyCredentialCreationOptions,
    UserVerificationRequirement,
    AttestationConveyancePreference,
)

router = APIRouter(prefix="/api/webauthn", tags=["webauthn"])

@router.post("/register/options")
async def registration_options(user: User = Depends(get_current_user)):
    """Generate WebAuthn registration options."""
    options = generate_registration_options(
        rp_id="app.company.com",
        rp_name="Company App",
        user_id=user.id.encode(),
        user_name=user.email,
        user_display_name=user.name,
        authenticator_selection=AuthenticatorSelection(
            user_verification=UserVerificationRequirement.PREFERRED,
            resident_key=ResidentKeyRequirement.PREFERRED,
        ),
        attestation=AttestationConveyancePreference.NONE,
    )

    # Store challenge in session/Redis
    await redis.set(f"webauthn:challenge:{user.id}", options.challenge, ex=300)

    return options

@router.post("/register/verify")
async def registration_verify(
    request: RegistrationVerifyRequest,
    user: User = Depends(get_current_user),
):
    """Verify WebAuthn registration response."""
    challenge = await redis.get(f"webauthn:challenge:{user.id}")
    if not challenge:
        raise HTTPException(400, "Registration expired")

    try:
        verification = verify_registration_response(
            credential=request.response,
            challenge=challenge,
            rp_id="app.company.com",
            expected_origin="https://app.company.com",
            expected_rp_id="app.company.com",
            require_user_verification=True,
        )

        # Store credential in database
        credential = WebAuthnCredential(
            user_id=user.id,
            credential_id=verification.credential_id,
            public_key=verification.credential_public_key,
            sign_count=verification.sign_count,
            transport=request.transports,
        )
        db.add(credential)
        db.commit()

        return {"status": "registered"}

    except Exception as e:
        raise HTTPException(400, f"Verification failed: {str(e)}")

@router.post("/login/options")
async def login_options(request: LoginOptionsRequest):
    """Generate WebAuthn authentication options."""
    # Look up user's credentials
    credentials = db.query(WebAuthnCredential).filter(
        WebAuthnCredential.user_id == request.user_id
    ).all()

    options = generate_authentication_options(
        rp_id="app.company.com",
        allow_credentials=[
            PublicKeyCredentialDescriptor(id=c.credential_id)
            for c in credentials
        ],
        user_verification=UserVerificationRequirement.PREFERRED,
    )

    await redis.set(f"webauthn:auth_challenge:{request.user_id}", options.challenge, ex=300)
    return options

@router.post("/login/verify")
async def login_verify(request: LoginVerifyRequest):
    """Verify WebAuthn authentication response."""
    credential = db.query(WebAuthnCredential).filter(
        WebAuthnCredential.credential_id == request.response.id
    ).first()

    if not credential:
        raise HTTPException(401, "Credential not found")

    challenge = await redis.get(f"webauthn:auth_challenge:{credential.user_id}")

    try:
        verification = verify_authentication_response(
            credential=request.response,
            challenge=challenge,
            expected_rp_id="app.company.com",
            expected_origin="https://app.company.com",
            credential_public_key=credential.public_key,
            credential_current_sign_count=credential.sign_count,
            require_user_verification=True,
        )

        # Update sign count
        credential.sign_count = verification.sign_count
        db.commit()

        # Generate JWT
        user = db.query(User).get(credential.user_id)
        token = create_access_token(user)

        return {"access_token": token, "token_type": "bearer"}

    except Exception as e:
        raise HTTPException(401, f"Authentication failed: {str(e)}")
```

**React WebAuthn integration:**

```typescript
// WebAuthn registration
export async function registerBiometric(userId: string) {
  // Step 1: Get registration options from server
  const options = await api.post(`/api/webauthn/register/options`).then((r) => r.data);

  // Step 2: Create credential using browser API
  const credential = (await navigator.credentials.create({
    publicKey: options,
  })) as PublicKeyCredential;

  // Step 3: Send response back to server
  const response = await api.post('/api/webauthn/register/verify', {
    response: publicKeyCredentialToJSON(credential),
    transports: (credential.response as any).getTransports?.(),
  });

  return response.data;
}

// WebAuthn authentication
export async function authenticateBiometric(userId: string) {
  // Step 1: Get authentication options
  const options = await api
    .post(`/api/webauthn/login/options`, { user_id: userId })
    .then((r) => r.data);

  // Step 2: Get credential from browser (triggers Touch ID/Face ID)
  const credential = (await navigator.credentials.get({
    publicKey: options,
  })) as PublicKeyCredential;

  // Step 3: Verify with server
  const response = await api.post('/api/webauthn/login/verify', {
    response: publicKeyCredentialToJSON(credential),
  });

  return response.data; // { access_token, token_type }
}
```

## Pipeline Integration

**Stage 5 (Development):** React Query configured with appropriate caching. Celery tasks implement progress reporting. File uploads use presigned URLs for direct S3 upload. WebAuthn registration and authentication flows complete.

**Stage 6 (Code Review):** Review React Query invalidation patterns. Validate Celery task idempotency. Check presigned URL security (expiration, bucket policy). Verify WebAuthn challenge lifecycle.

**Stage 7 (Testing):** React Query mock testing. Celery task integration tests. File upload end-to-end tests. WebAuthn flow tests (with mock credentials).

## Quality Standards

| Metric                          | Target  | Measurement          |
| ------------------------------- | ------- | -------------------- |
| React Query cache hit rate      | > 70%   | React Query devtools |
| Celery task success rate        | > 99%   | Celery monitoring    |
| File upload success rate        | > 99.5% | Upload monitoring    |
| WebAuthn registration success   | > 95%   | Registration metrics |
| API response time (p95)         | < 200ms | Application metrics  |
| Optimistic update rollback rate | < 1%    | Error tracking       |
