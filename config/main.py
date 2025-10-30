import os
import subprocess

username = os.environ.get('USER')

mc_path = f"/home/{username}/.mc"

try:
    config_fila = f"{mc_path}/code/usr/config.ini"

    subprocess.Popen(["open", config_fila])
except Exception as e:
    print(f"เกิดข้อผิดพลาด: {e}")
