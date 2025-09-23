"use client"

import type React from "react"

import { useState } from "react"
import { MessageCircle, Send, User, Bot, AlertTriangle, Phone, Heart } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"

interface ChatMessage {
  id: string
  type: "user" | "assistant"
  content: string
  timestamp: Date
}

export function AiAssistantSection() {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: "1",
      type: "user",
      content: "感受到心慌痛",
      timestamp: new Date(Date.now() - 300000),
    },
  ])

  const [inputMessage, setInputMessage] = useState("")

  const aiResponse = `如果您正在感受到心慌痛（胸部疼痛或压迫感），这可能是心脏供血不足的表现，属于一种需要高度重视的症状。以下是一些重要的建议：

⚠️ 请立即采取以下行动：

1. 停止活动，坐下或躺下休息
   避免继续运动或用力，减少心脏负担。

2. 使用硝酸甘油（如果医生曾处方）
   如果您已被诊断为心绞痛并有医生开具的硝酸甘油或其他药物：
   • 舌下含服一片（或喷一次）
   • 5分钟后若症状未缓解，可再用一次
   • 最多使用3次，间隔5分钟

3. 拨打急救电话（如中国120）
   如果：`

  const handleSendMessage = () => {
    if (!inputMessage.trim()) return

    const newUserMessage: ChatMessage = {
      id: Date.now().toString(),
      type: "user",
      content: inputMessage,
      timestamp: new Date(),
    }

    setMessages((prev) => [...prev, newUserMessage])
    setInputMessage("")

    // Simulate AI response
    setTimeout(() => {
      const aiMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        type: "assistant",
        content:
          "感谢您的咨询。基于您描述的症状，我建议您立即寻求医疗帮助。请详细描述您的症状持续时间、疼痛程度和伴随症状，以便我提供更准确的建议。",
        timestamp: new Date(),
      }
      setMessages((prev) => [...prev, aiMessage])
    }, 1000)
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault()
      handleSendMessage()
    }
  }

  return (
    <div className="p-6 space-y-6 h-full flex flex-col">
      {/* Header */}
      <div className="space-y-4">
        <div className="flex items-center gap-3">
          <div className="flex items-center justify-center w-6 h-6 bg-blue-100 rounded-full">
            <MessageCircle className="h-4 w-4 text-blue-600" />
          </div>
          <h2 className="text-lg font-medium text-foreground">AI对话助手</h2>
        </div>

        <div className="pl-9">
          <p className="text-sm text-muted-foreground">与医疗AI进行实时对话，获取专业的医学建议和解答</p>
        </div>
      </div>

      {/* Chat History Section */}
      <div className="space-y-4">
        <div className="flex items-center gap-3">
          <div className="flex items-center justify-center w-5 h-5 bg-gray-100 rounded-full">
            <MessageCircle className="h-3 w-3 text-gray-600" />
          </div>
          <h3 className="text-base font-medium text-foreground">对话历史</h3>
        </div>

        <div className="pl-8">
          <div className="flex items-center gap-2 text-sm text-muted-foreground">
            <User className="h-4 w-4" />
            <span className="font-medium">您：</span>
            <span>感受到心慌痛</span>
          </div>
        </div>
      </div>

      {/* Main Chat Interface */}
      <div className="flex-1 flex flex-col space-y-4">
        {/* AI Response Card */}
        <Card className="border-l-4 border-l-red-500">
          <CardContent className="p-4">
            <div className="flex items-start gap-3">
              <div className="flex items-center justify-center w-6 h-6 bg-red-100 rounded-full flex-shrink-0 mt-1">
                <Bot className="h-4 w-4 text-red-600" />
              </div>
              <div className="space-y-3 flex-1">
                <div className="font-medium text-sm">AI医生：</div>
                <div className="text-sm leading-relaxed whitespace-pre-line">{aiResponse}</div>

                {/* Emergency Actions */}
                <div className="bg-yellow-50 border border-yellow-200 rounded-md p-3 space-y-2">
                  <div className="flex items-center gap-2 text-yellow-800 font-medium text-sm">
                    <AlertTriangle className="h-4 w-4" />
                    紧急情况处理
                  </div>
                  <div className="text-sm text-yellow-700 space-y-1">
                    <div>• 胸痛持续超过5分钟</div>
                    <div>• 疼痛向左臂、颈部或下颌放射</div>
                    <div>• 伴有出汗、恶心、呼吸困难</div>
                    <div>• 感到极度焦虑或濒死感</div>
                  </div>
                  <div className="flex items-center gap-2 mt-2">
                    <Phone className="h-4 w-4 text-red-600" />
                    <span className="text-sm font-medium text-red-600">立即拨打 120 急救电话</span>
                  </div>
                </div>

                {/* Medication Instructions */}
                <div className="bg-blue-50 border border-blue-200 rounded-md p-3 space-y-2">
                  <div className="flex items-center gap-2 text-blue-800 font-medium text-sm">
                    <Heart className="h-4 w-4" />
                    用药指导
                  </div>
                  <div className="text-sm text-blue-700">如果：</div>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Chat Messages */}
        <div className="flex-1 space-y-3 max-h-96 overflow-y-auto">
          {messages.map((message) => (
            <div key={message.id} className={`flex gap-3 ${message.type === "user" ? "justify-end" : "justify-start"}`}>
              {message.type === "assistant" && (
                <div className="flex items-center justify-center w-6 h-6 bg-blue-100 rounded-full flex-shrink-0">
                  <Bot className="h-4 w-4 text-blue-600" />
                </div>
              )}
              <div
                className={`max-w-md p-3 rounded-lg text-sm ${
                  message.type === "user" ? "bg-primary text-primary-foreground" : "bg-muted text-muted-foreground"
                }`}
              >
                {message.content}
              </div>
              {message.type === "user" && (
                <div className="flex items-center justify-center w-6 h-6 bg-gray-100 rounded-full flex-shrink-0">
                  <User className="h-4 w-4 text-gray-600" />
                </div>
              )}
            </div>
          ))}
        </div>

        {/* Input Area */}
        <div className="border-t pt-4">
          <div className="flex gap-2">
            <input
              type="text"
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="请描述您的症状或问题..."
              className="flex-1 p-3 bg-input border border-border rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-primary/20"
            />
            <Button
              onClick={handleSendMessage}
              disabled={!inputMessage.trim()}
              className="px-4 py-3 bg-primary hover:bg-primary/90 text-primary-foreground rounded-md"
            >
              <Send className="h-4 w-4" />
            </Button>
          </div>
          <div className="text-xs text-muted-foreground mt-2">按 Enter 发送消息，Shift + Enter 换行</div>
        </div>
      </div>
    </div>
  )
}
