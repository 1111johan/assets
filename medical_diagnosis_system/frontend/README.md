# 医疗AI科研系统 - 前端

基于Next.js 14构建的现代化医疗AI系统前端界面。

## 🚀 快速开始

### 安装依赖

```bash
npm install
```

### 本地开发

```bash
npm run dev
```

访问 [http://localhost:3000](http://localhost:3000) 查看应用。

### 构建生产版本

```bash
npm run build
npm start
```

## 🛠️ 技术栈

- **框架**: Next.js 14
- **语言**: TypeScript
- **样式**: Tailwind CSS
- **UI组件**: 自定义组件 + Lucide React图标
- **表单**: React Hook Form + Zod验证
- **状态管理**: React Hooks
- **HTTP客户端**: Axios
- **通知**: React Hot Toast

## 📁 项目结构

```
frontend/
├── app/                    # Next.js App Router
│   ├── globals.css        # 全局样式
│   ├── layout.tsx         # 根布局
│   └── page.tsx          # 首页
├── components/            # React组件
│   ├── Header.tsx        # 页面头部
│   ├── Sidebar.tsx       # 侧边栏导航
│   ├── NewPatientForm.tsx # 新增病人表单
│   ├── HistoryPage.tsx   # 历史记录页面
│   ├── AIChatPage.tsx    # AI对话页面
│   ├── ReportOptimizePage.tsx # 报告优化页面
│   ├── SymptomAnalysisPage.tsx # 症状分析页面
│   ├── ResearchDataPage.tsx # 科研数据页面
│   ├── ModelTrainingPage.tsx # 模型训练页面
│   ├── EvidenceBundlePage.tsx # 证据包页面
│   └── SettingsPage.tsx  # 设置页面
├── public/               # 静态资源
├── package.json         # 项目配置
├── next.config.js       # Next.js配置
├── tailwind.config.js   # Tailwind配置
├── tsconfig.json        # TypeScript配置
└── env.example         # 环境变量示例
```

## 🎨 功能特性

### 核心功能
- **病人管理**: 录入、查看、管理病人信息
- **AI诊疗**: 生成中西医结合诊疗报告
- **智能对话**: AI医疗助手实时问答
- **症状分析**: 基于症状描述进行初步分析
- **报告优化**: AI辅助报告整理和优化
- **科研分析**: 数据分析和模型训练
- **证据包**: 生成综合性科研证据包

### UI特性
- **响应式设计**: 适配桌面和移动设备
- **现代化界面**: 基于Tailwind CSS的美观设计
- **交互友好**: 流畅的用户体验
- **主题一致**: 统一的视觉风格

## 🔧 配置说明

### 环境变量

创建 `.env.local` 文件：

```bash
# API配置
API_BASE_URL=http://localhost:3000/api

# 系统配置
NEXT_PUBLIC_APP_NAME=医疗AI科研系统
NEXT_PUBLIC_APP_VERSION=2.0.0
```

### API集成

前端通过以下API端点与后端通信：

- `POST /api/generate_report` - 生成诊疗报告
- `POST /api/chat` - AI对话
- `POST /api/optimize_report` - 报告优化
- `POST /api/analyze_symptoms` - 症状分析

## 📱 页面说明

### 1. 新增病人报告
- 病人基本信息录入
- 临床信息填写
- 实验室检查结果
- 影像学检查
- AI报告生成

### 2. 查看历史记录
- 病人列表展示
- 搜索和筛选
- 详细报告查看
- 数据导出

### 3. AI对话助手
- 实时对话界面
- 医疗问题咨询
- 对话历史管理
- 智能回复

### 4. 报告整理优化
- 报告格式优化
- 内容简化
- 信息增强
- 摘要生成

### 5. 症状分析
- 症状描述录入
- 严重程度评估
- AI初步分析
- 医学建议

### 6. 科研数据分析
- 数据创建
- 探索性分析
- 特征工程
- 质量评估

### 7. 模型训练
- 诊断模型训练
- 生存分析模型
- 复发预测模型
- 性能评估

### 8. 证据包生成
- 综合预测结果
- 科研报告生成
- 多维度分析
- 证据整合

### 9. 系统设置
- API配置
- 系统信息
- 功能说明
- 使用指南

## 🎯 开发指南

### 添加新页面

1. 在 `components/` 目录创建新组件
2. 在 `app/page.tsx` 中添加路由
3. 在 `components/Sidebar.tsx` 中添加导航项

### 样式规范

使用Tailwind CSS类名：

```tsx
// 按钮样式
className="btn-primary"     // 主要按钮
className="btn-secondary"   // 次要按钮

// 输入框样式
className="input-field"     // 标准输入框

// 卡片样式
className="card"           // 卡片容器

// 标题样式
className="section-header" // 章节标题
```

### 表单处理

使用React Hook Form + Zod：

```tsx
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'

const schema = z.object({
  name: z.string().min(1, '姓名不能为空'),
  age: z.number().min(0).max(120),
})

const { register, handleSubmit, formState: { errors } } = useForm({
  resolver: zodResolver(schema)
})
```

### API调用

使用Axios进行HTTP请求：

```tsx
import axios from 'axios'

const response = await axios.post('/api/generate_report', {
  patient: patientData,
  report_type: 'comprehensive'
})
```

## 🚀 部署

### Vercel部署

1. 安装Vercel CLI：
```bash
npm install -g vercel
```

2. 登录并部署：
```bash
vercel login
vercel
```

3. 配置环境变量：
在Vercel Dashboard中设置环境变量

### 其他平台

支持部署到任何支持Next.js的平台：
- Netlify
- Railway
- Render
- AWS Amplify

## 🔍 故障排除

### 常见问题

1. **构建失败**
   - 检查TypeScript类型错误
   - 确认所有依赖已安装
   - 查看构建日志

2. **API调用失败**
   - 检查API端点配置
   - 确认后端服务运行
   - 查看网络请求日志

3. **样式问题**
   - 确认Tailwind CSS配置
   - 检查类名拼写
   - 验证响应式断点

### 调试工具

- 使用浏览器开发者工具
- 启用React DevTools
- 查看Next.js构建分析

## 📚 学习资源

- [Next.js文档](https://nextjs.org/docs)
- [React文档](https://react.dev/)
- [Tailwind CSS文档](https://tailwindcss.com/docs)
- [TypeScript文档](https://www.typescriptlang.org/docs/)

## 🤝 贡献指南

1. Fork项目
2. 创建功能分支
3. 提交更改
4. 创建Pull Request

## 📄 许可证

MIT License

---

**注意**: 本系统仅供医疗参考，不能替代专业医生诊断。请遵守相关法律法规和医疗伦理。
