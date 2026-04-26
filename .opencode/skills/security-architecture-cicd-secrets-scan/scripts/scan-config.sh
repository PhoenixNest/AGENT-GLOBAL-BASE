# Scan entire git history for leaked secrets
trufflehog git https://github.com/org/repo --only-verified --json > history-scan.json
# Rotate any confirmed secrets immediately