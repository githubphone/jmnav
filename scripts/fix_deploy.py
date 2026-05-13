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
    # Fix gunicorn config - change sync to uvicorn worker
    """sed -i "s/worker_class = 'sync'/worker_class = 'uvicorn.workers.UvicornWorker'/" /www/jmnav/gunicorn_conf.py""",

    # Remove threads for uvicorn (uvicorn handles concurrency itself)
    """sed -i "/^threads = /d" /www/jmnav/gunicorn_conf.py""",

    # Make sure data dir exists with right permissions
    "chown -R www:www /www/jmnav/data",
    "chown -R www:www /www/jmnav/static",

    # Show fixed config
    "cat /www/jmnav/gunicorn_conf.py",

    # Restart the project via Baota cli (or direct)
    "kill -HUP $(cat /www/jmnav/gunicorn.pid) 2>/dev/null || systemctl restart jmnav 2>/dev/null || echo restart manually",
]

for cmd in cmds:
    stdin, stdout, stderr = client.exec_command(cmd, timeout=15)
    out = stdout.read().decode("utf-8", errors="replace").strip()
    err = stderr.read().decode("utf-8", errors="replace").strip()
    print(f"\n--- {cmd} ---")
    if out: print(out[:1000])
    if err: print(f"[ERR]{err[:300]}")

client.close()
