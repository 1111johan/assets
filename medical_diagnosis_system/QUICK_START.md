# 🚀 快速开始指南

## 一分钟快速启动

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 配置API Key
编辑 `.env` 文件，设置您的 OpenAI API Key：
```
OPENAI_API_KEY=your_actual_api_key_here
```

### 3. 一键启动
```bash
python start.py
```

### 4. 访问系统
- 前端界面：http://localhost:8501
- 后端API：http://127.0.0.1:8000
- API文档：http://127.0.0.1:8000/docs

## 🎯 核心功能演示

### 生成诊疗报告
1. 打开前端界面
2. 填写病人信息（姓名、年龄、症状等）
3. 输入检查结果（血检、影像等）
4. 点击"生成诊疗报告"
5. 查看AI生成的中西医结合报告
6. 下载PDF格式报告

### 查看历史记录
1. 在"查看历史记录"页面
2. 浏览所有病人信息
3. 点击查看详细报告
4. 生成和下载PDF报告

## 📋 系统特点

✅ **中西医结合**：融合现代医学和中医理论  
✅ **AI驱动**：基于GPT-4的智能诊断  
✅ **专业报告**：结构化的诊疗报告格式  
✅ **多格式输出**：支持文本和PDF格式  
✅ **历史管理**：完整的病人记录管理  
✅ **用户友好**：直观的Web界面  

## 🔧 故障排除

### 常见问题

**Q: 报告生成失败？**  
A: 检查OpenAI API Key是否正确配置，确保有足够额度

**Q: 无法访问界面？**  
A: 确保服务正在运行，检查端口是否被占用

**Q: PDF生成失败？**  
A: 确保ReportLab库已正确安装

### 测试系统
```bash
python test_system.py
```

### 查看日志
```bash
python main.py  # 后端日志
streamlit run app.py  # 前端日志
```

## 📚 更多资源

- [完整文档](README.md)
- [项目结构](PROJECT_STRUCTURE.md)
- [API示例](example_usage.py)
- [部署指南](deploy.py)

---

**开始使用您的AI医疗辅助系统吧！** 🏥✨
