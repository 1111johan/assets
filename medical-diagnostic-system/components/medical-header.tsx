"use client"

import { Plus, ChevronLeft, ChevronRight, Search, Bell, Settings, User, Sun, Moon } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"

interface MedicalHeaderProps {
  onToggleSidebar?: () => void
  sidebarCollapsed?: boolean
  isDarkMode?: boolean
  onThemeToggle?: () => void
}

export function MedicalHeader({ onToggleSidebar, sidebarCollapsed, isDarkMode, onThemeToggle }: MedicalHeaderProps) {
  return (
    <div className="border-b border-border bg-card shadow-sm">
      <div className="flex items-center justify-between p-4 lg:p-6">
        <div className="flex items-center gap-4">
          <div className="flex items-center justify-center w-10 h-10 lg:w-12 lg:h-12 bg-gradient-to-br from-primary to-primary/80 rounded-xl shadow-lg">
            <Plus className="h-5 w-5 lg:h-6 lg:w-6 text-primary-foreground" />
          </div>
          <div className="min-w-0">
            <h1 className="text-lg lg:text-xl font-bold text-foreground text-balance gradient-text">
              术前病情预测 & 中西医结合诊疗报告生成系统
            </h1>
            <p className="text-xs lg:text-sm text-muted-foreground mt-1 font-medium hidden sm:block">
              AI-Powered Medical Diagnostic & Report Generation System
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2 lg:gap-4">
          <div className="hidden md:flex items-center gap-3">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
              <Input
                placeholder="搜索患者、报告..."
                className="pl-10 w-48 lg:w-64 bg-input border-border focus:border-primary transition-all duration-200"
              />
            </div>

            <Button variant="ghost" size="sm" onClick={onThemeToggle} className="hover:bg-accent">
              {isDarkMode ? <Sun className="h-4 w-4" /> : <Moon className="h-4 w-4" />}
            </Button>

            <Button variant="ghost" size="sm" className="relative hover:bg-accent">
              <Bell className="h-4 w-4" />
              <div className="absolute -top-1 -right-1 w-2 h-2 bg-red-500 rounded-full animate-pulse"></div>
            </Button>

            <Button variant="ghost" size="sm" className="hover:bg-accent">
              <Settings className="h-4 w-4" />
            </Button>

            <Button variant="ghost" size="sm" className="gap-2 hover:bg-accent">
              <User className="h-4 w-4" />
              <span className="hidden lg:inline text-sm">医生账户</span>
            </Button>
          </div>

          <Button variant="ghost" size="sm" onClick={onThemeToggle} className="md:hidden hover:bg-accent">
            {isDarkMode ? <Sun className="h-4 w-4" /> : <Moon className="h-4 w-4" />}
          </Button>

          <Button variant="ghost" size="sm" onClick={onToggleSidebar} className="lg:hidden hover:bg-accent">
            {sidebarCollapsed ? <ChevronRight className="h-4 w-4" /> : <ChevronLeft className="h-4 w-4" />}
          </Button>

          <div className="hidden xl:flex items-center gap-4 text-xs">
            <div className="flex items-center gap-2 px-3 py-1.5 bg-green-500/20 border border-green-500/30 rounded-full">
              <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
              <span className="text-green-600 dark:text-green-400 font-medium">系统正常</span>
            </div>
            <div className="flex items-center gap-2 text-muted-foreground">
              <span>在线用户: 24</span>
              <span>•</span>
              <span>活跃模型: 3</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
