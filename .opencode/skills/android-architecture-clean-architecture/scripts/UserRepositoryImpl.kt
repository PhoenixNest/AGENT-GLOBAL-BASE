// Domain layer defines the contract
interface UserRepository {
    suspend fun getUser(id: String): Result<User, DomainError>
    suspend fun updateUser(user: User): Result<Unit, DomainError>
}

// Data layer implements the contract
class UserRepositoryImpl(
    private val api: UserApi,
    private val dao: UserDao,
    private val mapper: UserMapper
) : UserRepository {
    override suspend fun getUser(id: String): Result<User, DomainError> = ...
    override suspend fun updateUser(user: User): Result<Unit, DomainError> = ...
}

// DI module binds interface to implementation
@Module
@InstallIn(SingletonComponent::class)
abstract class RepositoryModule {
    @Binds
    abstract fun bindUserRepository(impl: UserRepositoryImpl): UserRepository
}