'use client'

import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import toast from 'react-hot-toast'
import axios from 'axios'

const patientSchema = z.object({
  name: z.string().min(1, '姓名不能为空'),
  age: z.number().min(0).max(120, '年龄必须在0-120之间'),
  sex: z.enum(['男', '女']),
  chief_complaint: z.string().min(1, '主诉不能为空'),
  history: z.string().optional(),
  labs: z.object({
    ALT: z.number().min(0),
    AST: z.number().min(0),
    ALP: z.number().min(0),
    总胆红素: z.number().min(0),
    直接胆红素: z.number().min(0),
    白蛋白: z.number().min(0),
    AFP: z.number().min(0),
    'CA19-9': z.number().min(0),
    CEA: z.number().min(0),
  }),
  imaging: z.string().optional(),
  additional_notes: z.string().optional(),
  report_type: z.enum(['comprehensive', 'western', 'tcm']),
})

type PatientFormData = z.infer<typeof patientSchema>

export function NewPatientForm() {
  const [isGenerating, setIsGenerating] = useState(false)
  const [generatedReport, setGeneratedReport] = useState<string | null>(null)
  const [patientName, setPatientName] = useState<string>('')

  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
  } = useForm<PatientFormData>({
    resolver: zodResolver(patientSchema),
    defaultValues: {
      age: 50,
      sex: '男',
      labs: {
        ALT: 40,
        AST: 40,
        ALP: 100,
        总胆红素: 20,
        直接胆红素: 5,
        白蛋白: 40,
        AFP: 20,
        'CA19-9': 37,
        CEA: 5,
      },
      report_type: 'comprehensive',
    },
  })

  const onSubmit = async (data: PatientFormData) => {
    setIsGenerating(true)
    setPatientName(data.name)

    try {
      const response = await axios.post('/api/generate_report', {
        patient: data,
        report_type: data.report_type,
      })

      if (response.data.success) {
        setGeneratedReport(response.data.report)
        toast.success('诊疗报告生成成功！')
      } else {
        throw new Error(response.data.error || '生成报告失败')
      }
    } catch (error: any) {
      console.error('生成报告失败:', error)
      toast.error(error.response?.data?.error || '生成报告失败，请稍后重试')
    } finally {
      setIsGenerating(false)
    }
  }

  const downloadReport = () => {
    if (!generatedReport) return
    
    const blob = new Blob([generatedReport], { type: 'text/plain;charset=utf-8' })
    const url = URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `诊疗报告_${patientName}_${new Date().toISOString().slice(0, 19).replace(/:/g, '-')}.txt`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    URL.revokeObjectURL(url)
  }

  const clearReport = () => {
    setGeneratedReport(null)
    setPatientName('')
    reset()
  }

  return (
    <div className="space-y-6">
      <h2 className="section-header">📝 新增病人诊疗报告</h2>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* 表单 */}
        <div className="card">
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
            {/* 基本信息 */}
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-4">基本信息</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    姓名 *
                  </label>
                  <input
                    {...register('name')}
                    className="input-field"
                    placeholder="请输入病人姓名"
                  />
                  {errors.name && (
                    <p className="text-red-500 text-sm mt-1">{errors.name.message}</p>
                  )}
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    年龄 *
                  </label>
                  <input
                    {...register('age', { valueAsNumber: true })}
                    type="number"
                    min="0"
                    max="120"
                    className="input-field"
                  />
                  {errors.age && (
                    <p className="text-red-500 text-sm mt-1">{errors.age.message}</p>
                  )}
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    性别 *
                  </label>
                  <select {...register('sex')} className="input-field">
                    <option value="男">男</option>
                    <option value="女">女</option>
                  </select>
                </div>
              </div>
            </div>

            {/* 临床信息 */}
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-4">临床信息</h3>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    主诉 *
                  </label>
                  <textarea
                    {...register('chief_complaint')}
                    rows={3}
                    className="input-field"
                    placeholder="请详细描述主要症状和持续时间"
                  />
                  {errors.chief_complaint && (
                    <p className="text-red-500 text-sm mt-1">{errors.chief_complaint.message}</p>
                  )}
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    既往病史
                  </label>
                  <textarea
                    {...register('history')}
                    rows={3}
                    className="input-field"
                    placeholder="请描述相关既往病史、手术史、过敏史等"
                  />
                </div>
              </div>
            </div>

            {/* 实验室检查 */}
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-4">实验室检查</h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    ALT (U/L)
                  </label>
                  <input
                    {...register('labs.ALT', { valueAsNumber: true })}
                    type="number"
                    step="0.1"
                    className="input-field"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    AST (U/L)
                  </label>
                  <input
                    {...register('labs.AST', { valueAsNumber: true })}
                    type="number"
                    step="0.1"
                    className="input-field"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    ALP (U/L)
                  </label>
                  <input
                    {...register('labs.ALP', { valueAsNumber: true })}
                    type="number"
                    step="0.1"
                    className="input-field"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    总胆红素 (μmol/L)
                  </label>
                  <input
                    {...register('labs.总胆红素', { valueAsNumber: true })}
                    type="number"
                    step="0.1"
                    className="input-field"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    直接胆红素 (μmol/L)
                  </label>
                  <input
                    {...register('labs.直接胆红素', { valueAsNumber: true })}
                    type="number"
                    step="0.1"
                    className="input-field"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    白蛋白 (g/L)
                  </label>
                  <input
                    {...register('labs.白蛋白', { valueAsNumber: true })}
                    type="number"
                    step="0.1"
                    className="input-field"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    AFP (ng/mL)
                  </label>
                  <input
                    {...register('labs.AFP', { valueAsNumber: true })}
                    type="number"
                    step="0.1"
                    className="input-field"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    CA19-9 (U/mL)
                  </label>
                  <input
                    {...register('labs.CA19-9', { valueAsNumber: true })}
                    type="number"
                    step="0.1"
                    className="input-field"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    CEA (ng/mL)
                  </label>
                  <input
                    {...register('labs.CEA', { valueAsNumber: true })}
                    type="number"
                    step="0.1"
                    className="input-field"
                  />
                </div>
              </div>
            </div>

            {/* 影像学检查 */}
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-4">影像学检查</h3>
              <textarea
                {...register('imaging')}
                rows={3}
                className="input-field"
                placeholder="请描述CT、MRI、超声等检查结果"
              />
            </div>

            {/* 其他备注 */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                其他备注
              </label>
              <textarea
                {...register('additional_notes')}
                rows={2}
                className="input-field"
                placeholder="其他需要说明的信息"
              />
            </div>

            {/* 报告类型 */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                报告类型
              </label>
              <select {...register('report_type')} className="input-field">
                <option value="comprehensive">中西医结合综合报告</option>
                <option value="western">西医诊疗报告</option>
                <option value="tcm">中医辨证报告</option>
              </select>
            </div>

            {/* 提交按钮 */}
            <button
              type="submit"
              disabled={isGenerating}
              className="w-full btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isGenerating ? '🤖 AI正在生成诊疗报告...' : '🚀 生成诊疗报告'}
            </button>
          </form>
        </div>

        {/* 生成的报告 */}
        <div className="card">
          {generatedReport ? (
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <h3 className="text-lg font-semibold text-gray-900">📋 生成的诊疗报告</h3>
                <button
                  onClick={clearReport}
                  className="text-sm text-gray-500 hover:text-gray-700"
                >
                  🗑️ 清除报告
                </button>
              </div>
              
              <div className="bg-gray-50 rounded-lg p-4 max-h-96 overflow-y-auto">
                <pre className="whitespace-pre-wrap text-sm text-gray-800">
                  {generatedReport}
                </pre>
              </div>
              
              <div className="flex space-x-2">
                <button
                  onClick={downloadReport}
                  className="flex-1 btn-primary"
                >
                  📥 下载报告
                </button>
              </div>
            </div>
          ) : (
            <div className="text-center text-gray-500 py-12">
              <div className="text-4xl mb-4">📄</div>
              <p>填写左侧表单并点击"生成诊疗报告"按钮</p>
              <p className="text-sm mt-2">AI将为您生成专业的中西医结合诊疗报告</p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
