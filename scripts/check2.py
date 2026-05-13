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
    "find /www -name 'main.py' 2>/dev/null",
    "ls -la /www/wwwroot/",
    "/www/server/pyporject_evn/jmnav_venv/bin/pip3.12 list 2>/dev/null",
    "ls /www/server/pyporject_evn/jmnav_venv/lib/python3.12/site-packages/ | grep -E 'fastapi|uvicorn|starlette|jinja|httpx|bs4|openpyxl' 2>/dev/null",
    "ps aux | grep gunicorn | grep -v grep",
]

for cmd in cmds:
    stdin, stdout, stderr = client.exec_command(cmd, timeout=15)
    out = stdout.read().decode("utf-8", errors="replace").strip()
    err = stderr.read().decode("utf-8", errors="replace").strip()
    print(f"\n--- {cmd} ---")
    if out: print(out[:2000])
    if err: print(f"[ERR]{err[:300]}")

client.close()
