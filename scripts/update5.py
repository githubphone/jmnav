import paramiko, os, sys
os.environ["PYTHONIOENCODING"] = "utf-8"
sys.stdout.reconfigure(encoding="utf-8")

HOST = "43.139.221.22"
USER = "root"
PASS = "JIANfeng@10086"

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, 22, USER, PASS, look_for_keys=False, allow_agent=False, timeout=10)

for cmd in [
    "cd /www/jmnav && git pull",
    "chown www:www /www/jmnav/static/js/echarts.min.js /www/jmnav/static/js/dashboard.js",
    "kill -HUP $(cat /www/jmnav/gunicorn.pid 2>/dev/null) 2>/dev/null; sleep 2",
    "curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:41234/",
]:
    stdin, stdout, stderr = client.exec_command(cmd, timeout=30)
    out = stdout.read().decode("utf-8", errors="replace").strip()
    err = stderr.read().decode("utf-8", errors="replace").strip()
    print(f"\n--- {cmd} ---")
    if out: print(out[:500])
    if err: print(f"[ERR]{err[:200]}")

client.close()
