"use client"

import { useState } from "react"
import { ChevronDown, Package, Minus, Plus } from "lucide-react"
import { Button } from "@/components/ui/button"

export function EvidencePackageSection() {
  const [analysisType, setAnalysisType] = useState("综合科研分析")
  const [patientData, setPatientData] = useState({
    age: 55,
    gender: "男",
    alt: 56.0,
    ast: 62.0,
    afp: 420.0,
    tumorSize: 3.5,
  })

  const updateValue = (field: string, delta: number) => {
    setPatientData((prev) => ({
      ...prev,
      [field]: Math.max(0, prev[field as keyof typeof prev] + delta),
    }))
  }

  return (
    <div className="p-6 space-y-8">
      {/* Header */}
      <div className="space-y-4">
        <div className="flex items-center gap-3">
          <div className="flex items-center justify-center w-6 h-6 bg-amber-100 rounded-full">
            <Package className="h-4 w-4 text-amber-600" />
          </div>
          <h2 className="text-lg font-medium text-foreground">科研证据包生成</h2>
        </div>

        <div className="pl-9">
          <p className="text-sm text-muted-foreground">基于多个AI模型的预测结果，生成综合性科研证据包和专业报告</p>
        </div>
      </div>

      {/* Analysis Type Selection */}
      <div className="space-y-4">
        <label className="text-sm text-muted-foreground">选择分析类型</label>
        <div className="relative max-w-md">
          <select
            value={analysisType}
            onChange={(e) => setAnalysisType(e.target.value)}
            className="w-full p-3 bg-input border border-border rounded-md text-sm appearance-none pr-10"
          >
            <option value="综合科研分析">🧬 综合科研分析</option>
            <option value="预后评估分析">📊 预后评估分析</option>
            <option value="风险分层分析">⚠️ 风险分层分析</option>
          </select>
          <ChevronDown className="absolute right-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground pointer-events-none" />
        </div>
      </div>

      {/* Patient Data Input */}
      <div className="space-y-6">
        <h3 className="text-base font-medium text-foreground">患者数据输入</h3>

        <div className="grid grid-cols-2 gap-6">
          {/* Age */}
          <div className="space-y-2">
            <label className="text-sm text-muted-foreground">年龄</label>
            <div className="flex items-center gap-2">
              <Button variant="outline" size="sm" onClick={() => updateValue("age", -1)} className="h-8 w-8 p-0">
                <Minus className="h-3 w-3" />
              </Button>
              <input
                type="number"
                value={patientData.age}
                onChange={(e) => setPatientData((prev) => ({ ...prev, age: Number.parseInt(e.target.value) || 0 }))}
                className="flex-1 p-2 bg-input border border-border rounded-md text-sm text-center"
              />
              <Button variant="outline" size="sm" onClick={() => updateValue("age", 1)} className="h-8 w-8 p-0">
                <Plus className="h-3 w-3" />
              </Button>
            </div>
          </div>

          {/* ALT */}
          <div className="space-y-2">
            <label className="text-sm text-muted-foreground">ALT (U/L)</label>
            <div className="flex items-center gap-2">
              <Button variant="outline" size="sm" onClick={() => updateValue("alt", -1)} className="h-8 w-8 p-0">
                <Minus className="h-3 w-3" />
              </Button>
              <input
                type="number"
                value={patientData.alt.toFixed(2)}
                onChange={(e) => setPatientData((prev) => ({ ...prev, alt: Number.parseFloat(e.target.value) || 0 }))}
                className="flex-1 p-2 bg-input border border-border rounded-md text-sm text-center"
                step="0.01"
              />
              <Button variant="outline" size="sm" onClick={() => updateValue("alt", 1)} className="h-8 w-8 p-0">
                <Plus className="h-3 w-3" />
              </Button>
            </div>
          </div>

          {/* Gender */}
          <div className="space-y-2">
            <label className="text-sm text-muted-foreground">性别</label>
            <div className="relative">
              <select
                value={patientData.gender}
                onChange={(e) => setPatientData((prev) => ({ ...prev, gender: e.target.value }))}
                className="w-full p-2 bg-input border border-border rounded-md text-sm appearance-none pr-8"
              >
                <option value="男">男</option>
                <option value="女">女</option>
              </select>
              <ChevronDown className="absolute right-2 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground pointer-events-none" />
            </div>
          </div>

          {/* AST */}
          <div className="space-y-2">
            <label className="text-sm text-muted-foreground">AST (U/L)</label>
            <div className="flex items-center gap-2">
              <Button variant="outline" size="sm" onClick={() => updateValue("ast", -1)} className="h-8 w-8 p-0">
                <Minus className="h-3 w-3" />
              </Button>
              <input
                type="number"
                value={patientData.ast.toFixed(2)}
                onChange={(e) => setPatientData((prev) => ({ ...prev, ast: Number.parseFloat(e.target.value) || 0 }))}
                className="flex-1 p-2 bg-input border border-border rounded-md text-sm text-center"
                step="0.01"
              />
              <Button variant="outline" size="sm" onClick={() => updateValue("ast", 1)} className="h-8 w-8 p-0">
                <Plus className="h-3 w-3" />
              </Button>
            </div>
          </div>

          {/* AFP */}
          <div className="space-y-2">
            <label className="text-sm text-muted-foreground">AFP (ng/mL)</label>
            <div className="flex items-center gap-2">
              <Button variant="outline" size="sm" onClick={() => updateValue("afp", -10)} className="h-8 w-8 p-0">
                <Minus className="h-3 w-3" />
              </Button>
              <input
                type="number"
                value={patientData.afp.toFixed(2)}
                onChange={(e) => setPatientData((prev) => ({ ...prev, afp: Number.parseFloat(e.target.value) || 0 }))}
                className="flex-1 p-2 bg-input border border-border rounded-md text-sm text-center"
                step="0.01"
              />
              <Button variant="outline" size="sm" onClick={() => updateValue("afp", 10)} className="h-8 w-8 p-0">
                <Plus className="h-3 w-3" />
              </Button>
            </div>
          </div>

          {/* Tumor Size */}
          <div className="space-y-2">
            <label className="text-sm text-muted-foreground">肿瘤大小 (cm)</label>
            <div className="flex items-center gap-2">
              <Button
                variant="outline"
                size="sm"
                onClick={() => updateValue("tumorSize", -0.1)}
                className="h-8 w-8 p-0"
              >
                <Minus className="h-3 w-3" />
              </Button>
              <input
                type="number"
                value={patientData.tumorSize.toFixed(2)}
                onChange={(e) =>
                  setPatientData((prev) => ({ ...prev, tumorSize: Number.parseFloat(e.target.value) || 0 }))
                }
                className="flex-1 p-2 bg-input border border-border rounded-md text-sm text-center"
                step="0.01"
              />
              <Button variant="outline" size="sm" onClick={() => updateValue("tumorSize", 0.1)} className="h-8 w-8 p-0">
                <Plus className="h-3 w-3" />
              </Button>
            </div>
          </div>
        </div>

        <div className="pt-4">
          <Button className="bg-blue-500 hover:bg-blue-600 text-white px-6 py-2 rounded-md text-sm font-medium flex items-center gap-2">
            <Package className="h-4 w-4" />
            生成科研证据包
          </Button>
        </div>
      </div>
    </div>
  )
}
