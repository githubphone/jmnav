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
    "ls -la /www/jmnav/",
    "cat /www/jmnav/gunicorn_conf.py",
    "cat /www/jmnav/main.py | head -30",
    "ls /www/jmnav/templates/ 2>/dev/null || echo no templates",
    "ls /www/jmnav/static/ 2>/dev/null || echo no static",
    "cat /www/jmnav/scraper.py | head -30",
    "ls /www/jmnav/data/ 2>/dev/null && cat /www/jmnav/data/site_data.json 2>/dev/null | head -10 || echo no data",
    "ls /www/jmnav/systems.json 2>/dev/null && cat /www/jmnav/systems.json | head -10 || echo no systems",
    "/www/server/pyporject_evn/jmnav_venv/bin/python -c 'import fastapi; from main import app; print(\"Import OK\")' 2>&1",
]

for cmd in cmds:
    stdin, stdout, stderr = client.exec_command(cmd, timeout=15)
    out = stdout.read().decode("utf-8", errors="replace").strip()
    err = stderr.read().decode("utf-8", errors="replace").strip()
    print(f"\n--- {cmd} ---")
    if out: print(out[:2000])
    if err: print(f"[ERR]{err[:500]}")

client.close()
