"""
系统配置文件
包含API密钥和其他敏感配置信息
"""

import os
from typing import Optional

class Config:
    """系统配置类"""
    
    # API配置
    DASHSCOPE_API_KEY = "sk-57a7c48444c74ccc8173024d9288e625"
    OPENAI_API_KEY = "your-openai-api-key-here"
    
    # 服务配置
    API_BASE_URL = "http://127.0.0.1:8000"
    MODEL_TRAINING_URL = "http://localhost:7003"  # 本地模拟服务
    # MODEL_TRAINING_URL = "http://47.108.190.171:7003"  # 生产服务器
    
    # 数据库配置
    DATABASE_PATH = "medical_database.db"
    
    # 系统配置
    SYSTEM_NAME = "医疗AI科研系统"
    VERSION = "1.0.0"
    
    @classmethod
    def get_api_key(cls, key_name: str) -> str:
        """获取API密钥，优先从环境变量读取"""
        env_key = f"{key_name.upper()}_API_KEY"
        return os.getenv(env_key, getattr(cls, env_key, ""))
    
    @classmethod
    def set_api_key(cls, key_name: str, value: str) -> None:
        """设置API密钥到环境变量"""
        env_key = f"{key_name.upper()}_API_KEY"
        os.environ[env_key] = value
    
    @classmethod
    def is_api_configured(cls, key_name: str) -> bool:
        """检查API密钥是否已配置"""
        return bool(cls.get_api_key(key_name))
    
    @classmethod
    def get_masked_api_key(cls, key_name: str) -> str:
        """获取掩码后的API密钥用于显示"""
        key = cls.get_api_key(key_name)
        if not key:
            return "未配置"
        if len(key) <= 8:
            return "*" * len(key)
        return key[:4] + "*" * (len(key) - 8) + key[-4:]

# 创建全局配置实例
config = Config()
