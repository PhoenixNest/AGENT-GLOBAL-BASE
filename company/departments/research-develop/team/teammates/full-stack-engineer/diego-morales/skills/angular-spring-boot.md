# Angular + Spring Boot

**Category:** Full-Stack Engineering (Java/Angular)
**Owner:** Full-Stack Engineer (Diego Morales)

## Overview

Delivers enterprise full-stack applications using Angular frontend with Spring Boot backend, covering Angular component architecture with signals and standalone components, Spring Boot REST controllers with exception handling, JPA/Hibernate entity mapping with relationships, Spring Security with OAuth2 and JWT authentication, and Docker deployment with multi-stage builds.

## Competency Dimensions

| Dimension                      | Description                                                                     | Proficiency Indicators                                                                                                                                                       |
| ------------------------------ | ------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Angular Component Architecture | Standalone components, signals, input/output, lifecycle, change detection       | Uses standalone components (no NgModules); leverages signals for reactive state; implements OnPush change detection; designs component hierarchy with clear responsibilities |
| Spring Boot REST Controllers   | Request mapping, path variables, request bodies, validation, exception handling | Designs RESTful controllers with proper HTTP semantics; uses Bean Validation; implements global exception handling with @ControllerAdvice                                    |
| JPA/Hibernate Entity Mapping   | Entity relationships, fetch strategies, cascade types, optimistic locking       | Designs entity graphs with correct fetch types (LAZY vs EAGER); implements optimistic locking with @Version; avoids N+1 queries with @EntityGraph                            |
| Spring Security                | OAuth2 resource server, JWT validation, method security, CORS configuration     | Configures Spring Security for JWT-based auth; implements @PreAuthorize method security; configures CORS for Angular frontend                                                |
| Docker Deployment              | Multi-stage builds, layer optimization, health checks, non-root user            | Writes production Dockerfiles with multi-stage builds; optimizes image layers; configures health checks; runs as non-root user                                               |

## Execution Guidance

### Angular Component Architecture

**Standalone component with signals:**

```typescript
// user-list.component.ts
import { Component, signal, computed, inject, OnInit } from "@angular/core";
import { CommonModule } from "@angular/common";
import { UserCardComponent } from "./user-card.component";
import { UserService } from "../services/user.service";
import { User } from "../models/user.model";

@Component({
  selector: "app-user-list",
  standalone: true,
  imports: [CommonModule, UserCardComponent],
  template: `
    <div class="user-list">
      @if (isLoading()) {
        <app-loading-spinner />
      } @else if (error()) {
        <app-error-message [message]="error()!" />
      } @else {
        @for (user of filteredUsers(); track user.id) {
          <app-user-card [user]="user" (selected)="onUserSelected($event)" />
        } @empty {
          <p>No users found</p>
        }
      }
    </div>
  `,
  styles: [
    `
      .user-list {
        display: grid;
        gap: 1rem;
      }
    `,
  ],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class UserListComponent implements OnInit {
  private userService = inject(UserService);

  // Signals for reactive state
  users = signal<User[]>([]);
  isLoading = signal<boolean>(false);
  error = signal<string | null>(null);
  searchQuery = signal<string>("");

  // Computed signal for derived state
  filteredUsers = computed(() => {
    const query = this.searchQuery().toLowerCase();
    if (!query) return this.users();
    return this.users().filter(
      (u) =>
        u.name.toLowerCase().includes(query) ||
        u.email.toLowerCase().includes(query),
    );
  });

  async ngOnInit(): Promise<void> {
    this.isLoading.set(true);
    try {
      const data = await this.userService.getUsers().toPromise();
      this.users.set(data ?? []);
    } catch (err) {
      this.error.set("Failed to load users");
    } finally {
      this.isLoading.set(false);
    }
  }

  onUserSelected(userId: string): void {
    // Navigate or emit
  }
}
```

**Signal-based state management pattern:**

```typescript
// user.store.ts — lightweight state management with signals
import { Injectable, signal, computed } from "@angular/core";
import { User } from "../models/user.model";

interface UserState {
  users: User[];
  selectedUserId: string | null;
  isLoading: boolean;
  error: string | null;
}

@Injectable({ providedIn: "root" })
export class UserStore {
  private state = signal<UserState>({
    users: [],
    selectedUserId: null,
    isLoading: false,
    error: null,
  });

  // Selectors (computed signals)
  users = computed(() => this.state().users);
  selectedUser = computed(() => {
    const userId = this.state().selectedUserId;
    if (!userId) return null;
    return this.state().users.find((u) => u.id === userId) ?? null;
  });
  isLoading = computed(() => this.state().isLoading);
  error = computed(() => this.state().error);

  // Updaters
  setUsers(users: User[]): void {
    this.state.update((s) => ({ ...s, users }));
  }

  setSelectedUserId(id: string | null): void {
    this.state.update((s) => ({ ...s, selectedUserId: id }));
  }

  setLoading(isLoading: boolean): void {
    this.state.update((s) => ({ ...s, isLoading }));
  }

  setError(error: string | null): void {
    this.state.update((s) => ({ ...s, error }));
  }
}
```

### Spring Boot REST Controllers

```java
@RestController
@RequestMapping("/api/users")
@Validated
@RequiredArgsConstructor
public class UserController {

    private final UserService userService;
    private final UserMapper userMapper;

    @GetMapping
    public ResponseEntity<Page<UserResponse>> getUsers(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "20") int size,
            @RequestParam(required = false) String search) {

        Pageable pageable = PageRequest.of(page, size, Sort.by("createdAt").descending());
        Page<User> users;

        if (search != null && !search.isBlank()) {
            users = userService.searchUsers(search, pageable);
        } else {
            users = userService.findAllUsers(pageable);
        }

        return ResponseEntity.ok(users.map(userMapper::toResponse));
    }

    @GetMapping("/{id}")
    public ResponseEntity<UserResponse> getUser(@PathVariable UUID id) {
        User user = userService.getUserById(id)
                .orElseThrow(() -> new ResourceNotFoundException("User", id));
        return ResponseEntity.ok(userMapper.toResponse(user));
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public ResponseEntity<UserResponse> createUser(
            @Valid @RequestBody CreateUserRequest request) {

        User user = userService.createUser(userMapper.toEntity(request));

        URI location = ServletUriComponentsBuilder.fromCurrentRequest()
                .path("/{id}")
                .buildAndExpand(user.getId())
                .toUri();

        return ResponseEntity.created(location)
                .body(userMapper.toResponse(user));
    }

    @PutMapping("/{id}")
    public ResponseEntity<UserResponse> updateUser(
            @PathVariable UUID id,
            @Valid @RequestBody UpdateUserRequest request) {

        User user = userService.updateUser(id, userMapper.toEntity(request));
        return ResponseEntity.ok(userMapper.toResponse(user));
    }

    @DeleteMapping("/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void deleteUser(@PathVariable UUID id) {
        userService.deleteUser(id);
    }
}

// Request DTOs with Bean Validation
public record CreateUserRequest(
        @NotBlank @Size(min = 2, max = 100) String name,
        @NotBlank @Email @Size(max = 255) String email,
        @NotBlank @Size(min = 12, max = 128) String password,
        @NotNull UserRole role
) {}

// Global exception handler
@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(ResourceNotFoundException.class)
    public ResponseEntity<ErrorResponse> handleNotFound(ResourceNotFoundException ex) {
        ErrorResponse error = new ErrorResponse(
                "RESOURCE_NOT_FOUND",
                ex.getMessage(),
                HttpStatus.NOT_FOUND.value()
        );
        return ResponseEntity.status(HttpStatus.NOT_FOUND).body(error);
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<ValidationErrorResponse> handleValidation(
            MethodArgumentNotValidException ex) {

        Map<String, String> fieldErrors = ex.getBindingResult().getFieldErrors().stream()
                .collect(Collectors.toMap(
                        FieldError::getField,
                        fe -> fe.getDefaultMessage() != null ? fe.getDefaultMessage() : "Invalid value"
                ));

        ValidationErrorResponse error = new ValidationErrorResponse(
                "VALIDATION_ERROR",
                "Request validation failed",
                fieldErrors
        );
        return ResponseEntity.badRequest().body(error);
    }

    @ExceptionHandler(DataIntegrityViolationException.class)
    public ResponseEntity<ErrorResponse> handleConflict(DataIntegrityViolationException ex) {
        return ResponseEntity.status(HttpStatus.CONFLICT)
                .body(new ErrorResponse("CONFLICT", "Resource already exists", HttpStatus.CONFLICT.value()));
    }
}
```

### JPA/Hibernate Entity Mapping

```java
@Entity
@Table(name = "users", indexes = {
    @Index(name = "idx_users_email", columnList = "email", unique = true)
})
@NamedEntityGraph(name = "User.withOrders",
    attributeNodes = @NamedAttributeNode("orders"))
public class User {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    @Column(nullable = false, length = 100)
    private String name;

    @Column(nullable = false, unique = true, length = 255)
    private String email;

    @Column(name = "password_hash", nullable = false)
    private String passwordHash;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 20)
    private UserRole role = UserRole.USER;

    @OneToMany(mappedBy = "user", cascade = CascadeType.ALL, orphanRemoval = true,
               fetch = FetchType.LAZY)
    private List<Order> orders = new ArrayList<>();

    @Version  // Optimistic locking
    private Long version;

    @CreationTimestamp
    @Column(name = "created_at", nullable = false, updatable = false)
    private LocalDateTime createdAt;

    @UpdateTimestamp
    @Column(name = "updated_at", nullable = false)
    private LocalDateTime updatedAt;

    // Helper methods for bidirectional relationship
    public void addOrder(Order order) {
        orders.add(order);
        order.setUser(this);
    }

    public void removeOrder(Order order) {
        orders.remove(order);
        order.setUser(null);
    }
}

@Entity
@Table(name = "orders")
public class Order {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id", nullable = false)
    private User user;

    @Column(name = "total_amount", nullable = false)
    private BigDecimal totalAmount;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 20)
    private OrderStatus status = OrderStatus.PENDING;

    @OneToMany(mappedBy = "order", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<OrderItem> items = new ArrayList<>();

    @Version
    private Long version;
}

// Repository with EntityGraph to prevent N+1
public interface UserRepository extends JpaRepository<User, UUID> {

    @EntityGraph(value = "User.withOrders", type = EntityGraph.EntityGraphType.LOAD)
    Optional<User> findById(UUID id);

    Page<User> findByNameContainingIgnoreCase(String search, Pageable pageable);
}

// Service layer — avoids N+1
@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class UserService {

    private final UserRepository userRepository;

    public Page<User> findAllUsers(Pageable pageable) {
        return userRepository.findAll(pageable);
    }

    @Transactional
    public User createUser(User user) {
        // Check unique constraint
        if (userRepository.existsByEmail(user.getEmail())) {
            throw new DuplicateResourceException("User with email already exists");
        }
        user.setPasswordHash(passwordEncoder.encode(user.getPasswordHash()));
        return userRepository.save(user);
    }
}
```

### Spring Security with OAuth2/JWT

```java
@Configuration
@EnableWebSecurity
@EnableMethodSecurity(prePostEnabled = true)
public class SecurityConfig {

    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        http
            .csrf(csrf -> csrf.disable())
            .cors(cors -> cors.configurationSource(corsConfigurationSource()))
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/api/auth/**", "/api/public/**").permitAll()
                .requestMatchers("/api/admin/**").hasRole("ADMIN")
                .requestMatchers("/h2-console/**").permitAll()
                .anyRequest().authenticated()
            )
            .oauth2ResourceServer(oauth2 -> oauth2
                .jwt(jwt -> jwt
                    .jwtAuthenticationConverter(jwtAuthenticationConverter())
                )
            )
            .sessionManagement(session -> session
                .sessionCreationPolicy(SessionCreationPolicy.STATELESS)
            );

        return http.build();
    }

    @Bean
    public CorsConfigurationSource corsConfigurationSource() {
        CorsConfiguration config = new CorsConfiguration();
        config.setAllowedOrigins(List.of("http://localhost:4200", "https://app.company.com"));
        config.setAllowedMethods(List.of("GET", "POST", "PUT", "DELETE", "OPTIONS"));
        config.setAllowedHeaders(List.of("Authorization", "Content-Type", "X-Request-ID"));
        config.setAllowCredentials(true);
        config.setMaxAge(3600L);

        UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
        source.registerCorsConfiguration("/api/**", config);
        return source;
    }

    @Bean
    public JwtAuthenticationConverter jwtAuthenticationConverter() {
        JwtGrantedAuthoritiesConverter grantedAuthoritiesConverter = new JwtGrantedAuthoritiesConverter();
        grantedAuthoritiesConverter.setAuthorityPrefix("ROLE_");
        grantedAuthoritiesConverter.setAuthoritiesClaimName("roles");

        JwtAuthenticationConverter jwtAuthenticationConverter = new JwtAuthenticationConverter();
        jwtAuthenticationConverter.setJwtGrantedAuthoritiesConverter(grantedAuthoritiesConverter);
        return jwtAuthenticationConverter;
    }
}

// Method-level security
@Service
public class OrderService {

    @PreAuthorize("hasRole('ADMIN') or #userId == authentication.principal.id")
    public List<Order> getUserOrders(UUID userId) {
        // Only admin or the user themselves can access
        return orderRepository.findByUserId(userId);
    }

    @PreAuthorize("hasRole('ADMIN')")
    public void deleteOrder(UUID orderId) {
        orderRepository.deleteById(orderId);
    }
}
```

### Docker Deployment

```dockerfile
# Backend — Multi-stage build
FROM eclipse-temurin:21-jdk-alpine AS builder
WORKDIR /app
COPY .mvn/ .mvn
COPY mvnw pom.xml ./
RUN ./mvnw dependency:go-offline -B
COPY src ./src
RUN ./mvnw clean package -DskipTests

FROM eclipse-temurin:21-jre-alpine
RUN addgroup -g 1001 appgroup && adduser -u 1001 -G appgroup -s /bin/sh -D appuser
WORKDIR /app
COPY --from=builder /app/target/*.jar app.jar
USER appuser
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:8080/actuator/health || exit 1
ENTRYPOINT ["java", "-jar", "app.jar"]

# Frontend — Multi-stage build
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --frozen-lockfile
COPY . .
RUN npm run build -- --configuration=production

FROM nginx:alpine
COPY --from=builder /app/dist/*/browser /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
    CMD curl -f http://localhost/ || exit 1
```

## Pipeline Integration

**Stage 5 (Development):** Angular components use standalone architecture with signals. Spring Boot controllers follow RESTful conventions. JPA entities configured with correct fetch strategies. Security configured with JWT validation.

**Stage 6 (Code Review):** Review component architecture for proper separation. Validate entity fetch strategies (no EAGER on collections). Check security configuration. Verify DTO mapping completeness.

**Stage 7 (Testing):** Angular component tests with signals. Spring Boot integration tests with @DataJpaTest and @WebMvcTest. Security tests for authorization rules.

## Quality Standards

| Metric               | Target                                         | Measurement             |
| -------------------- | ---------------------------------------------- | ----------------------- |
| Component standalone | 100% new components are standalone             | Code review             |
| Signal usage         | 100% reactive state uses signals               | Code review             |
| JPA fetch strategy   | 0 EAGER collections                            | Static analysis         |
| N+1 query prevention | All list queries use EntityGraph or JOIN FETCH | Query count monitoring  |
| Security coverage    | All endpoints have authorization               | Security audit          |
| Docker image size    | < 200MB for backend, < 50MB for frontend       | Image size check        |
| Health check         | All services have health endpoints             | Health check monitoring |
