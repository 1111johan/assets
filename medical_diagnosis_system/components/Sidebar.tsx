'use client'

import { X, FileText, History, MessageCircle, FileEdit, Search, BarChart3, Cpu, Package, Settings } from 'lucide-react'
import { clsx } from 'clsx'

type PageType = 
  | 'new-patient' 
  | 'history' 
  | 'ai-chat' 
  | 'report-optimize' 
  | 'symptom-analysis' 
  | 'research-data' 
  | 'model-training' 
  | 'evidence-bundle' 
  | 'settings'

interface SidebarProps {
  currentPage: PageType
  onPageChange: (page: PageType) => void
  isOpen: boolean
  onClose: () => void
}

const menuItems = [
  { id: 'new-patient' as PageType, label: '新增病人报告', icon: FileText },
  { id: 'history' as PageType, label: '查看历史记录', icon: History },
  { id: 'ai-chat' as PageType, label: 'AI对话助手', icon: MessageCircle },
  { id: 'report-optimize' as PageType, label: '报告整理优化', icon: FileEdit },
  { id: 'symptom-analysis' as PageType, label: '症状分析', icon: Search },
  { id: 'research-data' as PageType, label: '科研数据分析', icon: BarChart3 },
  { id: 'model-training' as PageType, label: '模型训练', icon: Cpu },
  { id: 'evidence-bundle' as PageType, label: '证据包生成', icon: Package },
  { id: 'settings' as PageType, label: '系统设置', icon: Settings },
]

export function Sidebar({ currentPage, onPageChange, isOpen, onClose }: SidebarProps) {
  return (
    <>
      {/* Mobile overlay */}
      {isOpen && (
        <div 
          className="fixed inset-0 bg-black bg-opacity-50 z-40 lg:hidden"
          onClick={onClose}
        />
      )}
      
      {/* Sidebar */}
      <aside className={clsx(
        'fixed top-0 left-0 z-50 h-full w-64 bg-white shadow-lg transform transition-transform duration-300 ease-in-out lg:translate-x-0 lg:static lg:inset-0',
        isOpen ? 'translate-x-0' : '-translate-x-full'
      )}>
        <div className="flex items-center justify-between p-4 border-b border-gray-200">
          <h2 className="text-lg font-semibold text-gray-900">导航菜单</h2>
          <button
            onClick={onClose}
            className="p-2 rounded-lg hover:bg-gray-100 lg:hidden"
          >
            <X className="h-5 w-5" />
          </button>
        </div>
        
        <nav className="p-4 space-y-2">
          {menuItems.map((item) => {
            const Icon = item.icon
            return (
              <button
                key={item.id}
                onClick={() => {
                  onPageChange(item.id)
                  onClose()
                }}
                className={clsx(
                  'w-full flex items-center space-x-3 px-3 py-2 rounded-lg text-left transition-colors duration-200',
                  currentPage === item.id
                    ? 'bg-blue-100 text-blue-700 border-r-2 border-blue-500'
                    : 'text-gray-700 hover:bg-gray-100'
                )}
              >
                <Icon className="h-5 w-5" />
                <span className="font-medium">{item.label}</span>
              </button>
            )
          })}
        </nav>
        
        <div className="absolute bottom-4 left-4 right-4">
          <div className="bg-gray-50 rounded-lg p-3">
            <div className="text-xs text-gray-500 mb-1">系统状态</div>
            <div className="flex items-center space-x-2">
              <div className="w-2 h-2 bg-green-500 rounded-full"></div>
              <span className="text-sm text-gray-700">运行正常</span>
            </div>
          </div>
        </div>
      </aside>
    </>
  )
}
