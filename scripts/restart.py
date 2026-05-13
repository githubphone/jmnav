import paramiko, os, sys
os.environ["PYTHONIOENCODING"] = "utf-8"
sys.stdout.reconfigure(encoding="utf-8")

HOST = "43.139.221.22"
USER = "root"
PASS = "JIANfeng@10086"

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, 22, USER, PASS, look_for_keys=False, allow_agent=False, timeout=10)

cmds = [
    # Kill old gunicorn and restart
    "kill -9 $(cat /www/jmnav/gunicorn.pid) 2>/dev/null; sleep 1; rm -f /www/jmnav/gunicorn.pid",
    """cd /www/jmnav && /www/server/pyporject_evn/jmnav_venv/bin/gunicorn -c /www/jmnav/gunicorn_conf.py main:app > /tmp/jmnav.log 2>&1 &""",
    "sleep 3 && curl -s -o /dev/null -w 'HTTP %{http_code}' http://127.0.0.1:41234/",
    # Also test with direct python
    "cd /www/jmnav && /www/server/pyporject_evn/jmnav_venv/bin/python3 -c 'from main import app; print(\"Import OK\")' 2>&1",
]

for cmd in cmds:
    stdin, stdout, stderr = client.exec_command(cmd, timeout=20)
    out = stdout.read().decode("utf-8", errors="replace").strip()
    err = stderr.read().decode("utf-8", errors="replace").strip()
    print(f"\n--- {cmd} ---")
    if out: print(out[:1000])
    if err: print(f"[ERR]{err[:300]}")

# Check error log
print("\n--- Error log ---")
stdin, stdout, stderr = client.exec_command("tail -30 /www/wwwlogs/python/jmnav/gunicorn_error.log 2>/dev/null", timeout=10)
out = stdout.read().decode("utf-8", errors="replace").strip()
err = stderr.read().decode("utf-8", errors="replace").strip()
if out: print(out[:2000])
if err: print(f"[ERR]{err[:300]}")

client.close()
