"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { User, Calendar, FileText, Download, ChevronRight } from "lucide-react"

// Mock lab results data
const labResults = [
  { id: 0, name: "ALT", value: 40, unit: "U/L", normal: "7-40" },
  { id: 1, name: "AST", value: 40, unit: "U/L", normal: "13-35" },
  { id: 2, name: "ALP", value: 100, unit: "U/L", normal: "45-125" },
  { id: 3, name: "总胆红素", value: 20, unit: "μmol/L", normal: "3.4-20.5" },
  { id: 4, name: "直接胆红素", value: 5, unit: "μmol/L", normal: "0-6.8" },
  { id: 5, name: "白蛋白", value: 40, unit: "g/L", normal: "40-55" },
  { id: 6, name: "AFP", value: 20, unit: "ng/mL", normal: "0-20" },
  { id: 7, name: "CA19-9", value: 37, unit: "U/mL", normal: "0-37" },
  { id: 8, name: "CEA", value: 5, unit: "ng/mL", normal: "0-5" },
]

export function PatientDetailSection() {
  const [selectedReport, setSelectedReport] = useState("报告 1 - 2025-09-19 14:03:46")

  return (
    <div className="space-y-6">
      {/* Patient Basic Info */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card className="border-border/50 bg-card/50 backdrop-blur-sm">
          <CardContent className="p-6">
            <div className="flex items-center gap-3 mb-4">
              <User className="w-5 h-5 text-primary" />
              <h3 className="font-semibold text-lg">基本信息</h3>
            </div>
            <div className="space-y-3">
              <div>
                <label className="text-sm font-medium text-muted-foreground">年龄</label>
                <p className="text-2xl font-bold">50岁</p>
              </div>
              <div>
                <label className="text-sm font-medium text-muted-foreground">主诉</label>
                <p className="font-medium">心绞痛</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="border-border/50 bg-card/50 backdrop-blur-sm">
          <CardContent className="p-6">
            <div className="flex items-center gap-3 mb-4">
              <Calendar className="w-5 h-5 text-primary" />
              <h3 className="font-semibold text-lg">记录信息</h3>
            </div>
            <div>
              <label className="text-sm font-medium text-muted-foreground">创建时间</label>
              <p className="text-lg font-mono">2025-09-19 14:01:52</p>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Lab Results */}
      <Card className="border-border/50 bg-card/50 backdrop-blur-sm">
        <CardHeader className="pb-4">
          <CardTitle className="text-lg">实验室检查结果</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="border-b border-border/30 bg-accent/20">
                <tr>
                  <th className="text-left p-3 font-medium text-muted-foreground">检查项目</th>
                  <th className="text-right p-3 font-medium text-muted-foreground">结果</th>
                  <th className="text-center p-3 font-medium text-muted-foreground">参考范围</th>
                  <th className="text-center p-3 font-medium text-muted-foreground">状态</th>
                </tr>
              </thead>
              <tbody>
                {labResults.map((result) => {
                  const isAbnormal = result.name === "ALP" && result.value === 100
                  return (
                    <tr key={result.id} className="border-b border-border/20 hover:bg-accent/20">
                      <td className="p-3 font-medium">{result.name}</td>
                      <td className="p-3 text-right font-mono">
                        <span className={isAbnormal ? "text-orange-600 dark:text-orange-400 font-semibold" : ""}>
                          {result.value}
                        </span>
                        {result.unit && <span className="text-muted-foreground ml-1">{result.unit}</span>}
                      </td>
                      <td className="p-3 text-center text-muted-foreground font-mono text-sm">{result.normal}</td>
                      <td className="p-3 text-center">
                        <Badge
                          variant={isAbnormal ? "destructive" : "secondary"}
                          className={
                            isAbnormal
                              ? "bg-orange-100 dark:bg-orange-900/30 text-orange-800 dark:text-orange-400"
                              : "bg-green-100 dark:bg-green-900/30 text-green-800 dark:text-green-400"
                          }
                        >
                          {isAbnormal ? "偏高" : "正常"}
                        </Badge>
                      </td>
                    </tr>
                  )
                })}
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>

      {/* Diagnostic Reports */}
      <Card className="border-border/50 bg-card/50 backdrop-blur-sm">
        <CardHeader className="pb-4">
          <div className="flex items-center gap-3">
            <FileText className="w-5 h-5 text-primary" />
            <CardTitle className="text-lg">诊疗报告</CardTitle>
          </div>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="flex items-center justify-between p-4 bg-accent/20 rounded-lg border border-border/30 hover:bg-accent/30 transition-colors cursor-pointer">
              <div className="flex items-center gap-3">
                <ChevronRight className="w-4 h-4 text-muted-foreground" />
                <span className="font-medium">{selectedReport}</span>
              </div>
              <Button variant="outline" size="sm" className="border-border/50 bg-transparent">
                <Download className="w-4 h-4 mr-2" />
                下载报告
              </Button>
            </div>

            <div className="p-4 bg-accent/10 rounded-lg border border-border/20">
              <p className="text-sm text-muted-foreground">点击上方报告可查看详细内容，或下载完整的诊疗报告文档。</p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
