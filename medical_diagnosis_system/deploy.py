#!/usr/bin/env python3
"""
一键部署脚本 - 自动安装依赖、配置环境、启动服务
"""

import subprocess
import sys
import os
import shutil
from pathlib import Path

def print_banner():
    """打印欢迎横幅"""
    print("=" * 70)
    print("🏥 术前病情预测 & 中西医结合诊疗报告生成系统")
    print("   一键部署脚本 v1.0.0")
    print("=" * 70)

def check_python_version():
    """检查Python版本"""
    print("🔍 检查Python版本...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python版本: {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"❌ Python版本过低: {version.major}.{version.minor}.{version.micro}")
        print("   需要Python 3.8或更高版本")
        return False

def install_dependencies():
    """安装依赖包"""
    print("📦 安装依赖包...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ])
        print("✅ 依赖包安装完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 依赖包安装失败: {e}")
        return False

def setup_environment():
    """设置环境配置"""
    print("⚙️  设置环境配置...")
    
    # 检查是否存在.env文件
    env_file = Path(".env")
    if not env_file.exists():
        # 复制示例文件
        if Path("env_example.txt").exists():
            shutil.copy("env_example.txt", ".env")
            print("✅ 已创建.env配置文件")
        else:
            print("⚠️  未找到env_example.txt文件")
    else:
        print("✅ .env配置文件已存在")
    
    # 检查API Key配置
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "your_openai_api_key_here":
        print("⚠️  请在.env文件中配置OPENAI_API_KEY")
        print("   编辑.env文件，将your_openai_api_key_here替换为您的API Key")
        return False
    else:
        print("✅ OpenAI API Key已配置")
        return True

def create_directories():
    """创建必要的目录"""
    print("📁 创建必要目录...")
    directories = ["reports", "logs"]
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"   ✅ {directory}/ 目录已创建")

def run_tests():
    """运行系统测试"""
    print("🧪 运行系统测试...")
    try:
        result = subprocess.run([
            sys.executable, "test_system.py"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ 系统测试通过")
            return True
        else:
            print("❌ 系统测试失败")
            print("错误输出:", result.stderr)
            return False
    except Exception as e:
        print(f"❌ 测试运行失败: {e}")
        return False

def start_services():
    """启动服务"""
    print("🚀 启动服务...")
    try:
        # 启动后端服务
        backend_process = subprocess.Popen([
            sys.executable, "main.py"
        ], cwd=Path(__file__).parent)
        
        # 等待后端启动
        import time
        time.sleep(3)
        
        # 启动前端服务
        frontend_process = subprocess.Popen([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.port", "8501",
            "--server.address", "localhost"
        ], cwd=Path(__file__).parent)
        
        print("✅ 服务启动成功")
        print("\n📋 访问地址:")
        print("   前端界面: http://localhost:8501")
        print("   后端API: http://127.0.0.1:8000")
        print("   API文档: http://127.0.0.1:8000/docs")
        
        print("\n💡 使用提示:")
        print("   1. 在浏览器中打开前端界面")
        print("   2. 开始使用系统生成诊疗报告")
        print("   3. 按Ctrl+C停止服务")
        
        # 保持程序运行
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n👋 正在停止服务...")
            backend_process.terminate()
            frontend_process.terminate()
            print("✅ 服务已停止")
        
        return True
    except Exception as e:
        print(f"❌ 服务启动失败: {e}")
        return False

def main():
    """主函数"""
    print_banner()
    
    # 检查Python版本
    if not check_python_version():
        sys.exit(1)
    
    # 安装依赖
    if not install_dependencies():
        sys.exit(1)
    
    # 设置环境
    if not setup_environment():
        print("\n⚠️  请先配置OpenAI API Key，然后重新运行部署脚本")
        sys.exit(1)
    
    # 创建目录
    create_directories()
    
    # 运行测试
    if not run_tests():
        print("\n⚠️  系统测试失败，但可以继续启动服务")
        response = input("是否继续启动服务？(y/N): ")
        if response.lower() != 'y':
            sys.exit(1)
    
    # 启动服务
    start_services()

if __name__ == "__main__":
    main()
