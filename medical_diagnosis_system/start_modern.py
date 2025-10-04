#!/usr/bin/env python3
"""
现代化医疗AI科研系统启动脚本
基于medical-diagnostic-system设计风格
"""

import subprocess
import sys
import os
import time
import signal
import psutil
from pathlib import Path

def kill_existing_processes():
    """终止现有进程"""
    print("🔄 检查并终止现有进程...")
    
    # 终止端口8000和8501的进程
    for port in [8000, 8501]:
        try:
            for proc in psutil.process_iter(['pid', 'name', 'connections']):
                try:
                    for conn in proc.info['connections'] or []:
                        if conn.laddr.port == port:
                            print(f"   终止进程 {proc.info['pid']} (端口 {port})")
                            proc.terminate()
                            proc.wait(timeout=5)
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass
        except Exception as e:
            print(f"   警告: 无法检查端口 {port}: {e}")

def start_backend():
    """启动后端API服务"""
    print("🚀 启动后端API服务...")
    
    # 设置环境变量
    env = os.environ.copy()
    env['DASHSCOPE_API_KEY'] = "sk-57a7c48444c74ccc8173024d9288e625"
    
    # 启动后端
    backend_cmd = [
        sys.executable, "-c",
        """
import uvicorn
from main import app
print('🏥 医疗AI科研系统后端启动中...')
uvicorn.run(app, host='0.0.0.0', port=8000, log_level='info')
"""
    ]
    
    try:
        backend_process = subprocess.Popen(
            backend_cmd,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # 等待后端启动
        time.sleep(3)
        
        # 检查后端是否启动成功
        try:
            import requests
            response = requests.get("http://127.0.0.1:8000/", timeout=5)
            if response.status_code == 200:
                print("✅ 后端API服务启动成功")
                return backend_process
            else:
                print("❌ 后端API服务启动失败")
                return None
        except Exception as e:
            print(f"❌ 后端API服务检查失败: {e}")
            return None
            
    except Exception as e:
        print(f"❌ 启动后端服务失败: {e}")
        return None

def start_frontend():
    """启动前端Streamlit服务"""
    print("🎨 启动现代化前端服务...")
    
    # 设置环境变量
    env = os.environ.copy()
    env['STREAMLIT_BROWSER_GATHER_USAGE_STATS'] = 'false'
    
    # 启动前端
    frontend_cmd = [
        sys.executable, "-m", "streamlit", "run", "app_modern.py",
        "--server.port", "8501",
        "--server.headless", "true",
        "--browser.gatherUsageStats", "false",
        "--server.enableCORS", "false",
        "--server.enableXsrfProtection", "false"
    ]
    
    try:
        frontend_process = subprocess.Popen(
            frontend_cmd,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # 等待前端启动
        time.sleep(5)
        
        # 检查前端是否启动成功
        try:
            import requests
            response = requests.get("http://localhost:8501/", timeout=10)
            if response.status_code == 200:
                print("✅ 现代化前端服务启动成功")
                return frontend_process
            else:
                print("❌ 现代化前端服务启动失败")
                return None
        except Exception as e:
            print(f"❌ 现代化前端服务检查失败: {e}")
            return None
            
    except Exception as e:
        print(f"❌ 启动现代化前端服务失败: {e}")
        return None

def main():
    """主启动函数"""
    print("🏥 医疗AI科研系统 - 现代化版本启动")
    print("=" * 50)
    
    # 切换到项目目录
    project_dir = Path(__file__).parent
    os.chdir(project_dir)
    print(f"📁 工作目录: {project_dir}")
    
    # 终止现有进程
    kill_existing_processes()
    time.sleep(2)
    
    # 启动后端
    backend_process = start_backend()
    if not backend_process:
        print("❌ 后端启动失败，退出")
        return
    
    # 启动前端
    frontend_process = start_frontend()
    if not frontend_process:
        print("❌ 前端启动失败，终止后端")
        backend_process.terminate()
        return
    
    print("\n🎉 系统启动成功！")
    print("=" * 50)
    print("📍 后端API服务: http://127.0.0.1:8000")
    print("📍 现代化前端: http://localhost:8501")
    print("📚 API文档: http://127.0.0.1:8000/docs")
    print("\n💡 功能特色:")
    print("   ✨ 现代化UI设计 - 基于medical-diagnostic-system")
    print("   🎨 深色/浅色主题切换")
    print("   📱 响应式布局设计")
    print("   🔬 完整科研分析功能")
    print("   🤖 AI智能对话助手")
    print("   📊 数据可视化分析")
    print("\n按 Ctrl+C 停止服务")
    
    try:
        # 保持进程运行
        while True:
            time.sleep(1)
            
            # 检查进程状态
            if backend_process.poll() is not None:
                print("❌ 后端服务意外停止")
                break
            if frontend_process.poll() is not None:
                print("❌ 前端服务意外停止")
                break
                
    except KeyboardInterrupt:
        print("\n🛑 正在停止服务...")
        
        # 终止进程
        if backend_process:
            backend_process.terminate()
        if frontend_process:
            frontend_process.terminate()
        
        # 等待进程结束
        time.sleep(2)
        
        # 强制终止
        if backend_process and backend_process.poll() is None:
            backend_process.kill()
        if frontend_process and frontend_process.poll() is None:
            frontend_process.kill()
        
        print("✅ 服务已停止")

if __name__ == "__main__":
    main()
