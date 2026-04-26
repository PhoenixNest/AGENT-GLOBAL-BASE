// commonMain — declare the interface
expect class PlatformClock {
    fun nowMillis(): Long
}

// androidMain — Android implementation
actual class PlatformClock {
    actual fun nowMillis() = System.currentTimeMillis()
}

// iosMain — iOS implementation
actual class PlatformClock {
    actual fun nowMillis() = NSDate().timeIntervalSince1970.toLong() * 1000
}