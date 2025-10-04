'use client'

import { useState } from 'react'
import { Send, Trash2 } from 'lucide-react'
import toast from 'react-hot-toast'
import axios from 'axios'

interface Message {
  role: 'user' | 'assistant'
  content: string
}

export function AIChatPage() {
  const [messages, setMessages] = useState<Message[]>([])
  const [inputMessage, setInputMessage] = useState('')
  const [isLoading, setIsLoading] = useState(false)

  const sendMessage = async () => {
    if (!inputMessage.trim() || isLoading) return

    const userMessage: Message = {
      role: 'user',
      content: inputMessage.trim()
    }

    setMessages(prev => [...prev, userMessage])
    setInputMessage('')
    setIsLoading(true)

    try {
      const response = await axios.post('/api/chat', {
        message: userMessage.content,
        conversation_history: messages
      })

      if (response.data.success) {
        const assistantMessage: Message = {
          role: 'assistant',
          content: response.data.response
        }
        setMessages(prev => [...prev, assistantMessage])
      } else {
        throw new Error(response.data.error || 'AI对话失败')
      }
    } catch (error: any) {
      console.error('AI对话失败:', error)
      toast.error(error.response?.data?.error || 'AI对话失败，请稍后重试')
    } finally {
      setIsLoading(false)
    }
  }

  const clearChat = () => {
    setMessages([])
    toast.success('对话已清空')
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  return (
    <div className="space-y-6">
      <h2 className="section-header">🤖 AI对话助手</h2>
      
      <div className="card">
        <div className="flex items-center justify-between mb-4">
          <p className="text-gray-600">
            💡 与医疗AI进行实时对话，获取专业的医学建议和解答
          </p>
          {messages.length > 0 && (
            <button
              onClick={clearChat}
              className="flex items-center space-x-1 text-sm text-gray-500 hover:text-gray-700"
            >
              <Trash2 className="h-4 w-4" />
              <span>清空对话</span>
            </button>
          )}
        </div>

        {/* 对话区域 */}
        <div className="bg-gray-50 rounded-lg p-4 h-96 overflow-y-auto mb-4">
          {messages.length === 0 ? (
            <div className="text-center text-gray-500 py-12">
              <div className="text-4xl mb-4">💬</div>
              <p>开始与AI医生对话吧！</p>
              <p className="text-sm mt-2">例如：我最近感觉右上腹疼痛，这可能是什么原因？</p>
            </div>
          ) : (
            <div className="space-y-4">
              {messages.map((message, index) => (
                <div
                  key={index}
                  className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div
                    className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
                      message.role === 'user'
                        ? 'bg-blue-600 text-white'
                        : 'bg-white text-gray-800 border border-gray-200'
                    }`}
                  >
                    <div className="text-sm font-medium mb-1">
                      {message.role === 'user' ? '👤 您' : '🤖 AI医生'}
                    </div>
                    <div className="whitespace-pre-wrap">{message.content}</div>
                  </div>
                </div>
              ))}
              {isLoading && (
                <div className="flex justify-start">
                  <div className="bg-white text-gray-800 border border-gray-200 px-4 py-2 rounded-lg">
                    <div className="text-sm font-medium mb-1">🤖 AI医生</div>
                    <div className="flex items-center space-x-1">
                      <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600"></div>
                      <span className="text-sm">正在思考中...</span>
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}
        </div>

        {/* 输入区域 */}
        <div className="flex space-x-2">
          <textarea
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="请输入您的问题..."
            className="flex-1 input-field resize-none"
            rows={3}
            disabled={isLoading}
          />
          <button
            onClick={sendMessage}
            disabled={!inputMessage.trim() || isLoading}
            className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-1"
          >
            <Send className="h-4 w-4" />
            <span>发送</span>
          </button>
        </div>
      </div>
    </div>
  )
}
