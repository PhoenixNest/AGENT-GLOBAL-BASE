class SecurityActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        // Prevent screenshots and screen recording
        window.setFlags(
            WindowManager.LayoutParams.FLAG_SECURE,
            WindowManager.LayoutParams.FLAG_SECURE
        )

        setContentView(R.layout.activity_payment)
    }

    override fun onPause() {
        super.onPause()
        // Clear sensitive data from clipboard
        val clipboard = getSystemService(CLIPBOARD_SERVICE) as ClipboardManager
        clipboard.clearPrimaryClip()
    }
}