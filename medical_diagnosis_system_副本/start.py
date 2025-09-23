#!/usr/bin/env python3
"""
启动脚本 - 同时启动后端和前端服务
"""

import subprocess
import sys
import time
import os
from pathlib import Path

def check_dependencies():
    """检查依赖是否安装"""
    try:
        import fastapi
        import streamlit
        import openai
        import reportlab
        print("✅ 所有依赖已安装")
        return True
    except ImportError as e:
        print(f"❌ 缺少依赖: {e}")
        print("请运行: pip install -r requirements.txt")
        return False

def check_api_key():
    """检查 OpenAI API Key"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "your_openai_api_key_here":
        print("⚠️  未设置 OpenAI API Key")
        print("请在系统设置中配置 API Key 或设置环境变量")
        return False
    print("✅ OpenAI API Key 已配置")
    return True

def start_backend():
    """启动后端服务"""
    print("🚀 启动后端服务...")
    try:
        subprocess.Popen([
            sys.executable, "main.py"
        ], cwd=Path(__file__).parent)
        print("✅ 后端服务已启动 (http://127.0.0.1:8000)")
        return True
    except Exception as e:
        print(f"❌ 后端启动失败: {e}")
        return False

def start_frontend():
    """启动前端服务"""
    print("🚀 启动前端服务...")
    try:
        subprocess.Popen([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.port", "8501",
            "--server.address", "localhost"
        ], cwd=Path(__file__).parent)
        print("✅ 前端服务已启动 (http://localhost:8501)")
        return True
    except Exception as e:
        print(f"❌ 前端启动失败: {e}")
        return False

def main():
    """主函数"""
    print("🏥 术前病情预测 & 中西医结合诊疗报告生成系统")
    print("=" * 60)
    
    # 检查依赖
    if not check_dependencies():
        sys.exit(1)
    
    # 检查 API Key
    check_api_key()
    
    # 启动服务
    print("\n📡 正在启动服务...")
    
    backend_success = start_backend()
    time.sleep(2)  # 等待后端启动
    
    frontend_success = start_frontend()
    
    if backend_success and frontend_success:
        print("\n🎉 系统启动成功！")
        print("\n📋 访问地址:")
        print("   前端界面: http://localhost:8501")
        print("   后端 API: http://127.0.0.1:8000")
        print("   API 文档: http://127.0.0.1:8000/docs")
        print("\n💡 使用提示:")
        print("   1. 在浏览器中打开前端界面")
        print("   2. 在系统设置中配置 OpenAI API Key")
        print("   3. 开始使用系统生成诊疗报告")
        print("\n⚠️  按 Ctrl+C 停止服务")
        
        try:
            # 保持程序运行
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n👋 服务已停止")
    else:
        print("\n❌ 服务启动失败")
        sys.exit(1)

if __name__ == "__main__":
    main()
