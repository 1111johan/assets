# 项目结构说明

```
medical_diagnosis_system/
├── main.py                 # FastAPI 后端主程序
├── app.py                  # Streamlit 前端界面
├── pdf_generator.py        # PDF 报告生成模块
├── test_system.py          # 系统功能测试脚本
├── start.py                # 一键启动脚本
├── requirements.txt        # Python 依赖包
├── README.md              # 项目说明文档
├── env_example.txt        # 环境变量配置示例
├── PROJECT_STRUCTURE.md   # 项目结构说明（本文件）
├── medical_reports.db     # SQLite 数据库文件（运行时生成）
└── reports/               # PDF 报告存储目录（运行时生成）
    └── *.pdf             # 生成的 PDF 报告文件
```

## 核心模块说明

### 1. 后端服务 (main.py)
- **FastAPI 应用**：提供 RESTful API 接口
- **数据模型**：定义病人信息和报告请求的数据结构
- **数据库操作**：SQLite 数据库的增删改查
- **AI 集成**：调用 OpenAI GPT-4 生成诊疗报告
- **PDF 生成**：集成 PDF 报告生成功能

### 2. 前端界面 (app.py)
- **Streamlit 应用**：提供用户友好的 Web 界面
- **病人信息录入**：表单式数据输入界面
- **报告展示**：格式化显示生成的诊疗报告
- **历史记录管理**：查看和管理病人历史数据
- **系统设置**：API Key 配置和系统信息

### 3. PDF 生成器 (pdf_generator.py)
- **报告格式化**：将文本报告转换为结构化 PDF
- **样式设计**：专业的医疗报告样式
- **表格生成**：实验室检查结果表格
- **多语言支持**：中文医疗术语支持

### 4. 测试脚本 (test_system.py)
- **功能验证**：测试所有核心功能模块
- **API 测试**：验证后端接口正常工作
- **集成测试**：端到端功能测试
- **错误诊断**：帮助定位系统问题

### 5. 启动脚本 (start.py)
- **一键启动**：同时启动前后端服务
- **依赖检查**：验证所需依赖是否安装
- **配置验证**：检查 API Key 等配置
- **服务监控**：监控服务运行状态

## 数据流图

```
用户输入 → Streamlit前端 → FastAPI后端 → OpenAI GPT-4
    ↓              ↓              ↓           ↓
病人信息 → 数据验证 → 数据库存储 → AI报告生成
    ↓              ↓              ↓           ↓
报告展示 ← PDF生成 ← 报告存储 ← 结构化输出
```

## 技术栈

| 层级 | 技术 | 用途 |
|------|------|------|
| 前端 | Streamlit | Web 用户界面 |
| 后端 | FastAPI | RESTful API 服务 |
| 数据库 | SQLite | 数据持久化存储 |
| AI 引擎 | OpenAI GPT-4 | 智能报告生成 |
| PDF 生成 | ReportLab | 专业报告输出 |
| 部署 | Python | 跨平台运行 |

## 部署架构

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   用户浏览器     │    │   Streamlit     │    │    FastAPI      │
│   (前端界面)     │◄──►│   (Web服务)     │◄──►│   (API服务)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                        │
                       ┌─────────────────┐              │
                       │   SQLite        │◄─────────────┘
                       │   (数据库)       │
                       └─────────────────┘
                                │
                       ┌─────────────────┐
                       │   OpenAI        │
                       │   (AI服务)      │
                       └─────────────────┘
```

## 快速开始

1. **安装依赖**：`pip install -r requirements.txt`
2. **配置环境**：复制 `env_example.txt` 为 `.env` 并配置 API Key
3. **运行测试**：`python test_system.py`
4. **启动系统**：`python start.py`
5. **访问界面**：打开 http://localhost:8501

## 注意事项

- 确保 OpenAI API Key 有效且有足够额度
- 系统需要网络连接以调用 OpenAI API
- PDF 生成需要 ReportLab 库支持
- 建议在 Python 3.8+ 环境中运行
