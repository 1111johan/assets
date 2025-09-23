#!/usr/bin/env python3
"""
清洁启动脚本 - 解决前端JavaScript错误和兼容性问题
"""

import subprocess
import sys
import time
import os
from pathlib import Path

def start_backend():
    """启动后端服务"""
    print("🚀 启动后端服务...")
    try:
        # 设置环境变量
        env = os.environ.copy()
        env["DASHSCOPE_API_KEY"] = "sk-57a7c48444c74ccc8173024d9288e625"
        
        subprocess.Popen([
            sys.executable, "-c", """
import uvicorn
from main import app
print('正在启动服务器...')
uvicorn.run(app, host='0.0.0.0', port=8000)
"""
        ], cwd=Path(__file__).parent, env=env)
        
        print("✅ 后端服务已启动 (http://127.0.0.1:8000)")
        return True
    except Exception as e:
        print(f"❌ 后端启动失败: {e}")
        return False

def start_frontend():
    """启动前端服务"""
    print("🚀 启动前端服务...")
    try:
        # 设置环境变量禁用统计收集
        env = os.environ.copy()
        env["STREAMLIT_BROWSER_GATHER_USAGE_STATS"] = "false"
        
        subprocess.Popen([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.port", "8501",
            "--server.headless", "true",
            "--browser.gatherUsageStats", "false",
            "--global.developmentMode", "false"
        ], cwd=Path(__file__).parent, env=env)
        
        print("✅ 前端服务已启动 (http://localhost:8501)")
        return True
    except Exception as e:
        print(f"❌ 前端启动失败: {e}")
        return False

def main():
    """主函数"""
    print("🏥 术前病情预测 & 中西医结合诊疗报告生成系统")
    print("   清洁启动模式 - 解决前端兼容性问题")
    print("=" * 60)
    
    # 清理旧进程
    print("🧹 清理旧进程...")
    try:
        subprocess.run(["pkill", "-f", "streamlit"], check=False)
        subprocess.run(["pkill", "-f", "uvicorn"], check=False)
        time.sleep(2)
        print("✅ 进程清理完成")
    except:
        pass
    
    # 启动服务
    print("\n📡 正在启动服务...")
    
    backend_success = start_backend()
    time.sleep(3)  # 等待后端启动
    
    frontend_success = start_frontend()
    time.sleep(3)  # 等待前端启动
    
    if backend_success and frontend_success:
        print("\n🎉 系统启动成功！")
        print("\n📋 访问地址:")
        print("   前端界面: http://localhost:8501")
        print("   后端 API: http://127.0.0.1:8000")
        print("   API 文档: http://127.0.0.1:8000/docs")
        
        print("\n💡 功能说明:")
        print("   1. 新增病人报告 - 生成中西医结合诊疗报告")
        print("   2. AI对话助手 - 实时医疗咨询")
        print("   3. 报告整理优化 - AI优化现有报告")
        print("   4. 症状分析 - 输入症状获取分析")
        print("   5. 历史记录管理 - 查看所有病人数据")
        
        print("\n🔧 故障排除:")
        print("   - 如遇到JavaScript错误，请刷新浏览器")
        print("   - 建议使用Chrome或Firefox浏览器")
        print("   - 如有问题，可查看终端日志")
        
        print("\n⚠️  按 Ctrl+C 停止服务")
        
        try:
            # 保持程序运行
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n👋 正在停止服务...")
            subprocess.run(["pkill", "-f", "streamlit"], check=False)
            subprocess.run(["pkill", "-f", "uvicorn"], check=False)
            print("✅ 服务已停止")
    else:
        print("\n❌ 服务启动失败")
        sys.exit(1)

if __name__ == "__main__":
    main()
