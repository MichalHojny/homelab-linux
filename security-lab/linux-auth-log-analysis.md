# Linux authentication log analysis

## Goal

Practice basic SOC L1 analysis of Linux authentication events.

## Useful log sources

```bash
journalctl
journalctl -u sshd
journalctl -u ssh
last
lastb
Recent authentication events
sudo journalctl --since "24 hours ago" | grep -Ei "failed|accepted|invalid user|sudo|session|authentication"
SSH logs on Arch
sudo journalctl -u sshd --since "24 hours ago"
SSH logs on Debian/Ubuntu
sudo journalctl -u ssh --since "24 hours ago"
Successful logins
last -a | head -30
sudo journalctl --since "24 hours ago" | grep -Ei "accepted password|accepted publickey"
Failed logins
sudo journalctl --since "24 hours ago" | grep -Ei "failed password|invalid user"
Source IP count
sudo journalctl --since "24 hours ago" \
  | grep -Ei "failed password|invalid user|accepted password|accepted publickey" \
  | grep -Eo 'from ([0-9]{1,3}\.){3}[0-9]{1,3}' \
  | awk '{print $2}' \
  | sort | uniq -c | sort -nr
Sudo activity
sudo journalctl --since "24 hours ago" | grep -i sudo
What to check
Was there a successful login?
Was the source IP expected?
Was the username valid?
Was sudo used after login?
Was a new user created?
Was a new service, cron job or process started?
Is this scanning, brute force or possible compromise?
Basic classification
FindingSeverity
Failed logins only, no successLow
Failed logins from many IPsLow / Medium
Successful login from unknown IPHigh
Successful login + sudoHigh
New user/service/cron after loginCritical
Example conclusion
Multiple failed SSH attempts were observed.
No successful login followed the attempts.
No sudo activity from unknown users was found.
Current classification: low severity internet scanning / brute-force noise.

