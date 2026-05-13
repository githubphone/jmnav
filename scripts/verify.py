import paramiko, os, sys
os.environ["PYTHONIOENCODING"] = "utf-8"
sys.stdout.reconfigure(encoding="utf-8")

HOST = "43.139.221.22"
USER = "root"
PASS = "JIANfeng@10086"

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, 22, USER, PASS, look_for_keys=False, allow_agent=False, timeout=10)

# Check HTML for chart containers and scripts
stdin, stdout, stderr = client.exec_command("""curl -s http://127.0.0.1:41234/ | grep -E '(chartFund|chartHousing|chartDistrict|statCards|dashboard\\.js|echarts\\.min\\.js)'""", timeout=15)
out = stdout.read().decode("utf-8", errors="replace").strip()
err = stderr.read().decode("utf-8", errors="replace").strip()
print("=== Chart references in HTML ===")
if out: print(out)
if err: print(f"ERR: {err[:300]}")

# Check if echarts.min.js is accessible
stdin2, stdout2, stderr2 = client.exec_command("curl -s -o /dev/null -w 'ECHARTS: %{http_code}' http://127.0.0.1:41234/static/js/echarts.min.js", timeout=15)
out2 = stdout2.read().decode("utf-8", errors="replace").strip()
err2 = stderr2.read().decode("utf-8", errors="replace").strip()
print(f"\n=== Static files ===")
if out2: print(out2)
if err2: print(f"ERR2: {err2[:300]}")

# Check gunicorn error log for Python errors
stdin3, stdout3, stderr3 = client.exec_command("tail -30 /www/wwwlogs/python/jmnav/gunicorn_error.log 2>/dev/null", timeout=10)
out3 = stdout3.read().decode("utf-8", errors="replace").strip()
if out3:
    lines = out3.split("\n")
    # Show only ERROR lines
    errors = [l for l in lines if "ERROR" in l or "Traceback" in l or "Error" in l]
    if errors:
        print(f"\n=== Recent errors ===")
        for e in errors[-5:]:
            print(e)

client.close()
