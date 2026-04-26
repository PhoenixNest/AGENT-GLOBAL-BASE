# Execution Guidance

## Execution Guidance

### OpenAPI/Swagger Specification Authoring

#### Specification Structure

```yaml
openapi: 3.0.3
info:
  title: [Service Name] API
  description: |
    [2-3 paragraph description of the service, its purpose, and its primary use cases.
    Include links to getting started guides, authentication docs, and support channels.]
  version: 1.0.0
  contact:
    name: API Team
    email: api-team@company.com
    url: https://developer.company.com/support
  license:
    name: Proprietary
    url: https://company.com/legal/api-license

servers:
  - url: https://api.company.com/v1
    description: Production
  - url: https://api-staging.company.com/v1
    description: Staging

security:
  - BearerAuth: []

paths:
  /resources:
    get:
      summary: List all resources
      description: |
        Returns a paginated list of all resources accessible to the authenticated user.
        Supports filtering, sorting, and field selection via query parameters.
      operationId: listResources
      tags:
        - Resources
      parameters:
        - name: page
          in: query
          description: Page number (1-based)
          required: false
          schema:
            type: integer
            minimum: 1
            default: 1
        - name: limit
          in: query
          description: Number of items per page
          required: false
          schema:
            type: integer
            minimum: 1
            maximum: 100
            default: 20
        - name: sort
          in: query
          description: Sort field and direction (e.g., `created_at:desc`)
          required: false
          schema:
            type: string
            pattern: '^[a-z_]+:(asc|desc)$'
        - name: fields
          in: query
          description: Comma-separated list of fields to include in response
          required: false
          schema:
            type: string
      responses:
        '200':
          description: Successful response with paginated resource list
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PaginatedResourceList'
              examples:
                default:
                  $ref: '#/components/examples/ListResourcesResponse'
        '401':
          $ref: '#/components/responses/Unauthorized'
        '403':
          $ref: '#/components/responses/Forbidden'
        '429':
          $ref: '#/components/responses/RateLimited'
      security:
        - BearerAuth: [resources:read]

    post:
      summary: Create a new resource
      description: |
        Creates a new resource with the provided attributes. Returns the created
        resource with server-generated fields (id, created_at, updated_at).
      operationId: createResource
      tags:
        - Resources
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ResourceCreateRequest'
            examples:
              default:
                $ref: '#/components/examples/CreateResourceRequest'
      responses:
        '201':
          description: Resource created successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Resource'
              examples:
                default:
                  $ref: '#/components/examples/CreateResourceResponse'
        '400':
          $ref: '#/components/responses/BadRequest'
        '401':
          $ref: '#/components/responses/Unauthorized'
        '409':
          $ref: '#/components/responses/Conflict'
      security:
        - BearerAuth: [resources:write]

  /resources/{resourceId}:
    get:
      summary: Get a specific resource
      description: Returns a single resource by ID. Returns 404 if not found.
      operationId: getResource
      tags:
        - Resources
      parameters:
        - name: resourceId
          in: path
          required: true
          description: Unique resource identifier (UUID format)
          schema:
            type: string
            format: uuid
      responses:
        '200':
          description: Successful response with resource details
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Resource'
              examples:
                default:
                  $ref: '#/components/examples/GetResourceResponse'
        '404':
          $ref: '#/components/responses/NotFound'
      security:
        - BearerAuth: [resources:read]

    delete:
      summary: Delete a resource
      description: |
        Soft-deletes the specified resource. The resource will be marked as deleted
        and excluded from list queries. Hard deletion occurs after 30 days per
        data retention policy.
      operationId: deleteResource
      tags:
        - Resources
      parameters:
        - name: resourceId
          in: path
          required: true
          schema:
            type: string
            format: uuid
      responses:
        '204':
          description: Resource deleted successfully (no content)
        '404':
          $ref: '#/components/responses/NotFound'
      security:
        - BearerAuth: [resources:delete]

components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
      description: |
        JWT access token obtained from the authentication endpoint.
        Include in the `Authorization` header as `Bearer <token>`.
        Tokens expire after 1 hour. Use refresh tokens to obtain new access tokens.

  schemas:
    Resource:
      type: object
      description: Represents a [resource type] in the system.
      properties:
        id:
          type: string
          format: uuid
          description: Unique resource identifier
          readOnly: true
        name:
          type: string
          description: Human-readable resource name
          minLength: 1
          maxLength: 255
        description:
          type: string
          description: Optional resource description
          maxLength: 1000
        status:
          type: string
          enum: [active, inactive, archived]
          description: Current resource status
          default: active
        created_at:
          type: string
          format: date-time
          description: ISO 8601 timestamp of resource creation
          readOnly: true
        updated_at:
          type: string
          format: date-time
          description: ISO 8601 timestamp of last resource update
          readOnly: true
      required:
        - id
        - name
        - status
        - created_at
        - updated_at

    ResourceCreateRequest:
      type: object
      description: Request body for creating a new resource.
      properties:
        name:
          type: string
          minLength: 1
          maxLength: 255
        description:
          type: string
          maxLength: 1000
        status:
          type: string
          enum: [active, inactive]
          default: active
      required:
        - name

    PaginatedResourceList:
      type: object
      description: Paginated list of resources with metadata.
      properties:
        data:
          type: array
          items:
            $ref: '#/components/schemas/Resource'
        meta:
          type: object
          properties:
            current_page:
              type: integer
            total_pages:
              type: integer
            total_count:
              type: integer
            per_page:
              type: integer
          required:
            - current_page
            - total_pages
            - total_count
            - per_page
        links:
          type: object
          properties:
            self:
              type: string
              format: uri
            first:
              type: string
              format: uri
            last:
              type: string
              format: uri
            next:
              type: string
              format: uri
            prev:
              type: string
              format: uri

  examples:
    ListResourcesResponse:
      value:
        data:
          - id: "550e8400-e29b-41d4-a716-446655440000"
            name: "Example Resource"
            description: "This is an example resource."
            status: "active"
            created_at: "2026-01-15T10:30:00Z"
            updated_at: "2026-01-15T10:30:00Z"
        meta:
          current_page: 1
          total_pages: 3
          total_count: 42
          per_page: 20
        links:
          self: "https://api.company.com/v1/resources?page=1&limit=20"
          first: "https://api.company.com/v1/resources?page=1&limit=20"
          last: "https://api.company.com/v1/resources?page=3&limit=20"
          next: "https://api.company.com/v1/resources?page=2&limit=20"

    CreateResourceRequest:
      value:
        name: "New Resource"
        description: "A newly created resource."

    CreateResourceResponse:
      value:
        id: "550e8400-e29b-41d4-a716-446655440001"
        name: "New Resource"
        description: "A newly created resource."
        status: "active"
        created_at: "2026-04-04T14:00:00Z"
        updated_at: "2026-04-04T14:00:00Z"

    GetResourceResponse:
      value:
        id: "550e8400-e29b-41d4-a716-446655440000"
        name: "Example Resource"
        description: "This is an example resource."
        status: "active"
        created_at: "2026-01-15T10:30:00Z"
        updated_at: "2026-01-15T10:30:00Z"

  responses:
    Unauthorized:
      description: Authentication required. Valid JWT access token not provided.
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            error:
              code: "UNAUTHORIZED"
              message: "Authentication required. Include a valid JWT access token in the Authorization header."
              status: 401

    Forbidden:
      description: Insufficient permissions for this operation.
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            error:
              code: "FORBIDDEN"
              message: "You do not have the required permissions to perform this operation."
              status: 403

    NotFound:
      description: The specified resource was not found.
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            error:
              code: "NOT_FOUND"
              message: "The specified resource does not exist or has been deleted."
              status: 404

    BadRequest:
      description: The request body is invalid. See error details for specifics.
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            error:
              code: "BAD_REQUEST"
              message: "The request body is invalid."
              status: 400
              details:
                - field: "name"
                  issue: "Name is required and cannot be empty."

    Conflict:
      description: The request conflicts with an existing resource.
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            error:
              code: "CONFLICT"
              message: "A resource with this name already exists."
              status: 409

    RateLimited:
      description: Too many requests. Retry after the specified duration.
      headers:
        Retry-After:
          schema:
            type: integer
          description: Seconds to wait before retrying.
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            error:
              code: "RATE_LIMITED"
              message: "Too many requests. Please retry after the specified duration."
              status: 429

  schemas:
    Error:
      type: object
      description: Standard error response structure.
      properties:
        error:
          type: object
          properties:
            code:
              type: string
              description: Machine-readable error code.
            message:
              type: string
              description: Human-readable error description.
            status:
              type: integer
              description: HTTP status code.
            details:
              type: array
              items:
                type: object
                properties:
                  field:
                    type: string
                    description: The field that caused the error.
                  issue:
                    type: string
                    description: Description of the validation issue.
          required:
            - code
            - message
            - status
```

#### OpenAPI Authoring Standards

| Standard                        | Requirement                                                                                             |
| ------------------------------- | ------------------------------------------------------------------------------------------------------- |
| **OpenAPI Version**             | 3.0.3 minimum; 3.1.0 preferred when supported by tooling                                                |
| **Every endpoint documented**   | All paths, methods, parameters, request bodies, and responses must be specified                         |
| **Examples required**           | Every response schema must have at least one example; complex request bodies must have examples         |
| **Error responses complete**    | Document all possible error responses (400, 401, 403, 404, 409, 429, 500) with error codes and messages |
| **Authentication documented**   | Security schemes defined at the component level; per-operation security overrides documented            |
| **Descriptions on every field** | Every schema property has a `description` field. No undocumented fields.                                |
| **Validation constraints**      | Use `minimum`, `maximum`, `minLength`, `maxLength`, `pattern`, `enum` to document validation rules      |
| **Consistent naming**           | Operation IDs use camelCase; tags use PascalCase; parameters use snake_case                             |
| **Version in URL**              | API version included in server URL path (e.g., `/v1/`, `/v2/`)                                          |
| **Lint validation**             | All specs pass `spectral` lint rules before merge; zero warnings or errors                              |

### Endpoint Reference Documentation

#### Endpoint Doc Structure

```markdown
# GET /api/v1/resources
```
