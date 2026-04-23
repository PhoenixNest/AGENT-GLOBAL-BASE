---
name: cross-platform-flutter-flutter-architecture
description: "Cross Platform skill: Flutter Architecture"
---

# Flutter Architecture

**Category:** Mobile Engineering — Cross-Platform (Flutter)
**Owner:** Cross-Platform Engineer (Fatima Al-Zahra)

## Overview

This skill implements production-grade Flutter application architecture covering widget tree optimization, BLoC state management, Riverpod for dependency injection, navigation architecture, and platform channel integration. It applies to Stage 5 (Development) where Flutter apps are built with scalable architecture, Stage 6 (Code Review) where widget composition and state management correctness are audited, and Stage 8 (Integrity Verification) where the CDO verifies IDS specifications are realized in Flutter implementation.

## Competency Dimensions

| Dimension                | Description                                                                                                   | Proficiency Indicators                                                                                                 |
| ------------------------ | ------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| Widget Tree Architecture | Widget/Element/RenderObject tree, const constructors, key management, widget lifecycle                        | Widget tree is optimized with const; keys used correctly for list items; build methods are pure and fast               |
| BLoC Pattern             | Event-State transformation, Cubit vs BLoC, BlocBuilder/BlocListener, event debouncing, state equality         | BLoCs are pure event processors; states are Equatable; UI reacts only to state changes; no business logic in widgets   |
| Riverpod                 | Provider types (Provider, StateProvider, StateNotifierProvider, FutureProvider), provider families, ref.watch | Providers are scoped appropriately; provider families for parameterized providers; ref.watch for reactive dependencies |
| Navigation               | GoRouter, declarative routing, nested navigation, deep linking, route guards, transition customization        | Navigation is declarative; deep links handled correctly; route guards for auth; nested navigators for tab screens      |
| Platform Channels        | MethodChannel, EventChannel, BasicMessageChannel, platform-specific implementation, error handling            | Platform channels are typed; errors propagate correctly; async platform calls don't block UI; channel setup is lazy    |

## Execution Guidance

### BLoC Pattern — Production Implementation

```dart
// MARK: - Event

abstract class UserListEvent extends Equatable {
  const UserListEvent();

  @override
  List<Object?> get props => [];
}

class UserListStarted extends UserListEvent {}

class UserListRefreshRequested extends UserListEvent {}

class UserListUserDeleted extends UserListEvent {
  final String userId;
  const UserListUserDeleted(this.userId);

  @override
  List<Object?> get props => [userId];
}

class UserListSearchChanged extends UserListEvent {
  final String query;
  const UserListSearchChanged(this.query);

  @override
  List<Object?> get props => [query];
}

// MARK: - State

class UserListState extends Equatable {
  final List<User> users;
  final bool isLoading;
  final bool isRefreshing;
  final String? errorMessage;
  final String searchQuery;

  const UserListState({
    this.users = const [],
    this.isLoading = false,
    this.isRefreshing = false,
    this.errorMessage,
    this.searchQuery = '',
  });

  UserListState copyWith({
    List<User>? users,
    bool? isLoading,
    bool? isRefreshing,
    String? errorMessage,
    String? searchQuery,
  }) {
    return UserListState(
      users: users ?? this.users,
      isLoading: isLoading ?? this.isLoading,
      isRefreshing: isRefreshing ?? this.isRefreshing,
      errorMessage: errorMessage,
      searchQuery: searchQuery ?? this.searchQuery,
    );
  }

  bool get hasUsers => users.isNotEmpty;
  bool get isEmptyState => !isLoading && users.isEmpty && errorMessage == null;

  @override
  List<Object?> get props => [users, isLoading, isRefreshing, errorMessage, searchQuery];
}

// MARK: - BLoC

class UserListBloc extends Bloc<UserListEvent, UserListState> {
  final GetUserListUseCase getUserList;
  final DeleteUserUseCase deleteUser;
  Timer? _searchDebounce;

  UserListBloc({
    required this.getUserList,
    required this.deleteUser,
  }) : super(const UserListState()) {
    on<UserListStarted>(_onStarted);
    on<UserListRefreshRequested>(_onRefreshRequested);
    on<UserListUserDeleted>(_onUserDeleted);
    on<UserListSearchChanged>(_onSearchChanged);
  }

  Future<void> _onStarted(
    UserListStarted event,
    Emitter<UserListState> emit,
  ) async {
    emit(state.copyWith(isLoading: true, errorMessage: null));
    try {
      final users = await getUserList();
      emit(state.copyWith(users: users, isLoading: false));
    } catch (e) {
      emit(state.copyWith(
        isLoading: false,
        errorMessage: e.toString(),
      ));
    }
  }

  Future<void> _onRefreshRequested(
    UserListRefreshRequested event,
    Emitter<UserListState> emit,
  ) async {
    emit(state.copyWith(isRefreshing: true));
    try {
      final users = await getUserList();
      emit(state.copyWith(users: users, isRefreshing: false));
    } catch (e) {
      emit(state.copyWith(
        isRefreshing: false,
        errorMessage: e.toString(),
      ));
    }
  }

  Future<void> _onUserDeleted(
    UserListUserDeleted event,
    Emitter<UserListState> emit,
  ) async {
    try {
      await deleteUser(event.userId);
      final updatedUsers = state.users.where((u) => u.id != event.userId).toList();
      emit(state.copyWith(users: updatedUsers));
    } catch (e) {
      emit(state.copyWith(errorMessage: e.toString()));
    }
  }

  void _onSearchChanged(
    UserListSearchChanged event,
    Emitter<UserListState> emit,
  ) {
    _searchDebounce?.cancel();
    _searchDebounce = Timer(const Duration(milliseconds: 300), () {
      // Trigger search with debounced query
      add(_UserListSearchExecuted(event.query));
    });
  }

  @override
  Future<void> close() {
    _searchDebounce?.cancel();
    return super.close();
  }
}

// MARK: - UI Integration

class UserListScreen extends StatelessWidget {
  const UserListScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return BlocProvider(
      create: (context) => UserListBloc(
        getUserList: context.read<GetUserListUseCase>(),
        deleteUser: context.read<DeleteUserUseCase>(),
      )..add(const UserListStarted()),
      child: const UserListView(),
    );
  }
}

class UserListView extends StatelessWidget {
  const UserListView({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Users'),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: () {
              context.read<UserListBloc>().add(const UserListRefreshRequested());
            },
          ),
        ],
      ),
      body: BlocBuilder<UserListBloc, UserListState>(
        builder: (context, state) {
          if (state.isLoading) {
            return const Center(child: CircularProgressIndicator());
          }

          if (state.errorMessage != null) {
            return Center(
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  const Icon(Icons.error_outline, size: 48, color: Colors.red),
                  const SizedBox(height: 16),
                  Text(state.errorMessage!),
                  const SizedBox(height: 16),
                  ElevatedButton(
                    onPressed: () {
                      context.read<UserListBloc>().add(const UserListStarted());
                    },
                    child: const Text('Retry'),
                  ),
                ],
              ),
            );
          }

          if (state.isEmptyState) {
            return const Center(child: Text('No users found'));
          }

          return RefreshIndicator(
            onRefresh: () async {
              context.read<UserListBloc>().add(const UserListRefreshRequested());
            },
            child: ListView.builder(
              itemCount: state.users.length,
              itemBuilder: (context, index) {
                final user = state.users[index];
                return UserListTile(user: user);
              },
            ),
          );
        },
      ),
    );
  }
}

class UserListTile extends StatelessWidget {
  final User user;
  const UserListTile({super.key, required this.user});

  @override
  Widget build(BuildContext context) {
    return ListTile(
      leading: CircleAvatar(child: Text(user.initials)),
      title: Text(user.name),
      subtitle: Text(user.email),
      trailing: IconButton(
        icon: const Icon(Icons.delete),
        onPressed: () {
          context.read<UserListBloc>().add(UserListUserDeleted(user.id));
        },
      ),
    );
  }
}
```

### Riverpod — Dependency Injection & State

```dart
// MARK: - Provider Definitions

// Simple value provider
final apiClientProvider = Provider<ApiClient>((ref) {
  return ApiClient(baseUrl: 'https://api.example.com');
});

// Repository provider (depends on other providers)
final userRepositoryProvider = Provider<UserRepository>((ref) {
  final apiClient = ref.watch(apiClientProvider);
  return UserRepositoryImpl(apiClient: apiClient);
});

// Use case provider
final getUserListUseCaseProvider = Provider<GetUserListUseCase>((ref) {
  final repository = ref.watch(userRepositoryProvider);
  return GetUseCase(repository);
});

// StateNotifierProvider for complex state
final userListNotifierProvider =
    StateNotifierProvider<UserListNotifier, UserListState>((ref) {
  final repository = ref.watch(userRepositoryProvider);
  return UserListNotifier(repository);
});

// Provider family for parameterized providers
final userProvider = FutureProvider.family<User, String>((ref, userId) {
  final repository = ref.watch(userRepositoryProvider);
  return repository.getUser(userId);
});

// Async notifier (Riverpod 2.0+)
@riverpod
class UserDetail extends _$UserDetail {
  @override
  Future<User> build(String userId) async {
    final repository = ref.watch(userRepositoryProvider);
    return repository.getUser(userId);
  }

  Future<void> refresh() async {
    state = const AsyncValue.loading();
    state = await AsyncValue.guard(() async {
      final repository = ref.read(userRepositoryProvider);
      return repository.getUser(userId);
    });
  }
}

// MARK: - Usage in Widget

class UserDetailScreen extends ConsumerWidget {
  final String userId;
  const UserDetailScreen({super.key, required this.userId});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final userAsync = ref.watch(userProvider(userId));

    return Scaffold(
      appBar: AppBar(title: const Text('User Detail')),
      body: userAsync.when(
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (error, stack) => Center(child: Text('Error: $error')),
        data: (user) => UserDetailView(user: user),
      ),
    );
  }
}

// MARK: - Riverpod vs BLoC Decision

// Use BLoC when:
// - Complex event-driven state machines
// - Need event debouncing, throttling, transformation
// - Team has BLoC experience
// - Need detailed event/state tracing

// Use Riverpod when:
// - Simple state management with dependency injection
// - Need provider composition and caching
// - Want less boilerplate
// - Async data fetching with built-in loading/error states

// Company standard: BLoC for complex feature state, Riverpod for DI and simple state
```

### Navigation — GoRouter

```dart
// MARK: - Router Configuration

final routerConfig = GoRouter(
  initialLocation: '/splash',
  redirect: (context, state) {
    final auth = context.read<AuthBloc>().state;
    final isAuth = auth is Authenticated;
    final isLoggingIn = state.matchedLocation == '/login';

    if (!isAuth && !isLoggingIn) {
      return '/login';
    }

    if (isAuth && isLoggingIn) {
      return '/home';
    }

    return null;
  },
  routes: [
    GoRoute(
      path: '/splash',
      builder: (context, state) => const SplashScreen(),
    ),
    GoRoute(
      path: '/login',
      builder: (context, state) => const LoginScreen(),
    ),
    ShellRoute(
      builder: (context, state, child) => MainShell(child: child),
      routes: [
        GoRoute(
          path: '/home',
          builder: (context, state) => const HomeScreen(),
        ),
        GoRoute(
          path: '/users',
          builder: (context, state) => const UserListScreen(),
          routes: [
            GoRoute(
              path: ':userId',
              builder: (context, state) {
                final userId = state.pathParameters['userId']!;
                return UserDetailScreen(userId: userId);
              },
            ),
          ],
        ),
        GoRoute(
          path: '/settings',
          builder: (context, state) => const SettingsScreen(),
        ),
      ],
    ),
  ],
  errorBuilder: (context, state) => const ErrorScreen(),
);

// MARK: - Deep Link Handling

// Configure in AndroidManifest.xml and Info.plist
// Android: intent-filter with BROWSABLE category
// iOS: Associated Domains with applinks:

// MARK: - Nested Navigation (Tab Screen)

class MainShell extends StatelessWidget {
  final Widget child;
  const MainShell({super.key, required this.child});

  @override
  Widget build(BuildContext context) {
    final state = GoRouterState.of(context);
    final currentIndex = _getTabIndex(state.matchedLocation);

    return Scaffold(
      body: child,
      bottomNavigationBar: NavigationBar(
        selectedIndex: currentIndex,
        destinations: const [
          NavigationDestination(icon: Icon(Icons.home), label: 'Home'),
          NavigationDestination(icon: Icon(Icons.people), label: 'Users'),
          NavigationDestination(icon: Icon(Icons.settings), label: 'Settings'),
        ],
        onDestinationSelected: (index) {
          final routes = ['/home', '/users', '/settings'];
          context.go(routes[index]);
        },
      ),
    );
  }

  int _getTabIndex(String location) {
    if (location.startsWith('/home')) return 0;
    if (location.startsWith('/users')) return 1;
    if (location.startsWith('/settings')) return 2;
    return 0;
  }
}
```

### Platform Channels

```dart
// MARK: - Flutter Side

class SecureStorage {
  static const _channel = MethodChannel('com.example.app/secure_storage');

  Future<void> write({required String key, required String value}) async {
    try {
      await _channel.invokeMethod('write', {'key': key, 'value': value});
    } on PlatformException catch (e) {
      throw SecureStorageException(e.code, e.message);
    }
  }

  Future<String?> read({required String key}) async {
    try {
      final result = await _channel.invokeMethod<String>('read', {'key': key});
      return result;
    } on PlatformException catch (e) {
      throw SecureStorageException(e.code, e.message);
    }
  }

  Future<void> delete({required String key}) async {
    try {
      await _channel.invokeMethod('delete', {'key': key});
    } on PlatformException catch (e) {
      throw SecureStorageException(e.code, e.message);
    }
  }
}

class SecureStorageException implements Exception {
  final String code;
  final String? message;
  const SecureStorageException(this.code, this.message);

  @override
  String toString() => 'SecureStorageException($code): $message';
}

// MARK: - EventChannel for Streaming

class BatteryStream {
  static const _channel = EventChannel('com.example.app/battery_level');

  Stream<double> get batteryLevel {
    return _channel.receiveBroadcastStream().map((event) => event as double);
  }
}

// MARK: - Android Side (Kotlin)

/*
class MainActivity : FlutterActivity() {
    private val secureStorage = SecureStorage()

    override fun configureFlutterEngine(flutterEngine: FlutterEngine) {
        super.configureFlutterEngine(flutterEngine)

        MethodChannel(flutterEngine.dartExecutor.binaryMessenger, "com.example.app/secure_storage")
            .setMethodCallHandler { call, result ->
                when (call.method) {
                    "write" -> {
                        val key = call.argument<String>("key")
                        val value = call.argument<String>("value")
                        if (key == null || value == null) {
                            result.error("INVALID_ARGS", "Key and value required", null)
                        } else {
                            secureStorage.write(key, value)
                            result.success(null)
                        }
                    }
                    "read" -> {
                        val key = call.argument<String>("key")
                        if (key == null) {
                            result.error("INVALID_ARGS", "Key required", null)
                        } else {
                            result.success(secureStorage.read(key))
                        }
                    }
                    "delete" -> {
                        val key = call.argument<String>("key")
                        if (key == null) {
                            result.error("INVALID_ARGS", "Key required", null)
                        } else {
                            secureStorage.delete(key)
                            result.success(null)
                        }
                    }
                    else -> result.notImplemented()
                }
            }
    }
}
*/

// MARK: - iOS Side (Swift)

/*
class AppDelegate: FlutterAppDelegate {
    private let secureStorage = SecureStorage()

    override func application(
        _ application: UIApplication,
        didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?
    ) -> Bool {
        let controller = window?.rootViewController as! FlutterViewController
        let channel = FlutterMethodChannel(
            name: "com.example.app/secure_storage",
            binaryMessenger: controller.binaryMessenger
        )

        channel.setMethodCallHandler { [weak self] call, result in
            guard let self = self else { return }

            switch call.method {
            case "write":
                guard let args = call.arguments as? [String: Any],
                      let key = args["key"] as? String,
                      let value = args["value"] as? String else {
                    result(FlutterError(code: "INVALID_ARGS", message: "Key and value required", details: nil))
                    return
                }
                self.secureStorage.write(key: key, value: value)
                result(nil)

            case "read":
                guard let args = call.arguments as? [String: Any],
                      let key = args["key"] as? String else {
                    result(FlutterError(code: "INVALID_ARGS", message: "Key required", details: nil))
                    return
                }
                result(self.secureStorage.read(key: key))

            case "delete":
                guard let args = call.arguments as? [String: Any],
                      let key = args["key"] as? String else {
                    result(FlutterError(code: "INVALID_ARGS", message: "Key required", details: nil))
                    return
                }
                self.secureStorage.delete(key: key)
                result(nil)

            default:
                result(FlutterMethodNotImplemented)
            }
        }

        return super.application(application, didFinishLaunchingWithOptions: launchOptions)
    }
}
*/
```

## Pipeline Integration

- **Stage 3 (Architecture):** ADR establishes Flutter architecture pattern (BLoC vs Riverpod), navigation strategy, and platform channel contracts.
- **Stage 5 (Development):** Primary skill for Flutter app development. All widgets, BLoCs, providers, navigation, and platform channels.
- **Stage 6 (Code Review):** Architecture review: BLoC purity, widget composition efficiency, provider correctness, platform channel error handling.
- **Stage 8 (Integrity Verification):** CDO verifies IDS specifications are realized. Widget tree performance profiled.

## Quality Standards

- **100%** BLoCs are pure event processors — no business logic in widgets
- All states are **Equatable** — efficient rebuild detection
- Widget build methods are **pure and fast** — no side effects, no network calls
- **const constructors** used wherever possible — widget tree optimization
- GoRouter used for **declarative navigation** — no imperative Navigator.push
- Deep links handled via **GoRouter redirect** — proper auth guards
- Platform channels are **typed and error-handled** — PlatformException caught and translated
- BLoC events are **debounced** where appropriate (search, text input)
- Provider scoping is **correct** — no over-scoped or under-scoped providers
- Widget keys used correctly — **ValueKey** for typed items, **PageStorageKey** for scroll state
- Platform channel calls are **async** — never block Flutter UI thread
