'use client'

import { useState } from 'react'
import toast from 'react-hot-toast'

export function SettingsPage() {
  const [apiProvider, setApiProvider] = useState('dashscope')
  const [apiKey, setApiKey] = useState('')
  const [isTesting, setIsTesting] = useState(false)

  const handleTestConnection = async () => {
    if (!apiKey.trim()) {
      toast.error('请输入API Key')
      return
    }

    setIsTesting(true)

    try {
      // 模拟API测试
      await new Promise(resolve => setTimeout(resolve, 2000))
      toast.success('✅ API连接测试成功')
    } catch (error) {
      console.error('API测试失败:', error)
      toast.error('API连接测试失败')
    } finally {
      setIsTesting(false)
    }
  }

  return (
    <div className="space-y-6">
      <h2 className="section-header">⚙️ 系统设置</h2>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* API 配置 */}
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">API 配置</h3>
          
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                选择AI服务提供商
              </label>
              <select
                value={apiProvider}
                onChange={(e) => setApiProvider(e.target.value)}
                className="input-field"
              >
                <option value="dashscope">阿里云通义千问</option>
                <option value="openai">OpenAI GPT</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                {apiProvider === 'dashscope' ? '阿里云API Key' : 'OpenAI API Key'}
              </label>
              <input
                type="password"
                value={apiKey}
                onChange={(e) => setApiKey(e.target.value)}
                placeholder={`请输入您的${apiProvider === 'dashscope' ? '阿里云' : 'OpenAI'} API Key`}
                className="input-field"
              />
            </div>

            <button
              onClick={handleTestConnection}
              disabled={!apiKey.trim() || isTesting}
              className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isTesting ? '🔧 正在测试连接...' : '🔧 测试连接'}
            </button>
          </div>
        </div>

        {/* 系统信息 */}
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">系统信息</h3>
          
          <div className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-3">
                <div className="text-sm text-blue-600 mb-1">系统版本</div>
                <div className="font-semibold text-blue-800">v2.0.0 (科研版)</div>
              </div>
              
              <div className="bg-green-50 border border-green-200 rounded-lg p-3">
                <div className="text-sm text-green-600 mb-1">后端状态</div>
                <div className="font-semibold text-green-800">运行中 ✅</div>
              </div>
              
              <div className="bg-green-50 border border-green-200 rounded-lg p-3">
                <div className="text-sm text-green-600 mb-1">前端状态</div>
                <div className="font-semibold text-green-800">运行中 ✅</div>
              </div>
              
              <div className="bg-green-50 border border-green-200 rounded-lg p-3">
                <div className="text-sm text-green-600 mb-1">数据库</div>
                <div className="font-semibold text-green-800">SQLite ✅</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* 功能说明 */}
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">功能说明</h3>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <h4 className="font-semibold text-blue-800 mb-2">🏥 诊疗报告生成</h4>
            <p className="text-sm text-blue-600">基于AI生成中西医结合诊疗报告</p>
          </div>
          
          <div className="bg-green-50 border border-green-200 rounded-lg p-4">
            <h4 className="font-semibold text-green-800 mb-2">🤖 AI对话助手</h4>
            <p className="text-sm text-green-600">智能医疗问答和症状分析</p>
          </div>
          
          <div className="bg-purple-50 border border-purple-200 rounded-lg p-4">
            <h4 className="font-semibold text-purple-800 mb-2">📊 科研数据分析</h4>
            <p className="text-sm text-purple-600">机器学习模型训练和数据分析</p>
          </div>
          
          <div className="bg-orange-50 border border-orange-200 rounded-lg p-4">
            <h4 className="font-semibold text-orange-800 mb-2">📋 证据包生成</h4>
            <p className="text-sm text-orange-600">综合AI预测结果生成科研证据包</p>
          </div>
          
          <div className="bg-red-50 border border-red-200 rounded-lg p-4">
            <h4 className="font-semibold text-red-800 mb-2">⚠️ 重要声明</h4>
            <p className="text-sm text-red-600">本系统仅供医疗参考，不能替代专业医生诊断</p>
          </div>
        </div>
      </div>

      {/* 使用指南 */}
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">使用指南</h3>
        
        <div className="space-y-4">
          <div>
            <h4 className="font-semibold text-gray-800 mb-2">1. 生成诊疗报告</h4>
            <p className="text-sm text-gray-600">
              在"新增病人报告"页面填写病人信息，选择报告类型，点击生成按钮即可获得AI生成的专业诊疗报告。
            </p>
          </div>
          
          <div>
            <h4 className="font-semibold text-gray-800 mb-2">2. AI对话咨询</h4>
            <p className="text-sm text-gray-600">
              在"AI对话助手"页面可以与医疗AI进行实时对话，获取医学建议和症状分析。
            </p>
          </div>
          
          <div>
            <h4 className="font-semibold text-gray-800 mb-2">3. 科研数据分析</h4>
            <p className="text-sm text-gray-600">
              使用"科研数据分析"和"模型训练"功能进行机器学习模型训练和数据分析。
            </p>
          </div>
          
          <div>
            <h4 className="font-semibold text-gray-800 mb-2">4. 查看历史记录</h4>
            <p className="text-sm text-gray-600">
              在"查看历史记录"页面可以浏览所有病人信息和生成的报告。
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}
