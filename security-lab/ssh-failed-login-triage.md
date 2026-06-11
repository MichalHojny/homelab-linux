# SSH failed login triage

Goal: document a simple SOC L1 workflow for failed SSH login alerts.

## Alert

Example alert:

```text
Multiple failed SSH login attempts detected on Linux host.
Step 1 - Check recent SSH logs

Arch:

sudo journalctl -u sshd --since "2 hours ago"

Debian/Ubuntu:

sudo journalctl -u ssh --since "2 hours ago"

Generic search:

sudo journalctl --since "2 hours ago" | grep -Ei "sshd|failed password|invalid user|accepted"
Step 2 - Count failed usernames
sudo journalctl --since "24 hours ago" | grep -Ei "failed password|invalid user" | awk '{print $0}' | head -50
Step 3 - Check successful logins
last -a | head -30
sudo journalctl --since "24 hours ago" | grep -Ei "accepted password|accepted publickey"
Step 4 - Check source IPs
sudo journalctl --since "24 hours ago" | grep -Ei "failed password|invalid user|accepted" | grep -Eo 'from ([0-9]{1,3}\.){3}[0-9]{1,3}' | sort | uniq -c | sort -nr
Step 5 - Check post-login activity
sudo journalctl --since "24 hours ago" | grep -Ei "sudo|session opened|useradd|passwd|systemctl|cron"
Step 6 - Classification
ResultClassification
Failed attempts only, no successful loginLow / scanning
Failed attempts followed by successful login from unknown IPHigh
Successful login + sudo activityHigh
New user/service/cron after loginCritical
Known admin IP and expected timeFalse positive / expected activity
Step 7 - Response

Low severity:

Document source IPs, usernames and time window.
No containment needed if no successful login.
Consider rate limiting or fail2ban.

High severity:

Disable affected account.
Block source IP.
Rotate password/SSH keys.
Check sudo activity.
Check persistence.
Escalate.
Evidence to collect
time window
host
source IP
username
failed/successful login count
authentication method
sudo activity
running services
network connections

