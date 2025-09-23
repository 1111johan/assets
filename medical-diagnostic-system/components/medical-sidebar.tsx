"use client"

import { useState } from "react"
import {
  ChevronDown,
  Activity,
  FileText,
  History,
  MessageSquare,
  BarChart3,
  Search,
  TrendingUp,
  Package,
} from "lucide-react"
import { cn } from "@/lib/utils"

const menuItems = [
  { id: "model-training", label: "模型训练", icon: Activity },
  { id: "new-patient", label: "新增病人报告", icon: FileText },
  { id: "history", label: "查看历史记录", icon: History },
  { id: "ai-assistant", label: "AI对话助手", icon: MessageSquare },
  { id: "report-optimization", label: "报告整理优化", icon: BarChart3 },
  { id: "symptom-analysis", label: "症状分析", icon: Search },
  { id: "research-analysis", label: "科研数据分析", icon: TrendingUp },
  { id: "evidence-package", label: "证据包生成", icon: Package },
]

interface MedicalSidebarProps {
  activeSection: string
  onSectionChange: (section: string) => void
}

export function MedicalSidebar({ activeSection, onSectionChange }: MedicalSidebarProps) {
  const [selectedFunction, setSelectedFunction] = useState("模型训练")

  return (
    <div className="w-64 bg-sidebar border-r border-sidebar-border h-screen flex flex-col shrink-0">
      <div className="p-4 lg:p-6 border-b border-sidebar-border">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 bg-primary/20 rounded-lg flex items-center justify-center">
            <Activity className="w-4 h-4 text-primary" />
          </div>
          <h2 className="text-lg font-semibold text-sidebar-foreground">导航菜单</h2>
        </div>
      </div>

      <div className="p-4 border-b border-sidebar-border">
        <div className="space-y-3">
          <label className="text-xs font-medium text-muted-foreground uppercase tracking-wider">选择功能</label>
          <div className="relative">
            <select
              value={selectedFunction}
              onChange={(e) => setSelectedFunction(e.target.value)}
              className="w-full p-3 bg-input border border-border rounded-lg text-sm appearance-none pr-10 focus:outline-none focus:ring-2 focus:ring-primary focus:border-primary transition-all duration-200"
            >
              <option value="模型训练">模型训练</option>
              <option value="证据包生成">证据包生成</option>
              <option value="AI对话助手">AI对话助手</option>
              <option value="报告整理优化">报告整理优化</option>
            </select>
            <ChevronDown className="absolute right-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground pointer-events-none" />
          </div>
        </div>
      </div>

      <nav className="flex-1 p-3 overflow-y-auto">
        <ul className="space-y-2">
          {menuItems.map((item) => {
            const IconComponent = item.icon
            return (
              <li key={item.id}>
                <button
                  onClick={() => onSectionChange(item.id)}
                  className={cn(
                    "w-full text-left px-4 py-3 text-sm rounded-lg transition-all duration-200 flex items-center gap-3 group",
                    activeSection === item.id
                      ? "bg-primary/20 text-primary border border-primary/30 shadow-sm"
                      : "text-sidebar-foreground hover:bg-sidebar-accent hover:text-sidebar-accent-foreground border border-transparent hover:border-border/30",
                  )}
                >
                  <IconComponent
                    className={cn(
                      "w-4 h-4 transition-colors duration-200",
                      activeSection === item.id
                        ? "text-primary"
                        : "text-muted-foreground group-hover:text-sidebar-accent-foreground",
                    )}
                  />
                  <span className="font-medium">{item.label}</span>
                  {activeSection === item.id && (
                    <div className="ml-auto w-2 h-2 bg-primary rounded-full animate-pulse" />
                  )}
                </button>
              </li>
            )
          })}
        </ul>
      </nav>

      <div className="p-4 border-t border-sidebar-border">
        <div className="flex items-center gap-2 text-xs text-muted-foreground">
          <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
          <span>系统运行正常</span>
        </div>
      </div>
    </div>
  )
}
