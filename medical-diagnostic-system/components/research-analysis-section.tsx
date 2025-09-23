"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { TrendingUp, Database, Plus, Minus, BarChart3 } from "lucide-react"

export function ResearchAnalysisSection() {
  const [patientCount, setPatientCount] = useState(500)

  const handleCountChange = (increment: boolean) => {
    setPatientCount((prev) => (increment ? prev + 1 : Math.max(0, prev - 1)))
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center gap-3 mb-8">
        <div className="w-10 h-10 bg-primary/20 rounded-xl flex items-center justify-center">
          <TrendingUp className="w-5 h-5 text-primary" />
        </div>
        <div>
          <h1 className="text-2xl font-bold text-foreground">科研数据分析</h1>
          <p className="text-muted-foreground mt-1">进行探索性数据分析，转证工程和数据质量评估</p>
        </div>
      </div>

      {/* Data Preparation Card */}
      <Card className="border-border/50 bg-card/50 backdrop-blur-sm">
        <CardHeader className="pb-4">
          <CardTitle className="text-lg font-semibold text-card-foreground">数据准备</CardTitle>
        </CardHeader>
        <CardContent className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Patient Count */}
            <div className="space-y-3">
              <Label htmlFor="patient-count" className="text-sm font-medium text-muted-foreground">
                患者数量
              </Label>
              <div className="flex items-center gap-2">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => handleCountChange(false)}
                  className="h-10 w-10 p-0 border-border/50 hover:bg-accent"
                >
                  <Minus className="w-4 h-4" />
                </Button>
                <Input
                  id="patient-count"
                  type="number"
                  value={patientCount}
                  onChange={(e) => setPatientCount(Number.parseInt(e.target.value) || 0)}
                  className="text-center font-mono text-lg bg-input/50 border-border/50 focus:border-primary"
                />
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => handleCountChange(true)}
                  className="h-10 w-10 p-0 border-border/50 hover:bg-accent"
                >
                  <Plus className="w-4 h-4" />
                </Button>
              </div>
            </div>

            {/* Create Example Data */}
            <div className="space-y-3">
              <Label className="text-sm font-medium text-muted-foreground">创建示例数据</Label>
              <Button
                variant="outline"
                className="w-full h-10 border-border/50 hover:bg-accent hover:border-primary/50 transition-all duration-200 bg-transparent"
              >
                <Database className="w-4 h-4 mr-2" />
                创建示例数据
              </Button>
            </div>
          </div>

          {/* Analysis Options */}
          <div className="pt-4 border-t border-border/30">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <Card className="border-border/30 bg-accent/20 hover:bg-accent/30 transition-colors cursor-pointer">
                <CardContent className="p-4 text-center">
                  <BarChart3 className="w-8 h-8 text-primary mx-auto mb-2" />
                  <h3 className="font-medium text-sm text-card-foreground">数据分布分析</h3>
                  <p className="text-xs text-muted-foreground mt-1">分析患者数据分布特征</p>
                </CardContent>
              </Card>

              <Card className="border-border/30 bg-accent/20 hover:bg-accent/30 transition-colors cursor-pointer">
                <CardContent className="p-4 text-center">
                  <TrendingUp className="w-8 h-8 text-primary mx-auto mb-2" />
                  <h3 className="font-medium text-sm text-card-foreground">趋势分析</h3>
                  <p className="text-xs text-muted-foreground mt-1">识别数据变化趋势</p>
                </CardContent>
              </Card>

              <Card className="border-border/30 bg-accent/20 hover:bg-accent/30 transition-colors cursor-pointer">
                <CardContent className="p-4 text-center">
                  <Database className="w-8 h-8 text-primary mx-auto mb-2" />
                  <h3 className="font-medium text-sm text-card-foreground">质量评估</h3>
                  <p className="text-xs text-muted-foreground mt-1">评估数据完整性和准确性</p>
                </CardContent>
              </Card>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
