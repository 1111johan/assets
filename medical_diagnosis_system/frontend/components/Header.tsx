'use client'

import { Menu, X } from 'lucide-react'

interface HeaderProps {
  onMenuClick: () => void
}

export function Header({ onMenuClick }: HeaderProps) {
  return (
    <header className="bg-white shadow-sm border-b border-gray-200">
      <div className="px-6 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <button
              onClick={onMenuClick}
              className="p-2 rounded-lg hover:bg-gray-100 lg:hidden"
            >
              <Menu className="h-6 w-6" />
            </button>
            <div className="flex items-center space-x-3">
              <div className="text-2xl">🏥</div>
              <div>
                <h1 className="text-xl font-bold text-gray-900">
                  医疗AI科研系统
                </h1>
                <p className="text-sm text-gray-500">
                  术前病情预测 & 中西医结合诊疗报告生成
                </p>
              </div>
            </div>
          </div>
          
          <div className="hidden md:flex items-center space-x-4">
            <div className="text-sm text-gray-500">
              系统版本 v2.0.0
            </div>
            <div className="w-2 h-2 bg-green-500 rounded-full"></div>
            <span className="text-sm text-gray-500">运行中</span>
          </div>
        </div>
      </div>
    </header>
  )
}
