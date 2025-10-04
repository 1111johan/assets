'use client'

import { useState } from 'react'
import toast from 'react-hot-toast'
import axios from 'axios'

export function ReportOptimizePage() {
  const [originalReport, setOriginalReport] = useState('')
  const [optimizedReport, setOptimizedReport] = useState('')
  const [optimizeType, setOptimizeType] = useState('format')
  const [isOptimizing, setIsOptimizing] = useState(false)

  const optimizeTypes = [
    { value: 'format', label: '📝 格式优化 - 改善报告格式和结构' },
    { value: 'simplify', label: '🎯 简化表达 - 使用更通俗易懂的语言' },
    { value: 'enhance', label: '✨ 内容增强 - 补充相关医学信息' },
    { value: 'summary', label: '📋 生成摘要 - 提取关键信息' },
  ]

  const handleOptimize = async () => {
    if (!originalReport.trim()) {
      toast.error('请输入需要优化的报告内容')
      return
    }

    setIsOptimizing(true)

    try {
      const response = await axios.post('/api/optimize_report', {
        original_report: originalReport,
        optimize_type: optimizeType,
      })

      if (response.data.success) {
        setOptimizedReport(response.data.optimized_report)
        toast.success('报告优化完成！')
      } else {
        throw new Error(response.data.error || '报告优化失败')
      }
    } catch (error: any) {
      console.error('报告优化失败:', error)
      toast.error(error.response?.data?.error || '报告优化失败，请稍后重试')
    } finally {
      setIsOptimizing(false)
    }
  }

  const downloadOptimizedReport = () => {
    if (!optimizedReport) return
    
    const blob = new Blob([optimizedReport], { type: 'text/plain;charset=utf-8' })
    const url = URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `优化报告_${new Date().toISOString().slice(0, 19).replace(/:/g, '-')}.txt`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    URL.revokeObjectURL(url)
  }

  const clearReports = () => {
    setOriginalReport('')
    setOptimizedReport('')
  }

  return (
    <div className="space-y-6">
      <h2 className="section-header">📊 报告整理优化</h2>
      
      <div className="card">
        <p className="text-gray-600 mb-6">
          💡 使用AI帮助您优化和整理医疗报告
        </p>

        <div className="space-y-6">
          {/* 优化类型选择 */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              选择优化类型
            </label>
            <select
              value={optimizeType}
              onChange={(e) => setOptimizeType(e.target.value)}
              className="input-field"
            >
              {optimizeTypes.map((type) => (
                <option key={type.value} value={type.value}>
                  {type.label}
                </option>
              ))}
            </select>
          </div>

          {/* 报告输入 */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              请粘贴需要优化的医疗报告：
            </label>
            <textarea
              value={originalReport}
              onChange={(e) => setOriginalReport(e.target.value)}
              placeholder="在此输入您想要优化的医疗报告内容..."
              className="input-field"
              rows={8}
            />
          </div>

          <button
            onClick={handleOptimize}
            disabled={!originalReport.trim() || isOptimizing}
            className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isOptimizing ? '🤖 AI正在优化报告...' : '🚀 开始优化'}
          </button>
        </div>
      </div>

      {/* 优化结果 */}
      {optimizedReport && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="card">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">📄 原始报告</h3>
            <div className="bg-gray-50 rounded-lg p-4 max-h-96 overflow-y-auto">
              <pre className="whitespace-pre-wrap text-sm text-gray-800">
                {originalReport}
              </pre>
            </div>
          </div>

          <div className="card">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-gray-900">✨ 优化后报告</h3>
              <button
                onClick={downloadOptimizedReport}
                className="btn-primary text-sm"
              >
                📥 下载
              </button>
            </div>
            <div className="bg-gray-50 rounded-lg p-4 max-h-96 overflow-y-auto">
              <pre className="whitespace-pre-wrap text-sm text-gray-800">
                {optimizedReport}
              </pre>
            </div>
          </div>
        </div>
      )}

      {/* 清空按钮 */}
      {(originalReport || optimizedReport) && (
        <div className="text-center">
          <button
            onClick={clearReports}
            className="btn-secondary"
          >
            🗑️ 清空所有内容
          </button>
        </div>
      )}
    </div>
  )
}
