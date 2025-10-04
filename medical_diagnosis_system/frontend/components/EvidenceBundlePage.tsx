'use client'

import { useState } from 'react'
import toast from 'react-hot-toast'

export function EvidenceBundlePage() {
  const [analysisType, setAnalysisType] = useState('comprehensive')
  const [patientData, setPatientData] = useState({
    age: 55,
    sex: '男',
    ALT: 56,
    AST: 62,
    AFP: 420,
    tumor_size_cm: 3.5
  })
  const [isGenerating, setIsGenerating] = useState(false)
  const [evidenceBundle, setEvidenceBundle] = useState<any>(null)

  const analysisTypes = [
    { value: 'comprehensive', label: '🔬 综合科研分析' },
    { value: 'sample', label: '📊 示例证据包' },
    { value: 'tcm_integration', label: '🌿 中西医结合分析' },
  ]

  const handleGenerateBundle = async () => {
    setIsGenerating(true)

    try {
      // 模拟证据包生成
      await new Promise(resolve => setTimeout(resolve, 3000))
      
      setEvidenceBundle({
        patient_info: {
          age: patientData.age,
          sex: patientData.sex,
          chief_complaint: '右上腹疼痛3周，伴食欲减退',
          key_labs: {
            ALT: patientData.ALT,
            AST: patientData.AST,
            AFP: patientData.AFP
          },
          imaging: 'CT提示肝右叶占位，大小约3.5cm，边界不清'
        },
        diagnostic_prediction: {
          prediction: '阳性',
          probability: 0.87,
          confidence_level: '高',
          model_performance: {
            auc_score: 0.89,
            model_type: 'XGBoost'
          }
        },
        survival_prediction: {
          median_survival_months: 36.5,
          risk_group: '中高危',
          model_performance: {
            c_index: 0.72,
            model_type: 'Cox回归'
          }
        },
        recurrence_prediction: {
          recurrence_risk: '高风险',
          recurrence_probability_2yr: 0.42
        },
        research_report: `# 科研分析报告

## 一、患者基础信息与AI模型预测摘要
- 基本信息：年龄${patientData.age}岁，${patientData.sex}性
- 主诉：右上腹疼痛3周，伴食欲减退
- 关键指标：AFP ${patientData.AFP} ng/mL
- AI诊断预测：阳性（概率：87%）
- 生存预测：中位生存时间36.5月，风险分层中高危
- 复发风险：高风险，2年复发概率42%

## 二、科学证据分析
### 机器学习模型性能
- 诊断模型AUC: 0.89
- 生存模型C-index: 0.72
- 主要预测因子：AFP、肿瘤大小、年龄

## 三、中西医结合诊疗方案
### 西医诊疗建议
- 诊断：基于AI预测和临床表现，高度怀疑原发性肝癌
- 分期评估：建议完善影像学检查明确分期
- 治疗策略：多学科团队讨论制定个体化治疗方案

### 中医辨证论治
- 证型分析：肝郁脾虚，痰瘀互结
- 治法：疏肝健脾，化痰散结
- 方药建议：逍遥散合六君子汤加减
- 调护：情志调畅，饮食清淡

## 四、临床决策建议
### 立即行动
- 建议完善增强MRI进一步评估
- 建议肝胆外科专科会诊

### 风险管理
- 基于高复发风险预测，建议积极的综合治疗
- 制定个体化随访监测方案
- 考虑术后辅助治疗

**重要声明：**
本报告基于AI模型预测和科学分析，仅供临床参考。最终诊疗决策应由主治医师结合临床经验做出。`
      })
      
      toast.success('科研证据包生成成功！')
    } catch (error) {
      console.error('生成失败:', error)
      toast.error('证据包生成失败，请稍后重试')
    } finally {
      setIsGenerating(false)
    }
  }

  const downloadEvidenceBundle = () => {
    if (!evidenceBundle) return
    
    const blob = new Blob([JSON.stringify(evidenceBundle, null, 2)], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `证据包_${analysisType}_${new Date().toISOString().slice(0, 19).replace(/:/g, '-')}.json`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    URL.revokeObjectURL(url)
  }

  const downloadResearchReport = () => {
    if (!evidenceBundle?.research_report) return
    
    const blob = new Blob([evidenceBundle.research_report], { type: 'text/plain;charset=utf-8' })
    const url = URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `科研报告_${analysisType}_${new Date().toISOString().slice(0, 19).replace(/:/g, '-')}.txt`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    URL.revokeObjectURL(url)
  }

  return (
    <div className="space-y-6">
      <h2 className="section-header">📋 科研证据包生成</h2>
      
      <div className="card">
        <p className="text-gray-600 mb-6">
          💡 基于多个AI模型的预测结果，生成综合性科研证据包和专业报告
        </p>

        <div className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              选择分析类型
            </label>
            <select
              value={analysisType}
              onChange={(e) => setAnalysisType(e.target.value)}
              className="input-field"
            >
              {analysisTypes.map((type) => (
                <option key={type.value} value={type.value}>
                  {type.label}
                </option>
              ))}
            </select>
          </div>

          {analysisType !== 'sample' && (
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-4">患者数据输入</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    年龄
                  </label>
                  <input
                    type="number"
                    min="18"
                    max="100"
                    value={patientData.age}
                    onChange={(e) => setPatientData(prev => ({ ...prev, age: Number(e.target.value) }))}
                    className="input-field"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    性别
                  </label>
                  <select
                    value={patientData.sex}
                    onChange={(e) => setPatientData(prev => ({ ...prev, sex: e.target.value }))}
                    className="input-field"
                  >
                    <option value="男">男</option>
                    <option value="女">女</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    ALT (U/L)
                  </label>
                  <input
                    type="number"
                    step="0.1"
                    value={patientData.ALT}
                    onChange={(e) => setPatientData(prev => ({ ...prev, ALT: Number(e.target.value) }))}
                    className="input-field"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    AST (U/L)
                  </label>
                  <input
                    type="number"
                    step="0.1"
                    value={patientData.AST}
                    onChange={(e) => setPatientData(prev => ({ ...prev, AST: Number(e.target.value) }))}
                    className="input-field"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    AFP (ng/mL)
                  </label>
                  <input
                    type="number"
                    step="0.1"
                    value={patientData.AFP}
                    onChange={(e) => setPatientData(prev => ({ ...prev, AFP: Number(e.target.value) }))}
                    className="input-field"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    肿瘤大小 (cm)
                  </label>
                  <input
                    type="number"
                    step="0.1"
                    value={patientData.tumor_size_cm}
                    onChange={(e) => setPatientData(prev => ({ ...prev, tumor_size_cm: Number(e.target.value) }))}
                    className="input-field"
                  />
                </div>
              </div>
            </div>
          )}

          <button
            onClick={handleGenerateBundle}
            disabled={isGenerating}
            className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isGenerating ? '🔬 正在生成科研证据包...' : '🔬 生成科研证据包'}
          </button>
        </div>
      </div>

      {/* 证据包摘要 */}
      {evidenceBundle && (
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">📊 证据包摘要</h3>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <h4 className="font-semibold text-blue-800 mb-2">诊断预测</h4>
              <div className="text-2xl font-bold text-blue-600">
                {evidenceBundle.diagnostic_prediction.prediction}
              </div>
              <div className="text-sm text-blue-600">
                概率: {(evidenceBundle.diagnostic_prediction.probability * 100).toFixed(1)}%
              </div>
            </div>
            
            <div className="bg-green-50 border border-green-200 rounded-lg p-4">
              <h4 className="font-semibold text-green-800 mb-2">生存预测</h4>
              <div className="text-2xl font-bold text-green-600">
                {evidenceBundle.survival_prediction.median_survival_months}月
              </div>
              <div className="text-sm text-green-600">
                风险分层: {evidenceBundle.survival_prediction.risk_group}
              </div>
            </div>
            
            <div className="bg-purple-50 border border-purple-200 rounded-lg p-4">
              <h4 className="font-semibold text-purple-800 mb-2">复发预测</h4>
              <div className="text-2xl font-bold text-purple-600">
                {(evidenceBundle.recurrence_prediction.recurrence_probability_2yr * 100).toFixed(1)}%
              </div>
              <div className="text-sm text-purple-600">
                2年复发风险
              </div>
            </div>
          </div>

          <div className="flex space-x-2">
            <button
              onClick={downloadEvidenceBundle}
              className="btn-primary"
            >
              📥 下载证据包(JSON)
            </button>
            <button
              onClick={downloadResearchReport}
              className="btn-secondary"
            >
              📥 下载科研报告
            </button>
          </div>
        </div>
      )}

      {/* 完整科研报告 */}
      {evidenceBundle?.research_report && (
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">📄 科研分析报告</h3>
          <div className="bg-gray-50 rounded-lg p-4 max-h-96 overflow-y-auto">
            <pre className="whitespace-pre-wrap text-sm text-gray-800">
              {evidenceBundle.research_report}
            </pre>
          </div>
        </div>
      )}
    </div>
  )
}
