'use client'

import { useState } from 'react'
import { useForm } from 'react-hook-form'
import toast from 'react-hot-toast'
import axios from 'axios'

interface SymptomData {
  main_symptom: string
  duration: string
  severity: string
  location: string
  triggers: string
  other_symptoms: string
  additional_info: string
}

export function SymptomAnalysisPage() {
  const [analysis, setAnalysis] = useState('')
  const [isAnalyzing, setIsAnalyzing] = useState(false)

  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
  } = useForm<SymptomData>({
    defaultValues: {
      severity: '中等',
    },
  })

  const onSubmit = async (data: SymptomData) => {
    setIsAnalyzing(true)

    try {
      // 过滤空值
      const symptoms = Object.fromEntries(
        Object.entries(data).filter(([_, value]) => value.trim())
      )

      const response = await axios.post('/api/analyze_symptoms', symptoms)

      if (response.data.success) {
        setAnalysis(response.data.analysis)
        toast.success('症状分析完成！')
      } else {
        throw new Error(response.data.error || '症状分析失败')
      }
    } catch (error: any) {
      console.error('症状分析失败:', error)
      toast.error(error.response?.data?.error || '症状分析失败，请稍后重试')
    } finally {
      setIsAnalyzing(false)
    }
  }

  const downloadAnalysis = () => {
    if (!analysis) return
    
    const blob = new Blob([analysis], { type: 'text/plain;charset=utf-8' })
    const url = URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `症状分析_${new Date().toISOString().slice(0, 19).replace(/:/g, '-')}.txt`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    URL.revokeObjectURL(url)
  }

  const clearAnalysis = () => {
    setAnalysis('')
    reset()
  }

  return (
    <div className="space-y-6">
      <h2 className="section-header">🔍 症状分析</h2>
      
      <div className="card">
        <p className="text-gray-600 mb-6">
          💡 输入症状描述，获取AI初步分析和医学建议
        </p>

        <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  主要症状 *
                </label>
                <textarea
                  {...register('main_symptom', { required: '主要症状不能为空' })}
                  placeholder="请详细描述您的主要症状"
                  className="input-field"
                  rows={3}
                />
                {errors.main_symptom && (
                  <p className="text-red-500 text-sm mt-1">{errors.main_symptom.message}</p>
                )}
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  持续时间
                </label>
                <input
                  {...register('duration')}
                  placeholder="例如：3天、1周"
                  className="input-field"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  严重程度
                </label>
                <select {...register('severity')} className="input-field">
                  <option value="轻微">轻微</option>
                  <option value="中等">中等</option>
                  <option value="严重">严重</option>
                  <option value="非常严重">非常严重</option>
                </select>
              </div>
            </div>

            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  症状部位
                </label>
                <input
                  {...register('location')}
                  placeholder="例如：右上腹、胸部、头部"
                  className="input-field"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  诱发因素
                </label>
                <textarea
                  {...register('triggers')}
                  placeholder="什么情况下症状会加重？"
                  className="input-field"
                  rows={2}
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  伴随症状
                </label>
                <textarea
                  {...register('other_symptoms')}
                  placeholder="还有其他症状吗？"
                  className="input-field"
                  rows={2}
                />
              </div>
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              其他信息
            </label>
            <textarea
              {...register('additional_info')}
              placeholder="年龄、性别、既往病史等"
              className="input-field"
              rows={2}
            />
          </div>

          <button
            type="submit"
            disabled={isAnalyzing}
            className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isAnalyzing ? '🤖 AI正在分析症状...' : '🔍 开始分析'}
          </button>
        </form>
      </div>

      {/* 分析结果 */}
      {analysis && (
        <div className="card">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-900">📋 分析结果</h3>
            <button
              onClick={downloadAnalysis}
              className="btn-primary text-sm"
            >
              📥 下载分析结果
            </button>
          </div>
          
          <div className="bg-gray-50 rounded-lg p-4 max-h-96 overflow-y-auto">
            <pre className="whitespace-pre-wrap text-sm text-gray-800">
              {analysis}
            </pre>
          </div>
        </div>
      )}

      {/* 清空按钮 */}
      {analysis && (
        <div className="text-center">
          <button
            onClick={clearAnalysis}
            className="btn-secondary"
          >
            🗑️ 清空分析结果
          </button>
        </div>
      )}
    </div>
  )
}
