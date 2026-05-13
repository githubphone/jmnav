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
    "curl -s http://127.0.0.1:41234/static/js/dashboard.js 2>/dev/null | head -30",
    "curl -s http://127.0.0.1:41234/ 2>/dev/null | grep -oE 'dashboard\\.js|echarts' | sort -u",
    "curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:41234/static/js/dashboard.js",
    "curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:41234/static/data/dashboard.json",
]

for cmd in cmds:
    stdin, stdout, stderr = client.exec_command(cmd, timeout=15)
    out = stdout.read().decode("utf-8", errors="replace").strip()
    err = stderr.read().decode("utf-8", errors="replace").strip()
    print(f"\n--- {cmd} ---")
    if out: print(out[:2000])
    if err: print(f"[ERR]{err[:300]}")

client.close()
