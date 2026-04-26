class SecureFileManager(private val context: Context) {

    // Internal storage — only accessible by this app
    fun saveSensitiveFile(fileName: String, data: ByteArray) {
        context.openFileOutput(fileName, Context.MODE_PRIVATE).use { outputStream ->
            outputStream.write(data)
        }
    }

    fun readSensitiveFile(fileName: String): ByteArray {
        return context.openFileInput(fileName).use { inputStream ->
            inputStream.readBytes()
        }
    }

    fun deleteSensitiveFile(fileName: String) {
        // Secure delete — overwrite before deletion
        val file = File(context.filesDir, fileName)
        if (file.exists()) {
            // Overwrite with random data
            FileOutputStream(file).use { fos ->
                val randomData = ByteArray(file.length().toInt())
                SecureRandom().nextBytes(randomData)
                fos.write(randomData)
                fos.flush()
            }
            file.delete()
        }
    }

    // NEVER use external storage for sensitive data
    // getExternalFilesDir() is acceptable for non-sensitive cached data
    fun saveNonSensitiveCache(fileName: String, data: ByteArray) {
        val cacheDir = context.getExternalFilesDir(null)
        File(cacheDir, fileName).writeBytes(data)
    }
}