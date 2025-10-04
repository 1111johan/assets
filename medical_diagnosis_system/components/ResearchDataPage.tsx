'use client'

import { useState } from 'react'
import toast from 'react-hot-toast'

export function ResearchDataPage() {
  const [nPatients, setNPatients] = useState(500)
  const [isCreating, setIsCreating] = useState(false)
  const [createdData, setCreatedData] = useState<any>(null)

  const handleCreateData = async () => {
    setIsCreating(true)

    try {
      // 模拟数据创建
      await new Promise(resolve => setTimeout(resolve, 2000))
      
      setCreatedData({
        file_path: `research_data/sample_medical_data_${nPatients}_${new Date().toISOString().slice(0, 19).replace(/:/g, '-')}.csv`,
        n_patients: nPatients,
        columns: ['age', 'sex', 'ALT', 'AST', 'AFP', 'tumor_size', 'diagnosis_target'],
        shape: [nPatients, 7]
      })
      
      toast.success('示例数据创建成功！')
    } catch (error) {
      console.error('创建失败:', error)
      toast.error('创建失败，请稍后重试')
    } finally {
      setIsCreating(false)
    }
  }

  return (
    <div className="space-y-6">
      <h2 className="section-header">🔬 科研数据分析</h2>
      
      <div className="card">
        <p className="text-gray-600 mb-6">
          💡 进行探索性数据分析、特征工程和数据质量评估
        </p>

        <div className="space-y-6">
          <div>
            <h3 className="text-lg font-semibold text-gray-900 mb-4">数据准备</h3>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  患者数量
                </label>
                <input
                  type="number"
                  min="100"
                  max="2000"
                  value={nPatients}
                  onChange={(e) => setNPatients(Number(e.target.value))}
                  className="input-field"
                />
              </div>
              
              <div className="flex items-end">
                <button
                  onClick={handleCreateData}
                  disabled={isCreating}
                  className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {isCreating ? '🔬 正在创建示例数据...' : '🔬 创建示例数据'}
                </button>
              </div>
            </div>
          </div>

          {createdData && (
            <div className="bg-green-50 border border-green-200 rounded-lg p-4">
              <h4 className="text-lg font-semibold text-green-800 mb-2">✅ 数据创建成功</h4>
              <div className="space-y-2 text-sm text-green-700">
                <p><strong>文件路径:</strong> {createdData.file_path}</p>
                <p><strong>数据形状:</strong> {createdData.shape[0]} 行 × {createdData.shape[1]} 列</p>
                <p><strong>变量数:</strong> {createdData.columns.length}</p>
                <p><strong>变量列表:</strong> {createdData.columns.join(', ')}</p>
              </div>
            </div>
          )}
        </div>
      </div>

      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">数据分析功能</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <h4 className="font-semibold text-blue-800 mb-2">📊 探索性数据分析</h4>
            <p className="text-sm text-blue-600">数据分布、相关性分析、异常值检测</p>
          </div>
          
          <div className="bg-green-50 border border-green-200 rounded-lg p-4">
            <h4 className="font-semibold text-green-800 mb-2">🔧 特征工程</h4>
            <p className="text-sm text-green-600">特征选择、特征变换、特征组合</p>
          </div>
          
          <div className="bg-purple-50 border border-purple-200 rounded-lg p-4">
            <h4 className="font-semibold text-purple-800 mb-2">📈 数据质量评估</h4>
            <p className="text-sm text-purple-600">缺失值分析、数据完整性检查</p>
          </div>
        </div>
      </div>
    </div>
  )
}
