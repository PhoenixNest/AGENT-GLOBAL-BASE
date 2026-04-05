# Enterprise Patterns

**Category:** Full-Stack Architecture (Java)
**Owner:** Full-Stack Engineer (Diego Morales)

## Overview

Implements enterprise-grade architectural patterns in Java Spring Boot applications, covering repository pattern implementation, service layer architecture with transaction boundaries, DTO/Entity mapping with MapStruct, validation chains using Hibernate Validator, and audit logging with JPA entity listeners. Ensures clean separation of concerns and maintainable code structure.

## Competency Dimensions

| Dimension                  | Description                                                                               | Proficiency Indicators                                                                                                                                      |
| -------------------------- | ----------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Repository Pattern         | Spring Data JPA repositories, custom queries, specification pattern, pagination           | Designs repository interfaces with type-safe queries; uses Specification for dynamic queries; implements custom repository fragments for complex operations |
| Service Layer Architecture | Transaction management, business logic organization, dependency injection, facade pattern | Designs services with clear transaction boundaries; uses @Transactional appropriately; implements facade pattern for complex workflows                      |
| DTO/Entity Mapping         | MapStruct configuration, nested mapping, collection mapping, custom mappers               | Configures MapStruct with compile-time code generation; handles bidirectional relationships; implements custom type mappers                                 |
| Validation Chains          | Hibernate Validator, custom validators, group validation, cross-field validation          | Builds validation chains with group sequences; implements custom constraint validators; validates cross-field dependencies                                  |
| Audit Logging              | Entity listeners, @CreatedDate/@LastModifiedDate, audit trail tables, soft deletes        | Implements audit fields automatically via entity listeners; maintains separate audit trail for sensitive operations; implements soft delete pattern         |

## Execution Guidance

### Repository Pattern Implementation

```java
// Base repository with common operations
@NoRepositoryBean
public interface BaseRepository<T, ID> extends JpaRepository<T, ID>, JpaSpecificationExecutor<T> {
    // Common methods available to all repositories
}

// Domain-specific repository
public interface OrderRepository extends BaseRepository<Order, UUID> {

    // Derived query methods (simple cases)
    Optional<Order> findByOrderNumber(String orderNumber);
    List<Order> findByUserIdAndStatus(UUID userId, OrderStatus status);
    boolean existsByOrderNumber(String orderNumber);

    // JPQL for complex queries
    @Query("""
        SELECT o FROM Order o
        JOIN FETCH o.items i
        JOIN FETCH i.product p
        WHERE o.user.id = :userId
        AND o.createdAt BETWEEN :from AND :to
        ORDER BY o.createdAt DESC
        """)
    List<Order> findUserOrdersWithItems(
            @Param("userId") UUID userId,
            @Param("from") LocalDateTime from,
            @Param("to") LocalDateTime to);

    // Native query for database-specific features
    @Query(value = """
        SELECT DATE_TRUNC('month', o.created_at) as month,
               COUNT(*) as order_count,
               SUM(o.total_amount) as revenue
        FROM orders o
        WHERE o.created_at >= :from
        GROUP BY DATE_TRUNC('month', o.created_at)
        ORDER BY month
        """, nativeQuery = true)
    List<MonthlyStats> getMonthlyStats(@Param("from") LocalDateTime from);

    // Specification for dynamic queries
    default Specification<Order> withUser(UUID userId) {
        return (root, query, cb) -> cb.equal(root.get("user").get("id"), userId);
    }

    default Specification<Order> withStatus(OrderStatus status) {
        return (root, query, cb) -> cb.equal(root.get("status"), status);
    }

    default Specification<Order> createdAfter(LocalDateTime date) {
        return (root, query, cb) -> cb.greaterThanOrEqualTo(root.get("createdAt"), date);
    }
}

// Service using Specification for dynamic queries
@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class OrderService {

    private final OrderRepository orderRepository;

    public Page<Order> searchOrders(OrderSearchCriteria criteria, Pageable pageable) {
        Specification<Order> spec = Specification.where(null);

        if (criteria.userId() != null) {
            spec = spec.and(orderRepository.withUser(criteria.userId()));
        }
        if (criteria.status() != null) {
            spec = spec.and(orderRepository.withStatus(criteria.status()));
        }
        if (criteria.dateFrom() != null) {
            spec = spec.and(orderRepository.createdAfter(criteria.dateFrom()));
        }
        if (criteria.search() != null) {
            spec = spec.and(withSearch(criteria.search()));
        }

        return orderRepository.findAll(spec, pageable);
    }

    private Specification<Order> withSearch(String search) {
        return (root, query, cb) -> {
            String pattern = "%" + search.toLowerCase() + "%";
            return cb.or(
                cb.like(cb.lower(root.get("orderNumber")), pattern),
                cb.like(cb.lower(root.get("status").as(String.class)), pattern)
            );
        };
    }
}
```

### Service Layer Architecture

```java
// Service with clear transaction boundaries
@Service
@RequiredArgsConstructor
@Slf4j
public class OrderProcessingService {

    private final OrderRepository orderRepository;
    private final PaymentService paymentService;
    private final InventoryService inventoryService;
    private final NotificationService notificationService;
    private final ApplicationEventPublisher eventPublisher;

    // Write operation — requires transaction
    @Transactional
    public Order processOrder(CreateOrderRequest request) {
        log.info("Processing order for user: {}", request.userId());

        // 1. Validate inventory (within transaction)
        for (OrderItemRequest item : request.items()) {
            inventoryService.reserveStock(item.productId(), item.quantity());
        }

        // 2. Create order
        Order order = new Order();
        order.setUser(request.userId());
        order.setItems(mapToOrderItems(request.items()));
        order.calculateTotal();
        order = orderRepository.save(order);

        // 3. Process payment
        try {
            PaymentResult payment = paymentService.charge(
                request.paymentToken(),
                order.getTotalAmount()
            );
            order.setPaymentId(payment.getId());
            order.setStatus(OrderStatus.PAID);
        } catch (PaymentException e) {
            order.setStatus(OrderStatus.PAYMENT_FAILED);
            orderRepository.save(order);
            throw e; // Transaction rolls back, inventory reservation released
        }

        order = orderRepository.save(order);

        // 4. Publish event (after transaction commit via @TransactionalEventListener)
        eventPublisher.publishEvent(new OrderCreatedEvent(order.getId()));

        return order;
    }

    // Read operation — read-only transaction (optimizes DB connection)
    @Transactional(readOnly = true)
    public Order getOrderDetails(UUID orderId) {
        return orderRepository.findById(orderId)
                .orElseThrow(() -> new ResourceNotFoundException("Order", orderId));
    }

    // Complex workflow — use facade pattern
    @Transactional
    public void cancelOrder(UUID orderId, String reason) {
        Order order = orderRepository.findById(orderId)
                .orElseThrow(() -> new ResourceNotFoundException("Order", orderId));

        if (order.getStatus() == OrderStatus.SHIPPED) {
            throw new BusinessException("Cannot cancel shipped order. Use return process instead.");
        }

        if (order.getStatus() == OrderStatus.CANCELLED) {
            throw new BusinessException("Order is already cancelled");
        }

        // Update order status
        order.setStatus(OrderStatus.CANCELLED);
        order.setCancellationReason(reason);
        orderRepository.save(order);

        // Release inventory
        for (OrderItem item : order.getItems()) {
            inventoryService.releaseStock(item.getProduct().getId(), item.getQuantity());
        }

        // Refund payment if applicable
        if (order.getStatus() == OrderStatus.PAID) {
            paymentService.refund(order.getPaymentId());
        }

        // Notify user
        notificationService.sendOrderCancellationNotification(order);
    }
}

// Transaction propagation understanding:
// REQUIRED (default): Join existing or create new
// REQUIRES_NEW: Always create new (suspends existing)
// MANDATORY: Must run within existing transaction
// NOT_SUPPORTED: Run outside transaction (suspends existing)
// NEVER: Must NOT run within transaction
// SUPPORTS: Join if exists, otherwise run without
// NESTED: Savepoint within existing transaction
```

### DTO/Entity Mapping with MapStruct

```java
// MapStruct mapper configuration
@Mapper(
    componentModel = "spring",
    injectionStrategy = InjectionStrategy.CONSTRUCTOR,
    nullValuePropertyMappingStrategy = NullValuePropertyMappingStrategy.IGNORE
)
public interface UserMapper {

    UserMapper INSTANCE = Mappers.getMapper(UserMapper.class);

    // Entity → DTO
    @Mapping(target = "displayName", expression = "java(user.getName() + \" (\" + user.getRole().name() + \")\")")
    @Mapping(target = "orderCount", source = "orders", qualifiedByName = "size")
    UserResponse toResponse(User user);

    List<UserResponse> toResponseList(List<User> users);

    // DTO → Entity (for creation)
    @Mapping(target = "id", ignore = true)
    @Mapping(target = "passwordHash", source = "password")
    @Mapping(target = "orders", ignore = true)
    @Mapping(target = "version", ignore = true)
    @Mapping(target = "createdAt", ignore = true)
    @Mapping(target = "updatedAt", ignore = true)
    User toEntity(CreateUserRequest request);

    // DTO → Entity (for update — only maps non-null fields)
    @BeanMapping(nullValuePropertyMappingStrategy = NullValuePropertyMappingStrategy.IGNORE)
    @Mapping(target = "id", ignore = true)
    @Mapping(target = "orders", ignore = true)
    @Mapping(target = "version", ignore = true)
    @Mapping(target = "createdAt", ignore = true)
    @Mapping(target = "passwordHash", ignore = true)
    void updateEntityFromDto(UpdateUserRequest request, @MappingTarget User user);

    // Nested mapping
    @Mapping(target = "userId", source = "user.id")
    @Mapping(target = "userName", source = "user.name")
    OrderResponse toResponse(Order order);

    // Custom mapping with @Named
    @Named("size")
    default int size(Collection<?> collection) {
        return collection != null ? collection.size() : 0;
    }

    // Custom type mapping
    @Mapping(target = "status", source = "status", qualifiedByName = "orderStatusToString")
    OrderResponse toResponseWithStatus(Order order);

    @Named("orderStatusToString")
    default String orderStatusToString(OrderStatus status) {
        return status != null ? status.name().toLowerCase() : null;
    }
}

// Generated code (compile-time, no reflection overhead):
// @Component
// public class UserMapperImpl implements UserMapper {
//     @Override
//     public UserResponse toResponse(User user) {
//         if (user == null) return null;
//         UserResponse response = new UserResponse();
//         response.setId(user.getId());
//         response.setName(user.getName());
//         // ... all fields mapped
//         return response;
//     }
// }
```

### Validation Chains

```java
// Request DTO with validation annotations
public record CreateOrderRequest(
        @NotNull UUID userId,

        @NotEmpty(message = "At least one item is required")
        @Size(min = 1, max = 50, message = "Order must have 1-50 items")
        List<@Valid OrderItemRequest> items,

        @NotNull(message = "Payment information is required")
        @Valid PaymentRequest payment
) {}

public record OrderItemRequest(
        @NotNull UUID productId,

        @NotNull @Min(value = 1, message = "Quantity must be at least 1")
        @Max(value = 99, message = "Quantity cannot exceed 99")
        Integer quantity
) {}

public record PaymentRequest(
        @NotBlank(message = "Payment token is required")
        @Size(min = 20, max = 500)
        String token,

        @NotNull @Positive(message = "Amount must be positive")
        BigDecimal amount
) {}

// Custom validator
@Target({ElementType.TYPE})
@Retention(RetentionPolicy.RUNTIME)
@Constraint(validatedBy = OrderAmountValidator.class)
public @interface ValidOrderAmount {
    String message() default "Order total does not match item sum";
    Class<?>[] groups() default {};
    Class<? extends Payload>[] payload() default {};
}

public class OrderAmountValidator implements ConstraintValidator<ValidOrderAmount, CreateOrderRequest> {
    @Override
    public boolean isValid(CreateOrderRequest request, ConstraintValidatorContext ctx) {
        if (request == null || request.items() == null) return true;

        BigDecimal itemTotal = request.items().stream()
                .map(item -> item.quantity().multiply(/* price lookup */))
                .reduce(BigDecimal.ZERO, BigDecimal::add);

        boolean valid = itemTotal.compareTo(request.payment().amount()) == 0;

        if (!valid) {
            ctx.disableDefaultConstraintViolation();
            ctx.buildConstraintViolationWithTemplate(
                    "Payment amount (" + request.payment().amount() +
                    ") does not match order total (" + itemTotal + ")"
            ).addPropertyNode("payment.amount").addConstraintViolation();
        }

        return valid;
    }
}

// Validation group sequence (validate in order, stop on failure)
@ValidOrderAmount(groups = OrderAmountCheck.class)
public record CreateOrderRequest(...) {}

// In controller — groups are validated in sequence
@PostMapping
public ResponseEntity<OrderResponse> createOrder(
        @Validated({Default.class, OrderAmountCheck.class})
        @RequestBody CreateOrderRequest request) {
    // ...
}
```

### Audit Logging with Entity Listeners

```java
// Auditable base class
@MappedSuperclass
@EntityListeners(AuditingEntityListener.class)
public abstract class AuditableEntity {

    @CreatedBy
    @Column(name = "created_by", updatable = false)
    private String createdBy;

    @CreatedDate
    @Column(name = "created_at", nullable = false, updatable = false)
    private LocalDateTime createdAt;

    @LastModifiedBy
    @Column(name = "updated_by")
    private String updatedBy;

    @LastModifiedDate
    @Column(name = "updated_at", nullable = false)
    private LocalDateTime updatedAt;

    @Version
    private Long version;
}

// Enable JPA auditing
@Configuration
@EnableJpaAuditing(auditorAwareRef = "springSecurityAuditorAware")
public class JpaAuditingConfig {

    @Bean
    public AuditorAware<String> springSecurityAuditorAware() {
        return () -> SecurityContextHolder.getContext()
                .getAuthentication()
                .map(Authentication::getName)
                .or(() -> Optional.of("system"));
    }
}

// Audit trail table for sensitive operations
@Entity
@Table(name = "audit_log")
public class AuditLog {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    @Column(nullable = false)
    private String entityName;

    @Column(nullable = false)
    private UUID entityId;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private AuditAction action;  // CREATE, UPDATE, DELETE

    @Column(columnDefinition = "jsonb")
    private String beforeState;  // JSON snapshot before change

    @Column(columnDefinition = "jsonb")
    private String afterState;   // JSON snapshot after change

    @Column(nullable = false)
    private String performedBy;

    @Column(nullable = false)
    private LocalDateTime performedAt;
}

// Entity listener for audit trail
@EntityListeners(AuditTrailListener.class)
public class Order extends AuditableEntity {
    // ...
}

public class AuditTrailListener {

    @PersistenceContext
    private EntityManager entityManager;

    @PostPersist
    public void onPostPersist(Object entity) {
        createAuditLog(entity, AuditAction.CREATE, null, entity);
    }

    @PostUpdate
    public void onPostUpdate(Object entity) {
        // In practice, you'd need to capture before state in @PreUpdate
        createAuditLog(entity, AuditAction.UPDATE, null, entity);
    }

    @PostRemove
    public void onPostRemove(Object entity) {
        createAuditLog(entity, AuditAction.DELETE, entity, null);
    }

    private void createAuditLog(Object entity, AuditAction action, Object before, Object after) {
        AuditLog log = new AuditLog();
        log.setEntityName(entity.getClass().getSimpleName());
        log.setEntityId(getEntityId(entity));
        log.setAction(action);
        log.setBeforeState(before != null ? toJson(before) : null);
        log.setAfterState(after != null ? toJson(after) : null);
        log.setPerformedBy(getCurrentUser());
        log.setPerformedAt(LocalDateTime.now());

        entityManager.persist(log);
    }
}

// Soft delete pattern
@Entity
@Table(name = "users")
@SQLRestriction("deleted = false")  // Hibernate 6.x
public class User {

    @Column(nullable = false)
    private boolean deleted = false;

    @Column(name = "deleted_at")
    private LocalDateTime deletedAt;

    @Column(name = "deleted_by")
    private String deletedBy;
}

// Repository for soft-delete entities
public interface UserRepository extends JpaRepository<User, UUID> {

    @Query("SELECT u FROM User u WHERE u.id = :id AND u.deleted = false")
    Optional<User> findActiveById(@Param("id") UUID id);

    @Modifying
    @Query("UPDATE User u SET u.deleted = true, u.deletedAt = CURRENT_TIMESTAMP, u.deletedBy = :deletedBy WHERE u.id = :id")
    int softDelete(@Param("id") UUID id, @Param("deletedBy") String deletedBy);
}
```

## Pipeline Integration

**Stage 5 (Development):** Repository interfaces use Specification for dynamic queries. Service layer has clear transaction boundaries. MapStruct mappers compile-time generated. Validation chains cover all request DTOs. Audit logging automatic via entity listeners.

**Stage 6 (Code Review):** Review transaction boundary correctness (no long-running transactions). Validate MapStruct mapper completeness. Check validation chain coverage. Verify audit logging on sensitive entities.

**Stage 7 (Testing):** Repository tests with @DataJpaTest. Service tests with @Transactional. Validation tests for all constraint violations. Audit log verification tests.

## Quality Standards

| Metric                       | Target                                 | Measurement                   |
| ---------------------------- | -------------------------------------- | ----------------------------- |
| Repository pattern usage     | 100% data access through repositories  | Code review                   |
| Transaction boundary clarity | All write methods have @Transactional  | Code review + static analysis |
| MapStruct mapping coverage   | 100% DTO/Entity mapping via MapStruct  | Code review                   |
| Validation coverage          | 100% request DTOs validated            | Validation test coverage      |
| Audit trail coverage         | 100% sensitive entities audited        | Entity listener audit         |
| N+1 query prevention         | 0 N+1 queries in production            | Query count monitoring        |
| Soft delete implementation   | All deletable entities use soft delete | Code review                   |
