import paramiko
import sys

HOST = "43.139.221.22"
PORT = 22
USER = "root"
PASSWORD = "JIANfeng@10086"

commands = [
    # Check OS and Python
    "cat /etc/os-release | head -3",
    "python3 --version 2>&1 || echo 'NO_PYTHON'",
    "python3.12 --version 2>&1 || echo 'NO_PYTHON312'",
    "pip3 --version 2>&1 || echo 'NO_PIP'",
    "git --version 2>&1 || echo 'NO_GIT'",
    "which bt 2>&1 || echo 'NO_BT'",
]

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
    client.connect(HOST, PORT, USER, PASSWORD, look_for_keys=False, allow_agent=False, timeout=10)
    print("=== Connected to server ===")
    for cmd in commands:
        stdin, stdout, stderr = client.exec_command(cmd)
        out = stdout.read().decode().strip()
        err = stderr.read().decode().strip()
        print(f"\n$ {cmd}")
        if out:
            print(out)
        if err:
            print(err)
except Exception as e:
    print(f"ERROR: {e}")
finally:
    client.close()
