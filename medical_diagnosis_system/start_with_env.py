#!/usr/bin/env python3
"""
带环境变量加载的启动脚本
自动加载 .env 文件并启动系统
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def load_env_file():
    """加载环境变量文件"""
    env_file = Path(".env")
    template_file = Path("env_template.txt")
    
    # 如果 .env 文件不存在，从模板创建
    if not env_file.exists():
        if template_file.exists():
            print("📝 创建环境配置文件...")
            with open(template_file, 'r', encoding='utf-8') as f:
                content = f.read()
            with open(env_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ 已创建 {env_file}")
        else:
            print("⚠️ 未找到环境配置文件模板")
            return False
    
    # 加载环境变量
    with open(env_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '=' in line:
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip()
                
                # 移除引号
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]
                elif value.startswith("'") and value.endswith("'"):
                    value = value[1:-1]
                
                os.environ[key] = value
    
    return True

def start_services():
    """启动所有服务"""
    print("🚀 启动医疗AI科研系统...")
    print("=" * 50)
    
    # 加载环境变量
    if not load_env_file():
        print("❌ 环境变量加载失败")
        return False
    
    # 获取配置
    api_port = os.getenv("API_PORT", "8000")
    frontend_port = os.getenv("FRONTEND_PORT", "8501")
    model_port = os.getenv("MODEL_TRAINING_PORT", "7003")
    
    print(f"📋 配置信息:")
    print(f"  后端API端口: {api_port}")
    print(f"  前端端口: {frontend_port}")
    print(f"  模型训练端口: {model_port}")
    print()
    
    try:
        # 启动模型训练服务
        print("🤖 启动模型训练服务...")
        model_process = subprocess.Popen([
            sys.executable, "mock_model_training.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(3)
        
        # 启动后端API服务
        print("🔧 启动后端API服务...")
        api_process = subprocess.Popen([
            sys.executable, "main.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(5)
        
        # 启动前端服务
        print("🌐 启动前端服务...")
        frontend_process = subprocess.Popen([
            sys.executable, "-m", "streamlit", "run", "app_simple.py",
            "--server.port", frontend_port,
            "--server.headless", "true",
            "--browser.gatherUsageStats", "false"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        print("✅ 所有服务已启动!")
        print(f"🌐 前端地址: http://localhost:{frontend_port}")
        print(f"🔧 后端API: http://localhost:{api_port}")
        print(f"🤖 模型训练: http://localhost:{model_port}")
        print()
        print("按 Ctrl+C 停止所有服务")
        
        # 等待用户中断
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 正在停止服务...")
            
            # 停止所有进程
            for process in [frontend_process, api_process, model_process]:
                if process.poll() is None:
                    process.terminate()
                    process.wait()
            
            print("✅ 所有服务已停止")
            
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        return False
    
    return True

if __name__ == "__main__":
    start_services()
