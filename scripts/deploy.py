import paramiko
import sys
import os

os.environ["PYTHONIOENCODING"] = "utf-8"

HOST = "43.139.221.22"
PORT = 22
USER = "root"
PASSWORD = "JIANfeng@10086"
PROJECT_DIR = "/www/wwwroot/jmnav"

sys.stdout.reconfigure(encoding="utf-8")

def ssh_cmd(client, cmd, timeout=120):
    print(f"\n>>> {cmd}")
    stdin, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    exit_code = stdout.channel.recv_exit_status()
    out = stdout.read().decode("utf-8", errors="replace").strip()
    err = stderr.read().decode("utf-8", errors="replace").strip()
    if out:
        print(out[:2000])
        if len(out) > 2000:
            print("... (truncated)")
    if err:
        print(f"[STDERR] {err[:1000]}")
    return exit_code, out, err


client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, PORT, USER, PASSWORD, look_for_keys=False, allow_agent=False, timeout=10)
print("=== Connected to server ===")

steps = [
    # Fix CentOS 7 repos (EOL -> vault)
    ('sed -i "s|mirror.centos.org|vault.epel.cloud|g; s|#baseurl=http://mirror.centos.org|baseurl=http://vault.epel.cloud|g; s|baseurl=http://mirror.centos.org|baseurl=http://vault.epel.cloud|g" /etc/yum.repos.d/C* /etc/yum.repos.d/epel* 2>/dev/null; yum clean all', 30),

    # Install build deps for Python
    ("yum install -y gcc make openssl-devel bzip2-devel libffi-devel zlib-devel readline-devel sqlite-devel wget xz-devel", 180),

    # Download and build Python 3.12
    ("cd /tmp && wget -q https://www.python.org/ftp/python/3.12.10/Python-3.12.10.tgz && tar xzf Python-3.12.10.tgz", 120),
    ("cd /tmp/Python-3.12.10 && ./configure --enable-optimizations --prefix=/usr/local/python312 && make -j$(nproc) && make altinstall", 600),

    # Add to PATH
    ('export PATH=/usr/local/python312/bin:$PATH && python3.12 --version', 10),
    ('/usr/local/python312/bin/pip3.12 install --upgrade pip setuptools', 60),
]

for cmd, t in steps:
    try:
        code, out, err = ssh_cmd(client, cmd, timeout=t)
        if code != 0:
            print(f"[WARN] Exit code: {code}")
    except Exception as e:
        print(f"[ERROR] {e}")

# Now deploy the project
PYTHON = "/usr/local/python312/bin/python3.12"
PIP = "/usr/local/python312/bin/pip3.12"

deploy_steps = [
    # Install git
    ("yum install -y git", 60),

    # Clone repo
    (f"cd /www/wwwroot && rm -rf jmnav && git clone https://github.com/githubphone/jmnav.git", 60),

    # Create venv
    (f"cd {PROJECT_DIR} && {PYTHON} -m venv .venv", 30),
    (f"cd {PROJECT_DIR} && .venv/bin/pip install --upgrade pip setuptools wheel", 60),
    (f"cd {PROJECT_DIR} && .venv/bin/pip install -r requirements.txt", 180),

    # Test
    (f"cd {PROJECT_DIR} && .venv/bin/python -c 'from main import app; print(\"App loaded OK\")'", 30),

    # Create systemd service
    (f"""cat > /etc/systemd/system/jmnav.service << 'EOF'
[Unit]
Description=zhihui zhujian FastAPI
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory={PROJECT_DIR}
ExecStart={PROJECT_DIR}/.venv/bin/gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 127.0.0.1:8000
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF""", 10),

    # Start service
    ("systemctl daemon-reload", 10),
    ("systemctl enable jmnav", 10),
    ("systemctl start jmnav", 10),
    ("sleep 3 && systemctl status jmnav --no-pager -l | head -20", 10),
]

for cmd, t in deploy_steps:
    try:
        code, out, err = ssh_cmd(client, cmd, timeout=t)
        if code != 0:
            print(f"[WARN] Exit code: {code}")
    except Exception as e:
        print(f"[ERROR] {e}")

# Final check
print("\n=== Final check ===")
ssh_cmd(client, "curl -s -o /dev/null -w 'HTTP %{http_code}' http://127.0.0.1:8000/", timeout=10)
ssh_cmd(client, "systemctl is-active jmnav", timeout=5)

client.close()
print("\n=== Deployment script finished ===")
