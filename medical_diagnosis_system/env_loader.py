"""
环境变量加载器
用于加载和管理环境变量配置
"""

import os
from pathlib import Path
from typing import Optional, Any

class EnvLoader:
    """环境变量加载器类"""
    
    def __init__(self, env_file: str = ".env"):
        """
        初始化环境变量加载器
        
        Args:
            env_file: 环境变量文件路径，默认为 .env
        """
        self.env_file = env_file
        self.load_env_file()
    
    def load_env_file(self):
        """加载环境变量文件"""
        env_path = Path(self.env_file)
        
        if env_path.exists():
            with open(env_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    # 跳过空行和注释行
                    if not line or line.startswith('#'):
                        continue
                    
                    # 解析键值对
                    if '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip()
                        
                        # 移除引号
                        if value.startswith('"') and value.endswith('"'):
                            value = value[1:-1]
                        elif value.startswith("'") and value.endswith("'"):
                            value = value[1:-1]
                        
                        # 设置环境变量
                        os.environ[key] = value
        else:
            print(f"⚠️ 环境文件 {self.env_file} 不存在，使用默认配置")
    
    def get(self, key: str, default: Any = None) -> str:
        """
        获取环境变量值
        
        Args:
            key: 环境变量名
            default: 默认值
            
        Returns:
            环境变量值或默认值
        """
        return os.getenv(key, default)
    
    def get_bool(self, key: str, default: bool = False) -> bool:
        """
        获取布尔类型环境变量
        
        Args:
            key: 环境变量名
            default: 默认值
            
        Returns:
            布尔值
        """
        value = self.get(key, str(default)).lower()
        return value in ('true', '1', 'yes', 'on')
    
    def get_int(self, key: str, default: int = 0) -> int:
        """
        获取整数类型环境变量
        
        Args:
            key: 环境变量名
            default: 默认值
            
        Returns:
            整数值
        """
        try:
            return int(self.get(key, str(default)))
        except ValueError:
            return default
    
    def get_list(self, key: str, separator: str = ',', default: list = None) -> list:
        """
        获取列表类型环境变量
        
        Args:
            key: 环境变量名
            separator: 分隔符
            default: 默认值
            
        Returns:
            列表
        """
        if default is None:
            default = []
        
        value = self.get(key, '')
        if not value:
            return default
        
        return [item.strip() for item in value.split(separator) if item.strip()]

# 创建全局环境变量加载器实例
env = EnvLoader()

# 常用配置的便捷访问方法
def get_api_key(service: str) -> str:
    """获取API密钥"""
    return env.get(f"{service.upper()}_API_KEY", "")

def get_service_url(service: str) -> str:
    """获取服务URL"""
    return env.get(f"{service.upper()}_URL", "")

def is_debug() -> bool:
    """是否调试模式"""
    return env.get_bool("DEBUG", False)

def get_log_level() -> str:
    """获取日志级别"""
    return env.get("LOG_LEVEL", "INFO")

# 示例用法
if __name__ == "__main__":
    print("🔧 环境配置加载器测试")
    print("=" * 40)
    
    # 测试基本功能
    print(f"DASHSCOPE_API_KEY: {get_api_key('dashscope')[:10]}...")
    print(f"API_BASE_URL: {env.get('API_BASE_URL', 'http://127.0.0.1:8000')}")
    print(f"DEBUG模式: {is_debug()}")
    print(f"日志级别: {get_log_level()}")
    
    # 显示所有环境变量
    print("\n📋 所有相关环境变量:")
    for key, value in os.environ.items():
        if any(prefix in key.upper() for prefix in ['API', 'URL', 'DEBUG', 'LOG']):
            # 隐藏敏感信息
            if 'KEY' in key.upper():
                display_value = value[:10] + "..." if len(value) > 10 else value
            else:
                display_value = value
            print(f"  {key}: {display_value}")
