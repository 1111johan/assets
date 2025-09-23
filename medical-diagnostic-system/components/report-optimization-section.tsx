"use client"

import { useState } from "react"
import { BarChart3, ChevronDown, Sparkles, FileText, Download, Eye } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

export function ReportOptimizationSection() {
  const [optimizationType, setOptimizationType] = useState("格式优化 - 改善报告格式和结构")
  const [reportContent, setReportContent] = useState("")
  const [isOptimizing, setIsOptimizing] = useState(false)
  const [optimizedReport, setOptimizedReport] = useState("")

  const handleOptimize = () => {
    setIsOptimizing(true)

    // Simulate optimization process
    setTimeout(() => {
      setOptimizedReport(`# 优化后的医疗报告

## 患者基本信息
- **姓名**: 张某某
- **年龄**: 55岁
- **性别**: 男性
- **就诊日期**: 2024年9月20日

## 主要症状
患者主诉胸部不适，伴有轻微胸痛，持续时间约2小时。

## 检查结果

### 实验室检查
| 项目 | 结果 | 参考范围 | 状态 |
|------|------|----------|------|
| ALT | 45 U/L | 7-40 U/L | ↑ 轻度升高 |
| AST | 38 U/L | 13-35 U/L | ↑ 轻度升高 |
| 总胆红素 | 18 μmol/L | 5-21 μmol/L | 正常 |

### 影像学检查
胸部CT显示：
- 双肺纹理清晰
- 心影大小正常
- 未见明显异常

## 诊断建议
1. **初步诊断**: 疑似心绞痛
2. **建议进一步检查**: 
   - 心电图检查
   - 心肌酶谱检测
   - 冠状动脉造影（如必要）

## 治疗建议
1. 立即休息，避免剧烈活动
2. 监测生命体征
3. 必要时给予硝酸甘油舌下含服
4. 建议住院观察24-48小时

## 注意事项
- 如症状加重，立即就医
- 定期复查心电图和心肌酶
- 戒烟限酒，控制饮食

---
*本报告由AI辅助生成，仅供参考，最终诊断请以医生意见为准*`)
      setIsOptimizing(false)
    }, 2000)
  }

  return (
    <div className="p-6 space-y-8">
      {/* Header */}
      <div className="space-y-4">
        <div className="flex items-center gap-3">
          <div className="flex items-center justify-center w-6 h-6 bg-purple-100 rounded-full">
            <BarChart3 className="h-4 w-4 text-purple-600" />
          </div>
          <h2 className="text-lg font-medium text-foreground">报告整理优化</h2>
        </div>

        <div className="pl-9">
          <p className="text-sm text-muted-foreground">使用AI智能助您优化和整理医疗报告</p>
        </div>
      </div>

      {/* Optimization Type Selection */}
      <div className="space-y-4">
        <label className="text-sm text-muted-foreground">选择优化类型</label>
        <div className="relative max-w-md">
          <select
            value={optimizationType}
            onChange={(e) => setOptimizationType(e.target.value)}
            className="w-full p-3 bg-input border border-border rounded-md text-sm appearance-none pr-10"
          >
            <option value="格式优化 - 改善报告格式和结构">📝 格式优化 - 改善报告格式和结构</option>
            <option value="内容优化 - 完善医学术语和描述">📋 内容优化 - 完善医学术语和描述</option>
            <option value="结构优化 - 重新组织报告逻辑">🔄 结构优化 - 重新组织报告逻辑</option>
            <option value="语言优化 - 提升专业表达">✨ 语言优化 - 提升专业表达</option>
          </select>
          <ChevronDown className="absolute right-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground pointer-events-none" />
        </div>
      </div>

      {/* Report Input */}
      <div className="space-y-4">
        <label className="text-sm text-muted-foreground">请粘贴需要优化的医疗报告：</label>
        <textarea
          value={reportContent}
          onChange={(e) => setReportContent(e.target.value)}
          placeholder="在此输入您想要优化的医疗报告内容..."
          rows={12}
          className="w-full p-4 bg-input border border-border rounded-md text-sm resize-none focus:outline-none focus:ring-2 focus:ring-primary/20"
        />
      </div>

      {/* Optimization Button */}
      <div className="flex gap-4">
        <Button
          onClick={handleOptimize}
          disabled={!reportContent.trim() || isOptimizing}
          className="bg-purple-500 hover:bg-purple-600 text-white px-6 py-2 rounded-md text-sm font-medium flex items-center gap-2"
        >
          {isOptimizing ? (
            <>
              <Sparkles className="h-4 w-4 animate-spin" />
              优化中...
            </>
          ) : (
            <>
              <Sparkles className="h-4 w-4" />
              开始优化
            </>
          )}
        </Button>
      </div>

      {/* Optimized Report Display */}
      {optimizedReport && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-base">
              <FileText className="h-5 w-5 text-green-600" />
              优化结果
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="bg-muted p-4 rounded-md">
              <div className="prose prose-sm max-w-none">
                <pre className="whitespace-pre-wrap text-sm leading-relaxed font-sans">{optimizedReport}</pre>
              </div>
            </div>

            <div className="flex gap-2 pt-4 border-t">
              <Button variant="outline" className="flex items-center gap-2 bg-transparent">
                <Eye className="h-4 w-4" />
                预览报告
              </Button>
              <Button variant="outline" className="flex items-center gap-2 bg-transparent">
                <Download className="h-4 w-4" />
                下载报告
              </Button>
              <Button className="bg-blue-500 hover:bg-blue-600 text-white flex items-center gap-2">
                <FileText className="h-4 w-4" />
                保存到病历
              </Button>
            </div>

            {/* Optimization Summary */}
            <Card className="bg-green-50 border-green-200">
              <CardContent className="p-4">
                <div className="text-sm space-y-2">
                  <div className="font-medium text-green-800">优化摘要</div>
                  <div className="text-green-700 space-y-1">
                    <div>✅ 改善了报告结构和格式</div>
                    <div>✅ 标准化了医学术语表达</div>
                    <div>✅ 增加了表格形式的检查结果</div>
                    <div>✅ 完善了诊断建议和治疗方案</div>
                    <div>✅ 添加了注意事项和随访建议</div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </CardContent>
        </Card>
      )}
    </div>
  )
}
