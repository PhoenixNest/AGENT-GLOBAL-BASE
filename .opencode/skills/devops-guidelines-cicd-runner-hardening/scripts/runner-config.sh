#!/bin/bash
set -euo pipefail
# 1. Isolated runner user
useradd --system --shell /usr/sbin/nologin --home /opt/actions-runner gh-runner
# 2. Ephemeral runner
echo -e "EPHEMERAL=true\nRUNNER_ALLOW_RUNASROOT=false" > /opt/actions-runner/.env
# 3. Network restrictions (allow only required endpoints)
iptables -A OUTPUT -d api.github.com -j ACCEPT
iptables -A OUTPUT -d vault.company.internal -j ACCEPT
iptables -A OUTPUT -j DROP
# 4. Filesystem restrictions
chmod 700 /opt/actions-runner
chown gh-runner:gh-runner /opt/actions-runner
# 5. Auto cleanup after job
find /opt/actions-runner/_work -mindepth 1 -delete 2>/dev/null
shred -u /tmp/* 2>/dev/null || true