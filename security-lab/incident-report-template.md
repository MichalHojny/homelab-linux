# Incident report template

## 1. Summary

Short description of what happened.

## 2. Severity

Low / Medium / High / Critical

## 3. Affected assets

- Host:
- User:
- IP:
- Service:
- Time window:

## 4. Timeline

| Time | Event |
|---|---|
| YYYY-MM-DD HH:MM | First suspicious event |
| YYYY-MM-DD HH:MM | Alert triggered |
| YYYY-MM-DD HH:MM | Analyst review started |
| YYYY-MM-DD HH:MM | Containment action |

## 5. Evidence

Logs, commands, alerts and screenshots used during analysis.

Example commands:

```bash
journalctl -xe
journalctl -u sshd
last
lastb
ss -tulpn
ps aux
docker logs CONTAINER
grep "Failed password" /var/log/auth.log
6. Initial analysis

What the alert indicates.

Questions:

Is it a true positive or false positive?
Is there evidence of compromise?
What user/service was affected?
Was there successful authentication?
Was there unusual outbound traffic?
Were files or services changed?
7. MITRE ATT&CK mapping
ObservationPossible MITRE technique
Failed SSH attemptsBrute Force
New suspicious userCreate Account
Suspicious serviceCreate or Modify System Process
Suspicious cron jobScheduled Task/Job
Unusual outbound connectionCommand and Control
8. Containment

Actions to stop further damage.

Examples:

disable account
block IP
isolate host
stop service
revoke token/key
rotate password
9. Eradication

Actions to remove root cause.

Examples:

remove malicious file
remove unauthorized user
remove persistence
patch vulnerability
fix exposed service
10. Recovery

Actions to return to normal.

Examples:

restart clean service
restore from backup
validate logs
monitor for recurrence
11. Lessons learned

What should be improved:

logging
alerting
firewall rules
access control
patching
documentation
