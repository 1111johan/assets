'use client'

import { useState } from 'react'
import toast from 'react-hot-toast'

export function ModelTrainingPage() {
  const [modelCategory, setModelCategory] = useState('diagnostic')
  const [isTraining, setIsTraining] = useState(false)
  const [trainingResults, setTrainingResults] = useState<any>(null)

  const handleTrainModel = async () => {
    setIsTraining(true)

    try {
      // 模拟模型训练
      await new Promise(resolve => setTimeout(resolve, 3000))
      
      setTrainingResults({
        model_type: 'XGBoost',
        auc_score: 0.89,
        target_column: 'diagnosis_target',
        feature_importance: [
          { feature: 'AFP', importance: 0.35 },
          { feature: 'tumor_size', importance: 0.22 },
          { feature: 'age', importance: 0.18 },
          { feature: 'ALT', importance: 0.15 },
          { feature: 'AST', importance: 0.10 }
        ]
      })
      
      toast.success('模型训练成功！')
    } catch (error) {
      console.error('训练失败:', error)
      toast.error('模型训练失败，请稍后重试')
    } finally {
      setIsTraining(false)
    }
  }

  return (
    <div className="space-y-6">
      <h2 className="section-header">🤖 模型训练</h2>
      
      <div className="card">
        <p className="text-gray-600 mb-6">
          💡 训练诊断、生存分析、复发预测等机器学习模型
        </p>

        <div className="space-y-6">
          <div>
            <h3 className="text-lg font-semibold text-gray-900 mb-4">模型配置</h3>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  选择模型类别
                </label>
                <select
                  value={modelCategory}
                  onChange={(e) => setModelCategory(e.target.value)}
                  className="input-field"
                >
                  <option value="diagnostic">诊断分类模型</option>
                  <option value="survival">生存分析模型</option>
                  <option value="recurrence">复发预测模型</option>
                </select>
              </div>
              
              <div className="flex items-end">
                <button
                  onClick={handleTrainModel}
                  disabled={isTraining}
                  className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {isTraining ? '🚀 正在训练模型...' : '🚀 开始训练模型'}
                </button>
              </div>
            </div>
          </div>

          {modelCategory === 'diagnostic' && (
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <h4 className="text-lg font-semibold text-blue-800 mb-2">🎯 诊断分类模型训练</h4>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    数据文件路径
                  </label>
                  <input
                    type="text"
                    defaultValue="research_data/sample_medical_data.csv"
                    className="input-field"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    目标变量列名
                  </label>
                  <input
                    type="text"
                    defaultValue="diagnosis_target"
                    className="input-field"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    模型算法
                  </label>
                  <select className="input-field">
                    <option value="xgboost">XGBoost</option>
                    <option value="lightgbm">LightGBM</option>
                    <option value="random_forest">Random Forest</option>
                    <option value="logistic">Logistic Regression</option>
                  </select>
                </div>
              </div>
            </div>
          )}

          {trainingResults && (
            <div className="bg-green-50 border border-green-200 rounded-lg p-4">
              <h4 className="text-lg font-semibold text-green-800 mb-4">✅ 模型训练成功</h4>
              
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
                <div className="bg-white rounded-lg p-3">
                  <div className="text-2xl font-bold text-green-600">
                    {trainingResults.auc_score}
                  </div>
                  <div className="text-sm text-gray-600">AUC得分</div>
                </div>
                <div className="bg-white rounded-lg p-3">
                  <div className="text-lg font-semibold text-green-600">
                    {trainingResults.model_type}
                  </div>
                  <div className="text-sm text-gray-600">模型类型</div>
                </div>
                <div className="bg-white rounded-lg p-3">
                  <div className="text-lg font-semibold text-green-600">
                    {trainingResults.target_column}
                  </div>
                  <div className="text-sm text-gray-600">目标变量</div>
                </div>
              </div>

              <div>
                <h5 className="font-semibold text-gray-800 mb-2">特征重要性 Top 5</h5>
                <div className="space-y-1">
                  {trainingResults.feature_importance.map((item: any, index: number) => (
                    <div key={index} className="flex items-center justify-between bg-white rounded px-3 py-2">
                      <span className="text-sm font-medium">{item.feature}</span>
                      <span className="text-sm text-gray-600">{item.importance.toFixed(3)}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}
        </div>
      </div>

      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">模型类型说明</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <h4 className="font-semibold text-blue-800 mb-2">🎯 诊断分类模型</h4>
            <p className="text-sm text-blue-600">用于疾病诊断和分类预测</p>
          </div>
          
          <div className="bg-green-50 border border-green-200 rounded-lg p-4">
            <h4 className="font-semibold text-green-800 mb-2">📈 生存分析模型</h4>
            <p className="text-sm text-green-600">预测患者生存时间和风险分层</p>
          </div>
          
          <div className="bg-purple-50 border border-purple-200 rounded-lg p-4">
            <h4 className="font-semibold text-purple-800 mb-2">🔄 复发预测模型</h4>
            <p className="text-sm text-purple-600">预测疾病复发概率和风险因素</p>
          </div>
        </div>
      </div>
    </div>
  )
}
