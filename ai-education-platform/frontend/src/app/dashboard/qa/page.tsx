'use client'

import { useState } from 'react'
import { Send, User, Bot, ThumbsUp, ThumbsDown } from 'lucide-react'

interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string
  sources?: { title: string; content: string }[]
}

const modeOptions = [
  { id: 'student', label: '👨‍🎓 學生模式', desc: '用簡單易懂的語言解答' },
  { id: 'teacher', label: '👨‍🏫 教師模式', desc: '提供專業的教學建議' },
  { id: 'parent', label: '👨‍👩‍👧 家長模式', desc: '幫助了解子女學習情況' },
]

export default function QAPage() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      role: 'assistant',
      content: '你好！我是 AI 助教。選擇一種模式後，輸入你的問題，我會根據校本知識庫為你解答。',
    }
  ])
  const [input, setInput] = useState('')
  const [mode, setMode] = useState('student')
  const [loading, setLoading] = useState(false)

  const handleSend = async () => {
    if (!input.trim()) return

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: input,
    }

    setMessages([...messages, userMessage])
    setInput('')
    setLoading(true)

    try {
      const res = await fetch('http://localhost:8000/api/v1/qa/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          question: input,
          mode: mode,
          user_id: 'demo'
        })
      })

      const data = await res.json()
      
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: data.answer || '這是一個示範回答。連接 API 後會顯示真實答案。',
        sources: data.sources || []
      }

      setMessages(prev => [...prev, assistantMessage])
    } catch (error) {
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: '抱歉，發生了錯誤。請稍後再試。'
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="h-[calc(100vh-180px)] flex flex-col">
      <h1 className="text-2xl font-bold text-gray-800 mb-4">AI 智能問答</h1>

      {/* Mode Selection */}
      <div className="flex gap-3 mb-4">
        {modeOptions.map((option) => (
          <button
            key={option.id}
            onClick={() => setMode(option.id)}
            className={`px-4 py-2 rounded-lg transition ${
              mode === option.id 
                ? 'bg-primary-500 text-white' 
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            {option.label}
          </button>
        ))}
      </div>

      {/* Chat Container */}
      <div className="flex-1 bg-white rounded-xl shadow-sm flex flex-col overflow-hidden">
        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.map((msg) => (
            <div
              key={msg.id}
              className={`flex gap-3 ${msg.role === 'user' ? 'flex-row-reverse' : ''}`}
            >
              <div className={`w-8 h-8 rounded-full flex items-center justify-center ${
                msg.role === 'user' ? 'bg-primary-500' : 'bg-gray-200'
              }`}>
                {msg.role === 'user' ? (
                  <User className="w-4 h-4 text-white" />
                ) : (
                  <Bot className="w-4 h-4 text-gray-600" />
                )}
              </div>
              <div className={`max-w-[70%] rounded-xl p-4 ${
                msg.role === 'user' 
                  ? 'bg-primary-500 text-white' 
                  : 'bg-gray-100 text-gray-800'
              }`}>
                <p className="whitespace-pre-wrap">{msg.content}</p>
                
                {/* Sources */}
                {msg.sources && msg.sources.length > 0 && (
                  <div className="mt-3 pt-3 border-t border-gray-200">
                    <p className="text-sm font-medium mb-2">📚 參考來源：</p>
                    {msg.sources.map((source, idx) => (
                      <div key={idx} className="text-sm opacity-80 mb-1">
                        • {source.title}
                      </div>
                    ))}
                  </div>
                )}

                {/* Feedback */}
                {msg.role === 'assistant' && (
                  <div className="mt-3 pt-3 border-t border-gray-200 flex gap-2">
                    <button className="text-sm opacity-70 hover:opacity-100 flex items-center gap-1">
                      <ThumbsUp className="w-4 h-4" /> 有用
                    </button>
                    <button className="text-sm opacity-70 hover:opacity-100 flex items-center gap-1">
                      <ThumbsDown className="w-4 h-4" /> 不準確
                    </button>
                  </div>
                )}
              </div>
            </div>
          ))}
          
          {loading && (
            <div className="flex gap-3">
              <div className="w-8 h-8 rounded-full bg-gray-200 flex items-center justify-center">
                <Bot className="w-4 h-4 text-gray-600" />
              </div>
              <div className="bg-gray-100 rounded-xl p-4">
                <div className="flex gap-1">
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Input */}
        <div className="p-4 border-t">
          <div className="flex gap-3">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSend()}
              placeholder="輸入你的問題..."
              className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
            />
            <button
              onClick={handleSend}
              disabled={!input.trim() || loading}
              className="px-6 py-2 bg-primary-500 text-white rounded-lg hover:bg-primary-600 disabled:opacity-50 transition flex items-center gap-2"
            >
              <Send className="w-4 h-4" />
              發送
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
