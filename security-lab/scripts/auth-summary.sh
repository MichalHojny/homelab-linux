#!/usr/bin/env bash
set -euo pipefail

echo "=== Auth summary: last 24h ==="
echo

echo "=== Failed / invalid SSH attempts ==="
sudo journalctl --since "24 hours ago" 2>/dev/null \
  | grep -Ei "failed password|invalid user" \
  | tail -30 || true

echo
echo "=== Successful SSH logins ==="
sudo journalctl --since "24 hours ago" 2>/dev/null \
  | grep -Ei "accepted password|accepted publickey" \
  | tail -30 || true

echo
echo "=== Source IP count from auth events ==="
sudo journalctl --since "24 hours ago" 2>/dev/null \
  | grep -Ei "failed password|invalid user|accepted password|accepted publickey" \
  | grep -Eo 'from ([0-9]{1,3}\.){3}[0-9]{1,3}' \
  | awk '{print $2}' \
  | sort \
  | uniq -c \
  | sort -nr || true

echo
echo "=== Recent sudo activity ==="
sudo journalctl --since "24 hours ago" 2>/dev/null \
  | grep -i sudo \
  | tail -30 || true

echo
echo "=== Recent logins ==="
last -a | head -20 || true
