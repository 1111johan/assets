# 🚀 Vercel部署指南 - 医疗AI科研系统

## 📋 部署概述

本指南将帮助您将医疗AI科研系统部署到Vercel平台。系统采用以下架构：

- **前端**: Next.js 14 + TypeScript + Tailwind CSS
- **后端**: Vercel Serverless Functions (Python)
- **AI服务**: 阿里云通义千问 + OpenAI GPT
- **数据库**: Vercel Postgres (推荐) 或外部数据库

## 🛠️ 部署前准备

### 1. 系统要求
- Node.js 18+ 
- Python 3.8+
- Vercel账户
- 阿里云通义千问API密钥
- (可选) OpenAI API密钥

### 2. 获取API密钥

#### 阿里云通义千问
1. 访问 [阿里云通义千问控制台](https://dashscope.console.aliyun.com/)
2. 创建API密钥
3. 记录API密钥备用

#### OpenAI (可选)
1. 访问 [OpenAI平台](https://platform.openai.com/)
2. 创建API密钥
3. 记录API密钥备用

## 🚀 部署步骤

### 步骤1: 准备项目文件

确保您的项目包含以下文件结构：

```
medical_diagnosis_system/
├── vercel.json                 # Vercel配置
├── api/                       # Serverless Functions
│   ├── __init__.py
│   ├── generate_report.py
│   └── chat.py
├── frontend/                  # Next.js前端
│   ├── package.json
│   ├── next.config.js
│   ├── tailwind.config.js
│   ├── tsconfig.json
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   └── globals.css
│   └── components/
│       ├── Header.tsx
│       ├── Sidebar.tsx
│       ├── NewPatientForm.tsx
│       └── ...
└── requirements.txt           # Python依赖
```

### 步骤2: 安装Vercel CLI

```bash
npm install -g vercel
```

### 步骤3: 登录Vercel

```bash
vercel login
```

### 步骤4: 初始化项目

在项目根目录运行：

```bash
vercel
```

按照提示完成配置：
- 选择项目名称
- 选择框架：Other
- 选择根目录：`./frontend`

### 步骤5: 配置环境变量

在Vercel Dashboard中配置环境变量：

1. 进入项目设置
2. 选择 "Environment Variables"
3. 添加以下变量：

```
DASHSCOPE_API_KEY=your_dashscope_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
API_BASE_URL=https://your-project.vercel.app/api
NODE_ENV=production
```

### 步骤6: 部署

```bash
vercel --prod
```

## 🔧 配置说明

### Vercel配置文件 (vercel.json)

```json
{
  "version": 2,
  "builds": [
    {
      "src": "api/**/*.py",
      "use": "@vercel/python"
    },
    {
      "src": "frontend/package.json",
      "use": "@vercel/next"
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "/api/$1"
    },
    {
      "src": "/(.*)",
      "dest": "/frontend/$1"
    }
  ],
  "functions": {
    "api/**/*.py": {
      "maxDuration": 30
    }
  }
}
```

### 前端配置 (frontend/next.config.js)

```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  env: {
    API_BASE_URL: process.env.API_BASE_URL || 'http://localhost:3000/api',
  },
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: '/api/:path*',
      },
    ]
  },
}

module.exports = nextConfig
```

## 📊 功能特性

### 已实现功能
- ✅ 病人信息录入
- ✅ AI诊疗报告生成
- ✅ AI对话助手
- ✅ 症状分析
- ✅ 报告优化整理
- ✅ 科研数据分析
- ✅ 模型训练界面
- ✅ 证据包生成
- ✅ 系统设置

### 技术特点
- 🚀 **无服务器架构**: 基于Vercel Serverless Functions
- ⚡ **高性能**: Next.js 14 + React 18
- 🎨 **现代UI**: Tailwind CSS + 响应式设计
- 🔒 **安全**: 环境变量管理 + API密钥保护
- 📱 **移动友好**: 完全响应式设计

## 🔍 故障排除

### 常见问题

#### 1. API调用失败
**问题**: 前端无法调用后端API
**解决方案**:
- 检查环境变量配置
- 确认API密钥有效性
- 查看Vercel函数日志

#### 2. 构建失败
**问题**: 部署时构建失败
**解决方案**:
- 检查Python依赖版本
- 确认所有文件路径正确
- 查看构建日志

#### 3. 环境变量未生效
**问题**: 环境变量在运行时未生效
**解决方案**:
- 重新部署项目
- 检查变量名称拼写
- 确认变量作用域设置

### 调试命令

```bash
# 查看部署日志
vercel logs

# 本地开发
vercel dev

# 检查项目状态
vercel ls
```

## 📈 性能优化

### 1. 前端优化
- 使用Next.js Image组件优化图片
- 启用代码分割和懒加载
- 配置CDN缓存策略

### 2. 后端优化
- 优化Python函数冷启动时间
- 使用连接池管理数据库连接
- 实现请求缓存机制

### 3. 数据库优化
- 使用Vercel Postgres
- 配置适当的索引
- 实现查询优化

## 🔐 安全建议

### 1. API密钥管理
- 使用环境变量存储敏感信息
- 定期轮换API密钥
- 限制API访问权限

### 2. 数据安全
- 实现数据加密
- 配置HTTPS
- 设置访问控制

### 3. 监控告警
- 配置错误监控
- 设置性能告警
- 实现日志分析

## 📚 扩展功能

### 1. 数据库集成
```python
# 使用Vercel Postgres
import os
import psycopg2

def get_db_connection():
    return psycopg2.connect(os.getenv('DATABASE_URL'))
```

### 2. 文件存储
```python
# 使用Vercel Blob存储
from vercel_storage import blob

def upload_file(file_data):
    return blob.put(file_data)
```

### 3. 监控集成
```javascript
// 使用Vercel Analytics
import { Analytics } from '@vercel/analytics/react'

export default function App() {
  return (
    <>
      <YourApp />
      <Analytics />
    </>
  )
}
```

## 🎯 部署检查清单

- [ ] 项目文件结构完整
- [ ] 环境变量配置正确
- [ ] API密钥有效
- [ ] 本地测试通过
- [ ] Vercel CLI已安装
- [ ] 项目已初始化
- [ ] 环境变量已设置
- [ ] 部署成功
- [ ] 功能测试通过
- [ ] 性能监控配置

## 📞 技术支持

如果在部署过程中遇到问题，请：

1. 查看Vercel官方文档
2. 检查项目日志
3. 参考故障排除部分
4. 联系技术支持

## 🎉 部署完成

恭喜！您的医疗AI科研系统已成功部署到Vercel。

**访问地址**: `https://your-project.vercel.app`

**功能测试**:
1. 打开系统首页
2. 测试病人信息录入
3. 生成AI诊疗报告
4. 使用AI对话功能
5. 检查所有功能模块

---

**重要提醒**: 
- 本系统仅供医疗参考，不能替代专业医生诊断
- 请妥善保管API密钥和敏感信息
- 定期备份重要数据
- 遵守相关法律法规和医疗伦理

祝您使用愉快！🏥✨
