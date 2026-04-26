object InputValidator {

    // Email validation — RFC 5322 simplified
    private val EMAIL_PATTERN = Pattern.compile(
        "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
    )

    // Name validation — Unicode letters, spaces, hyphens, apostrophes
    private val NAME_PATTERN = Pattern.compile("^[\\p{L}\\s\\-']{1,100}$")

    // Username validation — alphanumeric, underscores, 3-20 chars
    private val USERNAME_PATTERN = Pattern.compile("^[a-zA-Z0-9_]{3,20}$")

    fun validateEmail(email: String): Result<String> {
        return when {
            email.isBlank() -> Result.failure(ValidationError("Email is required"))
            !EMAIL_PATTERN.matcher(email).matches() ->
                Result.failure(ValidationError("Invalid email format"))
            else -> Result.success(email.trim().lowercase())
        }
    }

    fun validateName(name: String): Result<String> {
        return when {
            name.isBlank() -> Result.failure(ValidationError("Name is required"))
            !NAME_PATTERN.matcher(name).matches() ->
                Result.failure(ValidationError("Name contains invalid characters"))
            else -> Result.success(name.trim())
        }
    }

    fun validateUsername(username: String): Result<String> {
        return when {
            username.isBlank() -> Result.failure(ValidationError("Username is required"))
            !USERNAME_PATTERN.matcher(username).matches() ->
                Result.failure(ValidationError("Username must be 3-20 alphanumeric characters or underscores"))
            else -> Result.success(username.trim().lowercase())
        }
    }

    // Sanitize HTML to prevent XSS in WebViews
    fun sanitizeHtml(input: String): String {
        return input
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace("\"", "&quot;")
            .replace("'", "&#x27;")
    }

    // Validate URL for deep links — prevent open redirect
    private val ALLOWED_SCHEMES = setOf("https")
    private val ALLOWED_HOSTS = setOf("example.com", "www.example.com")

    fun validateDeepLink(uri: Uri): Result<Uri> {
        return when {
            uri.scheme !in ALLOWED_SCHEMES ->
                Result.failure(ValidationError("Invalid scheme: ${uri.scheme}"))
            uri.host !in ALLOWED_HOSTS ->
                Result.failure(ValidationError("Untrusted host: ${uri.host}"))
            else -> Result.success(uri)
        }
    }
}

// Sealed error type
@JvmInline
value class ValidationError(val message: String) : Exception(message)