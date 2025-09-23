#!/usr/bin/env python3
"""
系统运行脚本 - 一键启动完整的医疗诊疗系统
"""

import subprocess
import sys
import time
import os
import signal
from pathlib import Path

class SystemManager:
    def __init__(self):
        self.backend_process = None
        self.frontend_process = None
        
    def cleanup(self):
        """清理进程"""
        print("🧹 清理旧进程...")
        try:
            subprocess.run(["pkill", "-f", "streamlit"], check=False)
            subprocess.run(["pkill", "-f", "uvicorn"], check=False)
            subprocess.run(["pkill", "-f", "python.*main"], check=False)
            time.sleep(2)
            print("✅ 进程清理完成")
        except:
            pass
    
    def start_backend(self):
        """启动后端服务"""
        print("🚀 启动后端服务...")
        try:
            env = os.environ.copy()
            env["DASHSCOPE_API_KEY"] = "sk-57a7c48444c74ccc8173024d9288e625"
            
            self.backend_process = subprocess.Popen([
                sys.executable, "main.py"
            ], cwd=Path(__file__).parent, env=env)
            
            # 等待后端启动
            time.sleep(3)
            
            # 检查后端是否启动成功
            import requests
            try:
                response = requests.get("http://127.0.0.1:8000/", timeout=5)
                if response.status_code == 200:
                    print("✅ 后端服务启动成功 (http://127.0.0.1:8000)")
                    return True
                else:
                    print("❌ 后端服务启动失败")
                    return False
            except:
                print("❌ 后端服务连接失败")
                return False
                
        except Exception as e:
            print(f"❌ 后端启动异常: {e}")
            return False
    
    def start_frontend(self):
        """启动前端服务"""
        print("🚀 启动前端服务...")
        try:
            env = os.environ.copy()
            env["STREAMLIT_BROWSER_GATHER_USAGE_STATS"] = "false"
            
            self.frontend_process = subprocess.Popen([
                sys.executable, "-m", "streamlit", "run", "app.py",
                "--server.port", "8501",
                "--server.headless", "true",
                "--browser.gatherUsageStats", "false"
            ], cwd=Path(__file__).parent, env=env)
            
            # 等待前端启动
            time.sleep(5)
            
            # 检查前端是否启动成功
            import requests
            try:
                response = requests.get("http://localhost:8501/", timeout=5)
                if response.status_code == 200:
                    print("✅ 前端服务启动成功 (http://localhost:8501)")
                    return True
                else:
                    print("❌ 前端服务启动失败")
                    return False
            except:
                print("❌ 前端服务连接失败")
                return False
                
        except Exception as e:
            print(f"❌ 前端启动异常: {e}")
            return False
    
    def stop_services(self):
        """停止所有服务"""
        print("\n👋 正在停止服务...")
        if self.backend_process:
            self.backend_process.terminate()
        if self.frontend_process:
            self.frontend_process.terminate()
        
        # 强制清理
        self.cleanup()
        print("✅ 所有服务已停止")
    
    def run(self):
        """运行系统"""
        print("🏥 术前病情预测 & 中西医结合诊疗报告生成系统")
        print("=" * 60)
        
        # 设置信号处理
        def signal_handler(sig, frame):
            self.stop_services()
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        
        # 清理旧进程
        self.cleanup()
        
        # 启动后端
        if not self.start_backend():
            print("❌ 后端启动失败，退出")
            sys.exit(1)
        
        # 启动前端
        if not self.start_frontend():
            print("❌ 前端启动失败，但后端正常")
            print("💡 您可以直接访问API: http://127.0.0.1:8000/docs")
        
        print("\n🎉 系统启动完成！")
        print("\n📋 访问地址:")
        print("   🌐 前端界面: http://localhost:8501")
        print("   🔧 后端API: http://127.0.0.1:8000")
        print("   📚 API文档: http://127.0.0.1:8000/docs")
        
        print("\n🌟 主要功能:")
        print("   📝 新增病人报告 - 生成中西医结合诊疗报告")
        print("   🤖 AI对话助手 - 实时医疗咨询")
        print("   📊 报告整理优化 - AI优化现有报告")
        print("   🔍 症状分析 - 症状输入和专业分析")
        print("   📚 历史记录管理 - 查看所有数据")
        
        print("\n⚠️  按 Ctrl+C 停止服务")
        
        try:
            # 保持程序运行
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop_services()

if __name__ == "__main__":
    manager = SystemManager()
    manager.run()
