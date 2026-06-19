"""
一键启动所有后端微服务。
用法：用 .venv 中的 Python 运行此脚本，按 Ctrl+C 停止所有服务。
"""
import subprocess
import sys
import time
import os
import requests

# 确保使用 .venv 中的 Python 解释器
PYTHON = os.path.join(os.path.dirname(__file__), "..", ".venv", "Scripts", "python.exe")
if not os.path.exists(PYTHON):
    # 回退：使用当前进程的 Python
    PYTHON = sys.executable

services = [
    {"name": "RBAC认证服务", "file": "rbac_auth.py", "port": 8001, "health": "http://localhost:8001/rbac/health"},
    {"name": "AI主服务",     "file": "main.py",      "port": 8000},
    {"name": "任务管理服务", "file": "task_management.py", "port": 8002},
    {"name": "评价报告服务", "file": "court_evaluation_backend.py", "port": 8003},
    {"name": "案件管理服务", "file": "case_model.py", "port": 8004},
]

processes = []

print("=" * 50)
print("  模拟法庭 - 启动所有后端服务")
print("=" * 50)

try:
    for svc in services:
        print(f"\n[{svc['name']}] 启动中（端口 {svc['port']}）...")
        file_path = os.path.join(os.path.dirname(__file__), svc["file"])
        proc = subprocess.Popen(
            [PYTHON, file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        processes.append((svc["name"], proc))
        time.sleep(2)

        # 健康检查（如果定义了 health URL）
        if "health" in svc:
            healthy = False
            for attempt in range(10):
                try:
                    r = requests.get(svc["health"], timeout=2)
                    if r.status_code == 200:
                        print(f"  [OK] {svc['name']} ready (attempt {attempt + 1})")
                        healthy = True
                        break
                except Exception:
                    pass
                time.sleep(1)
            if not healthy:
                print(f"  [WARN] {svc['name']} health check not responding, may still be starting")

    print("\n" + "=" * 50)
    print("  所有服务已启动！按 Ctrl+C 停止")
    print("=" * 50)

    # 等待所有进程
    for name, proc in processes:
        proc.wait()

except KeyboardInterrupt:
    print("\n\n正在停止所有服务...")
    for name, proc in processes:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
        print(f"  [STOP] {name} stopped")
    print("所有服务已关闭。")
