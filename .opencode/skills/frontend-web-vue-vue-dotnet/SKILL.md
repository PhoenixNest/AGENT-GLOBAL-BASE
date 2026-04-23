---
name: frontend-web-vue-vue-dotnet
description: 'Frontend Web skill: Vue Dotnet'
---

# Vue 3 + .NET Integration

**Category:** Full-Stack Engineering (C#/Vue)
**Owner:** Full-Stack Engineer (Marcus Wright)

## Overview

Builds full-stack applications using Vue 3 Composition API frontend with .NET 7+ Minimal APIs backend, covering reactive state management with ref/computed/watch, Entity Framework Core with code-first migrations, multi-tenant architecture patterns, and role-based access control with JWT authentication.

## Competency Dimensions

| Dimension                 | Description                                                                             | Proficiency Indicators                                                                                                                           |
| ------------------------- | --------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| Vue 3 Composition API     | ref, reactive, computed, watch, watchEffect, composables                                | Uses Composition API exclusively (no Options API); designs reusable composables; understands reactivity system internals                         |
| .NET Minimal APIs         | Endpoint routing, parameter binding, result types, filter pipeline                      | Designs RESTful endpoints with Minimal API syntax; implements validation with FluentValidation; uses endpoint filters for cross-cutting concerns |
| Entity Framework Core     | Code-first migrations, relationships, LINQ queries, performance optimization            | Designs entity models with correct relationships; writes efficient LINQ queries; configures migrations for schema evolution                      |
| Multi-Tenant Architecture | Schema-per-tenant, discriminator column, connection string routing, data isolation      | Implements tenant resolution middleware; configures EF Core for tenant isolation; designs migration strategy for multi-tenant schema             |
| Role-Based Access Control | JWT authentication, policy-based authorization, role management, permission granularity | Configures ASP.NET Core Identity with JWT; implements policy-based authorization with requirements; manages role-permission hierarchy            |

## Execution Guidance

### Vue 3 Composition API

```typescript
// Composable for API data fetching
import { ref, computed, watch } from 'vue';
import axios from 'axios';

interface UseEntityOptions<T> {
  apiUrl: string;
  initialData?: T[];
  page?: Ref<number>;
  search?: Ref<string>;
}

export function useEntity<T extends { id: string }>(options: UseEntityOptions<T>) {
  const { apiUrl, initialData = [] } = options;

  const data = ref<T[]>(initialData);
  const loading = ref(false);
  const error = ref<string | null>(null);
  const total = ref(0);

  const page = options.page ?? ref(1);
  const search = options.search ?? ref('');

  const isEmpty = computed(() => data.value.length === 0);
  const pageCount = computed(() => Math.ceil(total.value / 20));

  async function fetchData() {
    loading.value = true;
    error.value = null;

    try {
      const response = await axios.get(apiUrl, {
        params: {
          page: page.value,
          search: search.value,
          page_size: 20,
        },
      });

      data.value = response.data.items;
      total.value = response.data.total;
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to fetch data';
    } finally {
      loading.value = false;
    }
  }

  // Auto-fetch when page or search changes
  watch([page, search], () => {
    fetchData();
  });

  // Fetch on mount
  fetchData();

  return {
    data,
    loading,
    error,
    total,
    isEmpty,
    pageCount,
    page,
    search,
    refetch: fetchData,
  };
}

// Composable for form management
export function useForm<T extends Record<string, any>>(initialValues: T) {
  const values = ref<T>({ ...initialValues });
  const errors = ref<Partial<Record<keyof T, string>>>({});
  const touched = ref<Partial<Record<keyof T, boolean>>>({});
  const isSubmitting = ref(false);

  function setField<K extends keyof T>(key: K, value: T[K]) {
    (values.value as any)[key] = value;
    (touched.value as any)[key] = true;
    // Clear error on change
    delete (errors.value as any)[key];
  }

  function resetForm() {
    values.value = { ...initialValues };
    errors.value = {};
    touched.value = {};
    isSubmitting.value = false;
  }

  async function submit(validationFn: (values: T) => Promise<boolean>,
                        submitFn: (values: T) => Promise<void>) {
    const isValid = await validationFn(values.value);
    if (!isValid) return;

    isSubmitting.value = true;
    try {
      await submitFn(values.value);
    } catch (err: any) {
      errors.value = err.response?.data?.errors || { general: 'Submission failed' };
    } finally {
      isSubmitting.value = false;
    }
  }

  return { values, errors, touched, isSubmitting, setField, resetForm, submit };
}

// Component using composables
<script setup lang="ts">
import { ref, computed } from 'vue';
import { useEntity, useForm } from '@/composables';

interface User {
  id: string;
  name: string;
  email: string;
  role: string;
}

const search = ref('');
const page = ref(1);

const { data: users, loading, error, total, pageCount, refetch } =
  useEntity<User>({
    apiUrl: '/api/users',
    page,
    search,
  });

const form = useForm({
  name: '',
  email: '',
  role: 'user',
});

async function validateUserForm(values: typeof form.values.value) {
  const newErrors: Record<string, string> = {};
  if (!values.name || values.name.length < 2) newErrors.name = 'Name is required';
  if (!values.email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(values.email)) {
    newErrors.email = 'Valid email is required';
  }
  form.errors.value = newErrors;
  return Object.keys(newErrors).length === 0;
}

async function createUser(values: typeof form.values.value) {
  await axios.post('/api/users', values);
  form.resetForm();
  refetch();
}
</script>

<template>
  <div class="users-page">
    <div class="header">
      <input v-model="search" placeholder="Search users..." />
      <button @click="showModal = true">Add User</button>
    </div>

    <div v-if="loading" class="loading">Loading...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else-if="isEmpty" class="empty">No users found</div>
    <div v-else class="user-list">
      <UserCard v-for="user in users" :key="user.id" :user="user" />
    </div>

    <Pagination
      v-if="pageCount > 1"
      :current-page="page"
      :total-pages="pageCount"
      @page-change="page = $event"
    />
  </div>
</template>
```

### .NET 7 Minimal APIs

```csharp
// Program.cs
using Microsoft.EntityFrameworkCore;
using Company.Api;
using Company.Api.Services;
using Company.Api.Repositories;
using Company.Api.Models;
using FluentValidation;
using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.IdentityModel.Tokens;

var builder = WebApplication.CreateBuilder(args);

// Services
builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseNpgsql(builder.Configuration.GetConnectionString("DefaultConnection")));

builder.Services.AddScoped<IUserRepository, UserRepository>();
builder.Services.AddScoped<IUserService, UserService>();

// Validators
builder.Services.AddValidatorsFromAssemblyContaining<Program>();

// Authentication
builder.Services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    .AddJwtBearer(options =>
    {
        options.TokenValidationParameters = new TokenValidationParameters
        {
            ValidateIssuer = true,
            ValidateAudience = true,
            ValidateLifetime = true,
            ValidateIssuerSigningKey = true,
            ValidIssuer = builder.Configuration["Jwt:Issuer"],
            ValidAudience = builder.Configuration["Jwt:Audience"],
            IssuerSigningKey = new SymmetricSecurityKey(
                System.Text.Encoding.UTF8.GetBytes(builder.Configuration["Jwt:Key"]!))
        };
    });

// Authorization policies
builder.Services.AddAuthorizationBuilder()
    .AddPolicy("AdminOnly", policy => policy.RequireRole("Admin"))
    .AddPolicy("UserOrAdmin", policy => policy.RequireRole("User", "Admin"));

var app = builder.Build();

// Middleware pipeline
app.UseHttpsRedirection();
app.UseCors("AllowFrontend");
app.UseAuthentication();
app.UseAuthorization();

// Endpoint group for users
var users = app.MapGroup("/api/users")
    .RequireAuthorization()
    .WithTags("Users");

users.MapGet("/", async (
    IUserService userService,
    int page = 1,
    int pageSize = 20,
    string? search = null) =>
{
    var result = await userService.GetUsersAsync(page, pageSize, search);
    return Results.Ok(result);
})
.RequireAuthorization("UserOrAdmin")
.WithOpenApi();

users.MapGet("/{id:guid}", async (
    Guid id,
    IUserService userService) =>
{
    var user = await userService.GetUserByIdAsync(id);
    return user is not null ? Results.Ok(user) : Results.NotFound();
})
.RequireAuthorization("UserOrAdmin")
.WithOpenApi();

users.MapPost("/", async (
    CreateUserRequest request,
    IUserService userService,
    IValidator<CreateUserRequest> validator) =>
{
    var validationResult = await validator.ValidateAsync(request);
    if (!validationResult.IsValid)
    {
        return Results.ValidationProblem(validationResult.ToDictionary());
    }

    var user = await userService.CreateUserAsync(request);
    return Results.Created($"/api/users/{user.Id}", user);
})
.RequireAuthorization("AdminOnly")
.WithOpenApi();

users.MapPut("/{id:guid}", async (
    Guid id,
    UpdateUserRequest request,
    IUserService userService) =>
{
    var user = await userService.UpdateUserAsync(id, request);
    return user is not null ? Results.Ok(user) : Results.NotFound();
})
.RequireAuthorization("AdminOnly")
.WithOpenApi();

users.MapDelete("/{id:guid}", async (
    Guid id,
    IUserService userService) =>
{
    var deleted = await userService.DeleteUserAsync(id);
    return deleted ? Results.NoContent() : Results.NotFound();
})
.RequireAuthorization("AdminOnly")
.WithOpenApi();

// CORS
app.UseCors("AllowFrontend", policy =>
    policy.WithOrigins("http://localhost:5173", "https://app.company.com")
        .AllowAnyMethod()
        .AllowAnyHeader()
        .AllowCredentials());

app.Run();
```

### Entity Framework Core

```csharp
// Models
public class User
{
    public Guid Id { get; set; } = Guid.NewGuid();
    public string Name { get; set; } = string.Empty;
    public string Email { get; set; } = string.Empty;
    public string PasswordHash { get; set; } = string.Empty;
    public string Role { get; set; } = "User";
    public Guid? TenantId { get; set; }
    public Tenant? Tenant { get; set; }
    public ICollection<Order> Orders { get; set; } = new List<Order>();
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
    public DateTime UpdatedAt { get; set; } = DateTime.UtcNow;
}

public class Order
{
    public Guid Id { get; set; } = Guid.NewGuid();
    public Guid UserId { get; set; }
    public User User { get; set; } = null!;
    public decimal TotalAmount { get; set; }
    public OrderStatus Status { get; set; } = OrderStatus.Pending;
    public ICollection<OrderItem> Items { get; set; } = new List<OrderItem>();
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
}

public class OrderItem
{
    public Guid Id { get; set; } = Guid.NewGuid();
    public Guid OrderId { get; set; }
    public Order Order { get; set; } = null!;
    public Guid ProductId { get; set; }
    public int Quantity { get; set; }
    public decimal UnitPrice { get; set; }
}

// DbContext
public class AppDbContext : DbContext
{
    private readonly ITenantResolver _tenantResolver;

    public AppDbContext(DbContextOptions<AppDbContext> options, ITenantResolver tenantResolver)
        : base(options)
    {
        _tenantResolver = tenantResolver;
    }

    public DbSet<User> Users => Set<User>();
    public DbSet<Order> Orders => Set<Order>();
    public DbSet<OrderItem> OrderItems => Set<OrderItem>();
    public DbSet<Tenant> Tenants => Set<Tenant>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        // Global query filter for multi-tenant (discriminator column approach)
        var currentTenantId = _tenantResolver.GetCurrentTenantId();

        modelBuilder.Entity<User>()
            .HasQueryFilter(u => u.TenantId == currentTenantId);

        modelBuilder.Entity<Order>()
            .HasQueryFilter(o => o.User.TenantId == currentTenantId);

        // Indexes
        modelBuilder.Entity<User>()
            .HasIndex(u => u.Email)
            .IsUnique();

        modelBuilder.Entity<User>()
            .HasIndex(u => u.TenantId);

        modelBuilder.Entity<Order>()
            .HasIndex(o => o.UserId);

        // Relationships
        modelBuilder.Entity<Order>()
            .HasOne(o => o.User)
            .WithMany(u => u.Orders)
            .HasForeignKey(o => o.UserId)
            .OnDelete(DeleteBehavior.Cascade);

        modelBuilder.Entity<OrderItem>()
            .HasOne(oi => oi.Order)
            .WithMany(o => o.Items)
            .HasForeignKey(oi => oi.OrderId)
            .OnDelete(DeleteBehavior.Cascade);
    }
}

// Repository with efficient queries
public class UserRepository : IUserRepository
{
    private readonly AppDbContext _context;

    public UserRepository(AppDbContext context)
    {
        _context = context;
    }

    public async Task<PagedResult<User>> GetUsersAsync(int page, int pageSize, string? search)
    {
        var query = _context.Users.AsQueryable();

        if (!string.IsNullOrWhiteSpace(search))
        {
            query = query.Where(u =>
                u.Name.Contains(search) || u.Email.Contains(search));
        }

        var total = await query.CountAsync();

        var items = await query
            .OrderByDescending(u => u.CreatedAt)
            .Skip((page - 1) * pageSize)
            .Take(pageSize)
            .Select(u => new UserDto
            {
                Id = u.Id,
                Name = u.Name,
                Email = u.Email,
                Role = u.Role,
                CreatedAt = u.CreatedAt,
            })
            .ToListAsync();

        return new PagedResult<UserDto>(items, total, page, pageSize);
    }

    public async Task<User?> GetByIdAsync(Guid id)
    {
        return await _context.Users
            .Include(u => u.Orders)
            .FirstOrDefaultAsync(u => u.Id == id);
    }
}

// Migration commands
// dotnet ef migrations add InitialCreate
// dotnet ef database update
// dotnet ef migrations add AddTenantColumn
// dotnet ef database update
```

### Multi-Tenant Architecture

```csharp
// Tenant resolution middleware
public class TenantMiddleware
{
    private readonly RequestDelegate _next;

    public TenantMiddleware(RequestDelegate next)
    {
        _next = next;
    }

    public async Task InvokeAsync(HttpContext context, AppDbContext dbContext)
    {
        // Extract tenant from subdomain, header, or JWT claim
        var tenantId = ExtractTenantId(context);

        if (tenantId.HasValue)
        {
            context.Items["TenantId"] = tenantId.Value;
        }

        await _next(context);
    }

    private Guid? ExtractTenantId(HttpContext context)
    {
        // Option 1: From JWT claim
        var tenantClaim = context.User.FindFirst("tenant_id");
        if (tenantClaim != null && Guid.TryParse(tenantClaim.Value, out var tenantId))
        {
            return tenantId;
        }

        // Option 2: From header
        if (context.Request.Headers.TryGetValue("X-Tenant-ID", out var headerValue))
        {
            if (Guid.TryParse(headerValue, out var headerTenantId))
            {
                return headerTenantId;
            }
        }

        // Option 3: From subdomain
        var host = context.Request.Host.Host;
        var subdomain = host.Split('.').FirstOrDefault();
        if (!string.IsNullOrEmpty(subdomain))
        {
            // Look up tenant by subdomain
            // This would be cached for performance
        }

        return null;
    }
}

// Tenant resolver service
public interface ITenantResolver
{
    Guid? GetCurrentTenantId();
}

public class TenantResolver : ITenantResolver
{
    private readonly IHttpContextAccessor _httpContextAccessor;

    public TenantResolver(IHttpContextAccessor httpContextAccessor)
    {
        _httpContextAccessor = httpContextAccessor;
    }

    public Guid? GetCurrentTenantId()
    {
        if (_httpContextAccessor.HttpContext?.Items["TenantId"] is Guid tenantId)
        {
            return tenantId;
        }
        return null;
    }
}

// Multi-tenant registration
builder.Services.AddMultiTenant<TenantInfo>()
    .WithHostStrategy()       // tenant1.company.com
    .WithClaimStrategy()      // JWT claim
    .WithHeaderStrategy()     // X-Tenant-ID header
    .WithStaticStore();       // Static tenant configuration
```

### Role-Based Access Control

```csharp
// Policy-based authorization with custom requirements
public class PermissionRequirement : IAuthorizationRequirement
{
    public string Permission { get; }

    public PermissionRequirement(string permission)
    {
        Permission = permission;
    }
}

public class PermissionHandler : AuthorizationHandler<PermissionRequirement>
{
    protected override Task HandleRequirementAsync(
        AuthorizationHandlerContext context,
        PermissionRequirement requirement)
    {
        if (context.User.IsInRole("Admin"))
        {
            context.Succeed(requirement);
            return Task.CompletedTask;
        }

        var userPermissions = context.User.FindAll("permission")
            .Select(c => c.Value);

        if (userPermissions.Contains(requirement.Permission))
        {
            context.Succeed(requirement);
        }

        return Task.CompletedTask;
    }
}

// Registration
builder.Services.AddSingleton<IAuthorizationHandler, PermissionHandler>();

builder.Services.AddAuthorizationBuilder()
    .AddPolicy("CanViewUsers", policy =>
        policy.AddRequirements(new PermissionRequirement("users:view")))
    .AddPolicy("CanEditUsers", policy =>
        policy.AddRequirements(new PermissionRequirement("users:edit")))
    .AddPolicy("CanDeleteUsers", policy =>
        policy.AddRequirements(new PermissionRequirement("users:delete")));

// Usage in endpoints
users.MapGet("/", async (...) => { ... })
    .RequireAuthorization("CanViewUsers");

users.MapPost("/", async (...) => { ... })
    .RequireAuthorization("CanEditUsers");

users.MapDelete("/{id}", async (...) => { ... })
    .RequireAuthorization("CanDeleteUsers");

// Role-permission matrix in database
public class Role
{
    public Guid Id { get; set; }
    public string Name { get; set; } = string.Empty;
    public ICollection<RolePermission> Permissions { get; set; } = new List<RolePermission>();
}

public class RolePermission
{
    public Guid RoleId { get; set; }
    public Role Role { get; set; } = null!;
    public string Permission { get; set; } = string.Empty;
}
```

## Pipeline Integration

**Stage 5 (Development):** Vue 3 components use Composition API. .NET Minimal APIs implement all endpoints. EF Core entities configured with multi-tenant filters. RBAC policies enforced.

**Stage 6 (Code Review):** Review composable reusability. Validate EF Core query efficiency (no N+1). Check multi-tenant data isolation. Verify RBAC coverage.

**Stage 7 (Testing):** Vue component tests with Vitest. API integration tests with WebApplicationFactory. EF Core tests with SQLite in-memory. Multi-tenant isolation tests.

## Quality Standards

| Metric                     | Target                                  | Measurement            |
| -------------------------- | --------------------------------------- | ---------------------- |
| Composition API usage      | 100% new components use Composition API | Code review            |
| Multi-tenant isolation     | 0 cross-tenant data leaks               | Security audit         |
| RBAC coverage              | 100% endpoints have authorization       | Security audit         |
| EF Core query efficiency   | 0 N+1 queries                           | Query count monitoring |
| Vue reactivity correctness | 0 stale data bugs                       | Bug tracking           |
| API response time (p95)    | < 200ms                                 | Application metrics    |
