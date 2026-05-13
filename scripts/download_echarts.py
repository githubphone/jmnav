import paramiko, os, sys, io
os.environ["PYTHONIOENCODING"] = "utf-8"
sys.stdout.reconfigure(encoding="utf-8")

HOST = "43.139.221.22"
USER = "root"
PASS = "JIANfeng@10086"

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, 22, USER, PASS, look_for_keys=False, allow_agent=False, timeout=10)

# Download echarts from bootcdn (accessible in China) and save to server
cmd = "curl -sL -o /www/jmnav/static/js/echarts.min.js https://cdn.bootcdn.net/ajax/libs/echarts/5.5.0/echarts.min.js"
stdin, stdout, stderr = client.exec_command(cmd, timeout=120)
stdout.channel.recv_exit_status()
err = stderr.read().decode("utf-8", errors="replace").strip()
out = stdout.read().decode("utf-8", errors="replace").strip()

# Check
cmd2 = "ls -la /www/jmnav/static/js/echarts.min.js && wc -c /www/jmnav/static/js/echarts.min.js"
stdin2, stdout2, stderr2 = client.exec_command(cmd2, timeout=15)
out2 = stdout2.read().decode("utf-8", errors="replace").strip()
err2 = stderr2.read().decode("utf-8", errors="replace").strip()

print(f"Download result: {out[:200] if out else 'OK'}")
if err: print(f"ERR: {err[:300]}")
print(f"\nFile check:\n{out2[:200]}")
if err2: print(f"ERR2: {err2[:300]}")

client.close()
