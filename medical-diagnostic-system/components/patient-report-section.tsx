"use client"

import { useState } from "react"
import { ChevronDown, FileText, Minus, Plus } from "lucide-react"
import { Button } from "@/components/ui/button"

export function PatientReportSection() {
  const [patientInfo, setPatientInfo] = useState({
    name: "",
    age: 50,
    gender: "男",
    chiefComplaint: "",
    medicalHistory: "",
    // Lab values
    alt: 40.0,
    ast: 40.0,
    alp: 100.0,
    totalBilirubin: 20.0,
    directBilirubin: 5.0,
    albumin: 40.0,
    afp: 20.0,
    ca199: 37.0,
    cea: 5.0,
  })

  const updateLabValue = (field: string, delta: number) => {
    setPatientInfo((prev) => ({
      ...prev,
      [field]: Math.max(0, prev[field as keyof typeof prev] + delta),
    }))
  }

  return (
    <div className="p-6 space-y-8">
      {/* Header */}
      <div className="space-y-4">
        <div className="flex items-center gap-3">
          <div className="flex items-center justify-center w-6 h-6 bg-green-100 rounded-full">
            <FileText className="h-4 w-4 text-green-600" />
          </div>
          <h2 className="text-lg font-medium text-foreground">新增病人诊疗报告</h2>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-8">
        {/* Basic Information */}
        <div className="space-y-6">
          <h3 className="text-base font-medium text-foreground">基本信息</h3>

          <div className="space-y-4">
            <div className="space-y-2">
              <label className="text-sm text-muted-foreground">姓名 *</label>
              <input
                type="text"
                value={patientInfo.name}
                onChange={(e) => setPatientInfo((prev) => ({ ...prev, name: e.target.value }))}
                placeholder="请输入病人姓名"
                className="w-full p-3 bg-input border border-border rounded-md text-sm"
              />
            </div>

            <div className="space-y-2">
              <label className="text-sm text-muted-foreground">年龄 *</label>
              <div className="flex items-center gap-2">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => setPatientInfo((prev) => ({ ...prev, age: Math.max(0, prev.age - 1) }))}
                  className="h-8 w-8 p-0"
                >
                  <Minus className="h-3 w-3" />
                </Button>
                <input
                  type="number"
                  value={patientInfo.age}
                  onChange={(e) => setPatientInfo((prev) => ({ ...prev, age: Number.parseInt(e.target.value) || 0 }))}
                  className="flex-1 p-2 bg-input border border-border rounded-md text-sm text-center"
                />
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => setPatientInfo((prev) => ({ ...prev, age: prev.age + 1 }))}
                  className="h-8 w-8 p-0"
                >
                  <Plus className="h-3 w-3" />
                </Button>
              </div>
            </div>

            <div className="space-y-2">
              <label className="text-sm text-muted-foreground">性别 *</label>
              <div className="relative">
                <select
                  value={patientInfo.gender}
                  onChange={(e) => setPatientInfo((prev) => ({ ...prev, gender: e.target.value }))}
                  className="w-full p-3 bg-input border border-border rounded-md text-sm appearance-none pr-10"
                >
                  <option value="男">男</option>
                  <option value="女">女</option>
                </select>
                <ChevronDown className="absolute right-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground pointer-events-none" />
              </div>
            </div>
          </div>
        </div>

        {/* Clinical Information */}
        <div className="space-y-6">
          <h3 className="text-base font-medium text-foreground">临床信息</h3>

          <div className="space-y-4">
            <div className="space-y-2">
              <label className="text-sm text-muted-foreground">主诉 *</label>
              <textarea
                value={patientInfo.chiefComplaint}
                onChange={(e) => setPatientInfo((prev) => ({ ...prev, chiefComplaint: e.target.value }))}
                placeholder="请详细描述主要症状和持续时间"
                rows={3}
                className="w-full p-3 bg-input border border-border rounded-md text-sm resize-none"
              />
            </div>

            <div className="space-y-2">
              <label className="text-sm text-muted-foreground">既往病史</label>
              <textarea
                value={patientInfo.medicalHistory}
                onChange={(e) => setPatientInfo((prev) => ({ ...prev, medicalHistory: e.target.value }))}
                placeholder="请描述相关既往病史、手术史、过敏史等"
                rows={3}
                className="w-full p-3 bg-input border border-border rounded-md text-sm resize-none"
              />
            </div>
          </div>
        </div>
      </div>

      {/* Laboratory Results */}
      <div className="space-y-6">
        <h3 className="text-base font-medium text-foreground">检查结果</h3>

        <div className="space-y-4">
          <h4 className="text-sm font-medium text-muted-foreground">实验室检查</h4>

          <div className="grid grid-cols-3 gap-4">
            {/* ALT */}
            <div className="space-y-2">
              <label className="text-sm text-muted-foreground">ALT (U/L)</label>
              <div className="flex items-center gap-1">
                <Button variant="outline" size="sm" onClick={() => updateLabValue("alt", -1)} className="h-7 w-7 p-0">
                  <Minus className="h-3 w-3" />
                </Button>
                <input
                  type="number"
                  value={patientInfo.alt.toFixed(2)}
                  onChange={(e) => setPatientInfo((prev) => ({ ...prev, alt: Number.parseFloat(e.target.value) || 0 }))}
                  className="flex-1 p-2 bg-input border border-border rounded-md text-xs text-center"
                  step="0.01"
                />
                <Button variant="outline" size="sm" onClick={() => updateLabValue("alt", 1)} className="h-7 w-7 p-0">
                  <Plus className="h-3 w-3" />
                </Button>
              </div>
            </div>

            {/* Total Bilirubin */}
            <div className="space-y-2">
              <label className="text-sm text-muted-foreground">总胆红素 (μmol/L)</label>
              <div className="flex items-center gap-1">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => updateLabValue("totalBilirubin", -1)}
                  className="h-7 w-7 p-0"
                >
                  <Minus className="h-3 w-3" />
                </Button>
                <input
                  type="number"
                  value={patientInfo.totalBilirubin.toFixed(2)}
                  onChange={(e) =>
                    setPatientInfo((prev) => ({ ...prev, totalBilirubin: Number.parseFloat(e.target.value) || 0 }))
                  }
                  className="flex-1 p-2 bg-input border border-border rounded-md text-xs text-center"
                  step="0.01"
                />
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => updateLabValue("totalBilirubin", 1)}
                  className="h-7 w-7 p-0"
                >
                  <Plus className="h-3 w-3" />
                </Button>
              </div>
            </div>

            {/* AFP */}
            <div className="space-y-2">
              <label className="text-sm text-muted-foreground">AFP (ng/mL)</label>
              <div className="flex items-center gap-1">
                <Button variant="outline" size="sm" onClick={() => updateLabValue("afp", -1)} className="h-7 w-7 p-0">
                  <Minus className="h-3 w-3" />
                </Button>
                <input
                  type="number"
                  value={patientInfo.afp.toFixed(2)}
                  onChange={(e) => setPatientInfo((prev) => ({ ...prev, afp: Number.parseFloat(e.target.value) || 0 }))}
                  className="flex-1 p-2 bg-input border border-border rounded-md text-xs text-center"
                  step="0.01"
                />
                <Button variant="outline" size="sm" onClick={() => updateLabValue("afp", 1)} className="h-7 w-7 p-0">
                  <Plus className="h-3 w-3" />
                </Button>
              </div>
            </div>

            {/* AST */}
            <div className="space-y-2">
              <label className="text-sm text-muted-foreground">AST (U/L)</label>
              <div className="flex items-center gap-1">
                <Button variant="outline" size="sm" onClick={() => updateLabValue("ast", -1)} className="h-7 w-7 p-0">
                  <Minus className="h-3 w-3" />
                </Button>
                <input
                  type="number"
                  value={patientInfo.ast.toFixed(2)}
                  onChange={(e) => setPatientInfo((prev) => ({ ...prev, ast: Number.parseFloat(e.target.value) || 0 }))}
                  className="flex-1 p-2 bg-input border border-border rounded-md text-xs text-center"
                  step="0.01"
                />
                <Button variant="outline" size="sm" onClick={() => updateLabValue("ast", 1)} className="h-7 w-7 p-0">
                  <Plus className="h-3 w-3" />
                </Button>
              </div>
            </div>

            {/* Direct Bilirubin */}
            <div className="space-y-2">
              <label className="text-sm text-muted-foreground">直接胆红素 (μmol/L)</label>
              <div className="flex items-center gap-1">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => updateLabValue("directBilirubin", -1)}
                  className="h-7 w-7 p-0"
                >
                  <Minus className="h-3 w-3" />
                </Button>
                <input
                  type="number"
                  value={patientInfo.directBilirubin.toFixed(2)}
                  onChange={(e) =>
                    setPatientInfo((prev) => ({ ...prev, directBilirubin: Number.parseFloat(e.target.value) || 0 }))
                  }
                  className="flex-1 p-2 bg-input border border-border rounded-md text-xs text-center"
                  step="0.01"
                />
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => updateLabValue("directBilirubin", 1)}
                  className="h-7 w-7 p-0"
                >
                  <Plus className="h-3 w-3" />
                </Button>
              </div>
            </div>

            {/* CA19-9 */}
            <div className="space-y-2">
              <label className="text-sm text-muted-foreground">CA19-9 (U/mL)</label>
              <div className="flex items-center gap-1">
                <Button variant="outline" size="sm" onClick={() => updateLabValue("ca199", -1)} className="h-7 w-7 p-0">
                  <Minus className="h-3 w-3" />
                </Button>
                <input
                  type="number"
                  value={patientInfo.ca199.toFixed(2)}
                  onChange={(e) =>
                    setPatientInfo((prev) => ({ ...prev, ca199: Number.parseFloat(e.target.value) || 0 }))
                  }
                  className="flex-1 p-2 bg-input border border-border rounded-md text-xs text-center"
                  step="0.01"
                />
                <Button variant="outline" size="sm" onClick={() => updateLabValue("ca199", 1)} className="h-7 w-7 p-0">
                  <Plus className="h-3 w-3" />
                </Button>
              </div>
            </div>

            {/* ALP */}
            <div className="space-y-2">
              <label className="text-sm text-muted-foreground">ALP (U/L)</label>
              <div className="flex items-center gap-1">
                <Button variant="outline" size="sm" onClick={() => updateLabValue("alp", -1)} className="h-7 w-7 p-0">
                  <Minus className="h-3 w-3" />
                </Button>
                <input
                  type="number"
                  value={patientInfo.alp.toFixed(2)}
                  onChange={(e) => setPatientInfo((prev) => ({ ...prev, alp: Number.parseFloat(e.target.value) || 0 }))}
                  className="flex-1 p-2 bg-input border border-border rounded-md text-xs text-center"
                  step="0.01"
                />
                <Button variant="outline" size="sm" onClick={() => updateLabValue("alp", 1)} className="h-7 w-7 p-0">
                  <Plus className="h-3 w-3" />
                </Button>
              </div>
            </div>

            {/* Albumin */}
            <div className="space-y-2">
              <label className="text-sm text-muted-foreground">白蛋白 (g/L)</label>
              <div className="flex items-center gap-1">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => updateLabValue("albumin", -1)}
                  className="h-7 w-7 p-0"
                >
                  <Minus className="h-3 w-3" />
                </Button>
                <input
                  type="number"
                  value={patientInfo.albumin.toFixed(2)}
                  onChange={(e) =>
                    setPatientInfo((prev) => ({ ...prev, albumin: Number.parseFloat(e.target.value) || 0 }))
                  }
                  className="flex-1 p-2 bg-input border border-border rounded-md text-xs text-center"
                  step="0.01"
                />
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => updateLabValue("albumin", 1)}
                  className="h-7 w-7 p-0"
                >
                  <Plus className="h-3 w-3" />
                </Button>
              </div>
            </div>

            {/* CEA */}
            <div className="space-y-2">
              <label className="text-sm text-muted-foreground">CEA (ng/mL)</label>
              <div className="flex items-center gap-1">
                <Button variant="outline" size="sm" onClick={() => updateLabValue("cea", -1)} className="h-7 w-7 p-0">
                  <Minus className="h-3 w-3" />
                </Button>
                <input
                  type="number"
                  value={patientInfo.cea.toFixed(2)}
                  onChange={(e) => setPatientInfo((prev) => ({ ...prev, cea: Number.parseFloat(e.target.value) || 0 }))}
                  className="flex-1 p-2 bg-input border border-border rounded-md text-xs text-center"
                  step="0.01"
                />
                <Button variant="outline" size="sm" onClick={() => updateLabValue("cea", 1)} className="h-7 w-7 p-0">
                  <Plus className="h-3 w-3" />
                </Button>
              </div>
            </div>
          </div>
        </div>

        <div className="space-y-2">
          <h4 className="text-sm font-medium text-muted-foreground">影像学检查</h4>
          <textarea
            placeholder="请描述CT、MRI、超声等影像学检查结果..."
            rows={3}
            className="w-full p-3 bg-input border border-border rounded-md text-sm resize-none"
          />
        </div>
      </div>
    </div>
  )
}
