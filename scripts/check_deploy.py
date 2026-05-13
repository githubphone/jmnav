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
    "ls -la /www/wwwroot/jmnav/",
    "ls /www/server/pyporject_evn/jmnav_venv/bin/python*",
    "/www/server/pyporject_evn/jmnav_venv/bin/python --version",
    "/www/server/pyporject_evn/jmnav_venv/bin/pip list 2>/dev/null | grep -iE 'fastapi|uvicorn|gunicorn|starlette|httpx|jinja|bs4|openpyxl'",
    "cat /www/wwwroot/jmnav/main.py | head -10",
    "cat /www/wwwroot/jmnav/scraper.py | head -10",
    "cat /www/wwwroot/jmnav/templates/index.html | head -10",
    "tail -100 /tmp/jmnav.err 2>/dev/null || echo no_err_file",
    "curl -s http://127.0.0.1:8000/ 2>&1 | tail -30",
    "/www/server/pyporject_evn/jmnav_venv/bin/gunicorn --version 2>&1",
]

for cmd in cmds:
    print(f"\n--- {cmd} ---")
    stdin, stdout, stderr = client.exec_command(cmd, timeout=15)
    out = stdout.read().decode("utf-8", errors="replace").strip()
    err = stderr.read().decode("utf-8", errors="replace").strip()
    if out: print(out[:2000])
    if err: print(f"[ERR]{err[:500]}")

client.close()
