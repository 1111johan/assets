"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Badge } from "@/components/ui/badge"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { History, Search, Download, Filter, User } from "lucide-react"

// Mock patient data
const mockPatients = [
  {
    id: 13,
    name: "杜坤源",
    age: 50,
    gender: "男",
    complaint: "心绞痛",
    createdAt: "2025-09-19 14:01:52",
    status: "已生成",
  },
  {
    id: 12,
    name: "杜坤源",
    age: 50,
    gender: "男",
    complaint: "心绞痛",
    createdAt: "2025-09-18 15:22:07",
    status: "已生成",
  },
  {
    id: 11,
    name: "杜坤源",
    age: 50,
    gender: "男",
    complaint: "心绞痛",
    createdAt: "2025-09-18 15:20:43",
    status: "已生成",
  },
  {
    id: 10,
    name: "完整性测试患者",
    age: 45,
    gender: "男",
    complaint: "右上腹疼痛2周",
    createdAt: "2025-09-18 15:13:16",
    status: "已生成",
  },
  {
    id: 9,
    name: "测试患者",
    age: 45,
    gender: "男",
    complaint: "右上腹疼痛2周",
    createdAt: "2025-09-18 14:50:03",
    status: "已生成",
  },
  {
    id: 8,
    name: "杜坤源",
    age: 50,
    gender: "男",
    complaint: "脑出血",
    createdAt: "2025-09-17 06:40:18",
    status: "已生成",
  },
  {
    id: 7,
    name: "杜坤源",
    age: 50,
    gender: "男",
    complaint: "脑出血",
    createdAt: "2025-09-17 06:21:23",
    status: "已生成",
  },
  {
    id: 6,
    name: "杜坤源",
    age: 50,
    gender: "男",
    complaint: "脑出血",
    createdAt: "2025-09-17 06:20:40",
    status: "已生成",
  },
  {
    id: 5,
    name: "杜坤源",
    age: 50,
    gender: "男",
    complaint: "脑出血",
    createdAt: "2025-09-17 06:19:51",
    status: "已生成",
  },
  {
    id: 4,
    name: "杜坤源",
    age: 50,
    gender: "男",
    complaint: "脑出血",
    createdAt: "2025-09-17 06:18:22",
    status: "已生成",
  },
]

export function HistoryRecordsSection() {
  const [searchTerm, setSearchTerm] = useState("")
  const [selectedPatient, setSelectedPatient] = useState<number | null>(null)

  const filteredPatients = mockPatients.filter(
    (patient) =>
      patient.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      patient.complaint.toLowerCase().includes(searchTerm.toLowerCase()),
  )

  const selectedPatientData = mockPatients.find((p) => p.id === selectedPatient)

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center gap-3 mb-8">
        <div className="w-10 h-10 bg-primary/20 rounded-xl flex items-center justify-center">
          <History className="w-5 h-5 text-primary" />
        </div>
        <div>
          <h1 className="text-2xl font-bold text-foreground">查看历史记录</h1>
        </div>
      </div>

      {/* Success Alert */}
      <div className="bg-green-50 dark:bg-green-950/20 border border-green-200 dark:border-green-800/30 rounded-lg p-4">
        <div className="flex items-center gap-2 text-green-800 dark:text-green-400">
          <div className="w-4 h-4 bg-green-500 rounded-full flex items-center justify-center">
            <span className="text-white text-xs">✓</span>
          </div>
          <span className="font-medium">找到 {filteredPatients.length} 条病人记录</span>
        </div>
      </div>

      {/* Search and Filters */}
      <Card className="border-border/50 bg-card/50 backdrop-blur-sm">
        <CardContent className="p-4">
          <div className="flex items-center gap-4">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-muted-foreground" />
              <Input
                placeholder="输入姓名或主诉关键词"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-10 bg-input/50 border-border/50 focus:border-primary"
              />
            </div>
            <Button variant="outline" size="sm" className="border-border/50 bg-transparent">
              <Download className="w-4 h-4 mr-2" />
              导出
            </Button>
            <Button variant="outline" size="sm" className="border-border/50 bg-transparent">
              <Filter className="w-4 h-4 mr-2" />
              筛选
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Patient Records Table */}
      <Card className="border-border/50 bg-card/50 backdrop-blur-sm">
        <CardContent className="p-0">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="border-b border-border/30 bg-accent/20">
                <tr>
                  <th className="text-left p-4 font-medium text-muted-foreground">ID</th>
                  <th className="text-left p-4 font-medium text-muted-foreground">姓名</th>
                  <th className="text-left p-4 font-medium text-muted-foreground">年龄</th>
                  <th className="text-left p-4 font-medium text-muted-foreground">性别</th>
                  <th className="text-left p-4 font-medium text-muted-foreground">主诉</th>
                  <th className="text-left p-4 font-medium text-muted-foreground">创建时间</th>
                  <th className="text-left p-4 font-medium text-muted-foreground">报告状态</th>
                </tr>
              </thead>
              <tbody>
                {filteredPatients.map((patient, index) => (
                  <tr
                    key={patient.id}
                    className={`border-b border-border/20 hover:bg-accent/30 cursor-pointer transition-colors ${
                      selectedPatient === patient.id ? "bg-primary/10" : ""
                    }`}
                    onClick={() => setSelectedPatient(patient.id)}
                  >
                    <td className="p-4 text-muted-foreground">{index}</td>
                    <td className="p-4 font-medium">{patient.name}</td>
                    <td className="p-4 text-muted-foreground">{patient.age}</td>
                    <td className="p-4 text-muted-foreground">{patient.gender}</td>
                    <td className="p-4">{patient.complaint}</td>
                    <td className="p-4 text-muted-foreground font-mono text-sm">{patient.createdAt}</td>
                    <td className="p-4">
                      <Badge
                        variant="secondary"
                        className="bg-green-100 dark:bg-green-900/30 text-green-800 dark:text-green-400"
                      >
                        {patient.status}
                      </Badge>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>

      {/* Patient Detail Selection */}
      <Card className="border-border/50 bg-card/50 backdrop-blur-sm">
        <CardHeader className="pb-4">
          <div className="flex items-center gap-3">
            <User className="w-5 h-5 text-primary" />
            <CardTitle className="text-lg">病人详细信息</CardTitle>
          </div>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div>
              <label className="text-sm font-medium text-muted-foreground mb-2 block">选择病人查看详细报告</label>
              <Select
                value={selectedPatient?.toString() || ""}
                onValueChange={(value) => setSelectedPatient(Number.parseInt(value))}
              >
                <SelectTrigger className="bg-input/50 border-border/50 focus:border-primary">
                  <SelectValue placeholder="选择病人..." />
                </SelectTrigger>
                <SelectContent>
                  {mockPatients.map((patient) => (
                    <SelectItem key={patient.id} value={patient.id.toString()}>
                      {patient.id} - {patient.name} ({patient.complaint})
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            {selectedPatientData && (
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 p-4 bg-accent/20 rounded-lg border border-border/30">
                <div>
                  <label className="text-xs font-medium text-muted-foreground">姓名</label>
                  <p className="font-medium">{selectedPatientData.name}</p>
                </div>
                <div>
                  <label className="text-xs font-medium text-muted-foreground">性别</label>
                  <p className="font-medium">{selectedPatientData.gender}</p>
                </div>
                <div>
                  <label className="text-xs font-medium text-muted-foreground">年龄</label>
                  <p className="font-medium">{selectedPatientData.age}岁</p>
                </div>
                <div>
                  <label className="text-xs font-medium text-muted-foreground">报告数量</label>
                  <p className="font-medium">1</p>
                </div>
              </div>
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
