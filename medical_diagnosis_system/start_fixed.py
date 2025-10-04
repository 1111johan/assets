#!/usr/bin/env python3
"""
修复版启动脚本 - 解决前端Streamlit错误
"""

import os
import sys
import subprocess
import time
import signal
import psutil

def kill_existing_processes():
    """杀死现有的服务进程"""
    print("🔄 清理现有服务进程...")
    
    # 杀死占用8000和8501端口的进程
    for port in [8000, 8501]:
        try:
            for proc in psutil.process_iter(['pid', 'name', 'connections']):
                try:
                    for conn in proc.info['connections']:
                        if conn.laddr.port == port:
                            print(f"   终止端口{port}上的进程: {proc.info['name']} (PID: {proc.info['pid']})")
                            proc.terminate()
                            proc.wait(timeout=5)
                except (psutil.NoSuchProcess, psutil.AccessDenied, AttributeError):
                    pass
        except Exception as e:
            print(f"   清理端口{port}时出错: {e}")
    
    time.sleep(2)

def start_backend():
    """启动后端服务"""
    print("🚀 启动后端API服务...")
    
    # 设置环境变量
    env = os.environ.copy()
    env["DASHSCOPE_API_KEY"] = "sk-57a7c48444c74ccc8173024d9288e625"
    
    # 启动FastAPI后端
    backend_cmd = [
        sys.executable, "-c",
        """
import uvicorn
from main import app
print('后端服务启动中...')
uvicorn.run(app, host='0.0.0.0', port=8000, log_level='info')
"""
    ]
    
    backend_process = subprocess.Popen(
        backend_cmd,
        env=env,
        cwd=os.getcwd(),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True
    )
    
    # 等待后端启动
    print("   等待后端服务启动...")
    time.sleep(5)
    
    # 检查后端是否启动成功
    import requests
    try:
        response = requests.get("http://127.0.0.1:8000/", timeout=5)
        if response.status_code == 200:
            print("✅ 后端服务启动成功")
        else:
            print("❌ 后端服务启动失败")
            return None
    except:
        print("❌ 后端服务连接失败")
        return None
    
    return backend_process

def start_frontend():
    """启动前端服务"""
    print("🌐 启动前端Streamlit服务...")
    
    # 设置环境变量
    env = os.environ.copy()
    env["STREAMLIT_BROWSER_GATHER_USAGE_STATS"] = "false"
    env["STREAMLIT_SERVER_HEADLESS"] = "true"
    
    # 启动Streamlit前端
    frontend_cmd = [
        sys.executable, "-m", "streamlit", "run", "app.py",
        "--server.port", "8501",
        "--server.headless", "true",
        "--browser.gatherUsageStats", "false",
        "--server.enableCORS", "false",
        "--server.enableXsrfProtection", "false",
        "--client.showErrorDetails", "false"
    ]
    
    frontend_process = subprocess.Popen(
        frontend_cmd,
        env=env,
        cwd=os.getcwd(),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True
    )
    
    # 等待前端启动
    print("   等待前端服务启动...")
    time.sleep(8)
    
    # 检查前端是否启动成功
    import requests
    try:
        response = requests.get("http://localhost:8501/", timeout=10)
        if response.status_code == 200:
            print("✅ 前端服务启动成功")
        else:
            print("❌ 前端服务启动失败")
            return None
    except:
        print("❌ 前端服务连接失败")
        return None
    
    return frontend_process

def main():
    """主启动函数"""
    print("🏥 医疗AI科研系统 - 修复版启动器")
    print("=" * 50)
    
    try:
        # 1. 清理现有进程
        kill_existing_processes()
        
        # 2. 启动后端
        backend_process = start_backend()
        if backend_process is None:
            print("❌ 后端启动失败，退出")
            return
        
        # 3. 启动前端
        frontend_process = start_frontend()
        if frontend_process is None:
            print("❌ 前端启动失败，但后端仍在运行")
            print("   您可以直接访问API: http://127.0.0.1:8000")
            return
        
        # 4. 显示访问信息
        print("\n🎉 系统启动成功！")
        print("=" * 50)
        print("📱 前端界面: http://localhost:8501")
        print("🔌 后端API: http://127.0.0.1:8000")
        print("📚 API文档: http://127.0.0.1:8000/docs")
        print("=" * 50)
        print("按 Ctrl+C 停止服务")
        
        # 5. 等待用户中断
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 正在停止服务...")
            
            # 停止进程
            if backend_process:
                backend_process.terminate()
            if frontend_process:
                frontend_process.terminate()
            
            print("✅ 服务已停止")
    
    except Exception as e:
        print(f"❌ 启动过程中发生错误: {e}")

if __name__ == "__main__":
    main()
