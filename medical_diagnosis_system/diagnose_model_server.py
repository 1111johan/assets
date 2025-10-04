#!/usr/bin/env python3
"""
模型训练服务器诊断工具
用于检查外部模型训练服务器的连接状态
"""

import socket
import requests
import time
from datetime import datetime

# 服务器配置
SERVER_HOST = "47.108.190.171"
TEST_PORTS = [7003, 8080, 8000, 3000, 5000, 80, 443, 9000, 9999]

def check_port(host, port, timeout=3):
    """检查端口是否开放"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            return result == 0
    except Exception as e:
        print(f"   ❌ 端口 {port} 检查失败: {e}")
        return False

def check_http_service(host, port, timeout=5):
    """检查HTTP服务是否响应"""
    try:
        url = f"http://{host}:{port}/"
        response = requests.get(url, timeout=timeout)
        return {
            "success": True,
            "status_code": response.status_code,
            "content_type": response.headers.get('content-type', 'unknown'),
            "content_length": len(response.content)
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def main():
    print("🔍 模型训练服务器诊断工具")
    print("=" * 50)
    print(f"目标服务器: {SERVER_HOST}")
    print(f"检查时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 1. 检查网络连通性
    print("1️⃣ 检查网络连通性...")
    try:
        import subprocess
        result = subprocess.run(['ping', '-c', '3', SERVER_HOST], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"   ✅ 服务器 {SERVER_HOST} 网络可达")
        else:
            print(f"   ❌ 服务器 {SERVER_HOST} 网络不可达")
            return
    except Exception as e:
        print(f"   ⚠️  无法检查网络连通性: {e}")
    
    print()
    
    # 2. 检查端口开放状态
    print("2️⃣ 检查端口开放状态...")
    open_ports = []
    for port in TEST_PORTS:
        print(f"   检查端口 {port}...", end=" ")
        if check_port(SERVER_HOST, port):
            print("✅ 开放")
            open_ports.append(port)
        else:
            print("❌ 关闭")
    
    print()
    
    # 3. 检查HTTP服务
    if open_ports:
        print("3️⃣ 检查HTTP服务响应...")
        for port in open_ports:
            print(f"   检查 http://{SERVER_HOST}:{port}/ ...")
            result = check_http_service(SERVER_HOST, port)
            if result["success"]:
                print(f"      ✅ HTTP服务正常")
                print(f"         状态码: {result['status_code']}")
                print(f"         内容类型: {result['content_type']}")
                print(f"         内容长度: {result['content_length']} bytes")
            else:
                print(f"      ❌ HTTP服务异常: {result['error']}")
    else:
        print("3️⃣ 跳过HTTP服务检查（没有开放的端口）")
    
    print()
    
    # 4. 总结和建议
    print("4️⃣ 诊断总结")
    print("-" * 30)
    if open_ports:
        print(f"✅ 发现 {len(open_ports)} 个开放端口: {open_ports}")
        print("建议:")
        print("   1. 检查这些端口上运行的服务")
        print("   2. 确认哪个是模型训练服务")
        print("   3. 更新配置中的端口号")
    else:
        print("❌ 没有发现任何开放的端口")
        print("可能的原因:")
        print("   1. 模型训练服务未启动")
        print("   2. 防火墙阻止了外部连接")
        print("   3. 服务只监听本地地址(127.0.0.1)")
        print("   4. 服务运行在不同的端口上")
        print()
        print("建议:")
        print("   1. 登录服务器检查服务状态")
        print("   2. 检查防火墙配置")
        print("   3. 确认服务监听地址和端口")
        print("   4. 查看服务日志")

if __name__ == "__main__":
    main()
