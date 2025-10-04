#!/bin/bash

# Vercel快速部署脚本
echo "🚀 开始部署医疗AI科研系统到Vercel..."

# 检查是否安装了Vercel CLI
if ! command -v vercel &> /dev/null; then
    echo "❌ Vercel CLI 未安装，正在安装..."
    npm install -g vercel
fi

# 检查是否已登录
if ! vercel whoami &> /dev/null; then
    echo "🔐 请先登录Vercel..."
    vercel login
fi

# 进入前端目录
cd frontend

# 安装依赖
echo "📦 安装前端依赖..."
npm install

# 构建项目
echo "🔨 构建项目..."
npm run build

# 返回根目录
cd ..

# 部署到Vercel
echo "🚀 部署到Vercel..."
vercel

echo "✅ 部署完成！"
echo ""
echo "📋 下一步操作："
echo "1. 在Vercel Dashboard中配置环境变量："
echo "   - DASHSCOPE_API_KEY: 您的阿里云通义千问API密钥"
echo "   - OPENAI_API_KEY: 您的OpenAI API密钥（可选）"
echo ""
echo "2. 运行生产部署："
echo "   vercel --prod"
echo ""
echo "3. 访问您的应用："
echo "   https://your-project.vercel.app"
