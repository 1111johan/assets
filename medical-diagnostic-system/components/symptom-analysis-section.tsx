"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Search, Stethoscope, Clock, AlertTriangle, MapPin, Activity } from "lucide-react"

export function SymptomAnalysisSection() {
  const [formData, setFormData] = useState({
    mainSymptoms: "",
    location: "",
    duration: "",
    severity: "",
    triggers: "",
    otherInfo: "",
  })

  const handleInputChange = (field: string, value: string) => {
    setFormData((prev) => ({ ...prev, [field]: value }))
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center gap-3 mb-8">
        <div className="w-10 h-10 bg-primary/20 rounded-xl flex items-center justify-center">
          <Search className="w-5 h-5 text-primary" />
        </div>
        <div>
          <h1 className="text-2xl font-bold text-foreground">症状分析</h1>
          <p className="text-muted-foreground mt-1">输入症状描述，获取AI初步分析和医学建议</p>
        </div>
      </div>

      {/* Symptom Description Form */}
      <Card className="border-border/50 bg-card/50 backdrop-blur-sm">
        <CardHeader className="pb-4">
          <CardTitle className="text-lg font-semibold">症状描述</CardTitle>
        </CardHeader>
        <CardContent className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Main Symptoms */}
            <div className="space-y-3">
              <Label htmlFor="main-symptoms" className="text-sm font-medium flex items-center gap-2">
                <Stethoscope className="w-4 h-4 text-primary" />
                主要症状
              </Label>
              <Textarea
                id="main-symptoms"
                placeholder="请详细描述您的主要症状"
                value={formData.mainSymptoms}
                onChange={(e) => handleInputChange("mainSymptoms", e.target.value)}
                className="min-h-[100px] bg-input/50 border-border/50 focus:border-primary resize-none"
              />
            </div>

            {/* Symptom Location */}
            <div className="space-y-3">
              <Label htmlFor="location" className="text-sm font-medium flex items-center gap-2">
                <MapPin className="w-4 h-4 text-primary" />
                症状部位
              </Label>
              <Textarea
                id="location"
                placeholder="例如：右上腹、胸部、头部"
                value={formData.location}
                onChange={(e) => handleInputChange("location", e.target.value)}
                className="min-h-[100px] bg-input/50 border-border/50 focus:border-primary resize-none"
              />
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Duration */}
            <div className="space-y-3">
              <Label htmlFor="duration" className="text-sm font-medium flex items-center gap-2">
                <Clock className="w-4 h-4 text-primary" />
                持续时间
              </Label>
              <Input
                id="duration"
                placeholder="例如：3天、1周"
                value={formData.duration}
                onChange={(e) => handleInputChange("duration", e.target.value)}
                className="bg-input/50 border-border/50 focus:border-primary"
              />
            </div>

            {/* Severity */}
            <div className="space-y-3">
              <Label htmlFor="severity" className="text-sm font-medium flex items-center gap-2">
                <AlertTriangle className="w-4 h-4 text-primary" />
                严重程度
              </Label>
              <Select value={formData.severity} onValueChange={(value) => handleInputChange("severity", value)}>
                <SelectTrigger className="bg-input/50 border-border/50 focus:border-primary">
                  <SelectValue placeholder="选择严重程度" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="轻微">轻微</SelectItem>
                  <SelectItem value="中等">中等</SelectItem>
                  <SelectItem value="严重">严重</SelectItem>
                  <SelectItem value="非常严重">非常严重</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>

          <div className="space-y-3">
            <Label htmlFor="triggers" className="text-sm font-medium flex items-center gap-2">
              <Activity className="w-4 h-4 text-primary" />
              诱发因素
            </Label>
            <Textarea
              id="triggers"
              placeholder="什么情况下症状会加重？"
              value={formData.triggers}
              onChange={(e) => handleInputChange("triggers", e.target.value)}
              className="min-h-[80px] bg-input/50 border-border/50 focus:border-primary resize-none"
            />
          </div>

          <div className="space-y-3">
            <Label htmlFor="other-info" className="text-sm font-medium">
              其他信息
            </Label>
            <Textarea
              id="other-info"
              placeholder="年龄、性别、既往病史等"
              value={formData.otherInfo}
              onChange={(e) => handleInputChange("otherInfo", e.target.value)}
              className="min-h-[80px] bg-input/50 border-border/50 focus:border-primary resize-none"
            />
          </div>

          {/* Analysis Button */}
          <div className="pt-4 border-t border-border/30">
            <Button className="w-full md:w-auto bg-primary hover:bg-primary/90 text-primary-foreground" size="lg">
              <Search className="w-4 h-4 mr-2" />
              开始分析
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Analysis Results Placeholder */}
      <Card className="border-border/50 bg-card/50 backdrop-blur-sm">
        <CardHeader className="pb-4">
          <CardTitle className="text-lg font-semibold">分析结果</CardTitle>
          <CardDescription>AI将根据您的症状描述提供初步分析</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="text-center py-8 text-muted-foreground">
            <Search className="w-12 h-12 mx-auto mb-4 opacity-50" />
            <p>请填写症状信息并点击"开始分析"按钮</p>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
