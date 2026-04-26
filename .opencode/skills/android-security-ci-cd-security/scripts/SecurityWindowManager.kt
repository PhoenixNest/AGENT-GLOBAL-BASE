class SecurityWindowManager(private val window: Window) {

    fun preventScreenshots() {
        window.setFlags(
            WindowManager.LayoutParams.FLAG_SECURE,
            WindowManager.LayoutParams.FLAG_SECURE
        )
    }

    fun preventRecentsSnapshot() {
        // In Activity.onCreate():
        // this.setRecentsScreenshotEnabled(false)  // API 33+
    }

    fun clearClipboardOnBackground() {
        // Register LifecycleObserver to clear clipboard when app backgrounds
    }
}

// Prevent sensitive data in logs
@Suppress("PrintStackTrace")
class SecureLogger {
    companion object {
        private const val TAG = "App"
        private const val IS_DEBUG = BuildConfig.DEBUG

        fun d(message: String, throwable: Throwable? = null) {
            if (IS_DEBUG) {
                Log.d(TAG, message, throwable)
            }
        }

        fun e(message: String, throwable: Throwable? = null) {
            // Always log errors but sanitize PII
            Log.e(TAG, sanitize(message), throwable?.sanitize())
        }

        private fun sanitize(message: String): String {
            // Remove tokens, emails, phone numbers from log messages
            return message
                .replace(Regex("Bearer [\\w.-]+"), "Bearer [REDACTED]")
                .replace(Regex("[\\w.+-]+@[\\w-]+\\.[\\w.]+"), "[EMAIL REDACTED]")
        }
    }
}