'use client'

import { useState } from 'react'
import { Send, User, Bot, ThumbsUp, ThumbsDown, BookOpen, ChevronDown, ChevronUp } from 'lucide-react'

interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string
  context?: string
  sources?: { source: string; score: number; excerpt: string }[]
}

const modeOptions = [
  { id: 'student', label: '👨‍🎓 Student', desc: 'Simple, easy-to-understand answers' },
  { id: 'teacher', label: '👨‍🏫 Teacher', desc: 'Professional teaching suggestions' },
  { id: 'parent', label: '👨‍👩‍👧 Parent', desc: 'Help understand child learning' },
]

export default function QAPage() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      role: 'assistant',
      content: 'Hello! I\'m your AI teaching assistant. Ask me any question and I\'ll answer based on the school\'s knowledge base.',
    }
  ])
  const [input, setInput] = useState('')
  const [mode, setMode] = useState('student')
  const [loading, setLoading] = useState(false)
  const [expandedSources, setExpandedSources] = useState<string[]>([])

  const toggleSource = (id: string) => {
    setExpandedSources(prev => 
      prev.includes(id) ? prev.filter(x => x !== id) : [...prev, id]
    )
  }

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
      // First, query RAG to get context
      const ragRes = await fetch('http://localhost:8000/api/v1/rag/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          query: input,
          school_id: 'b52ed795-43d2-4ad3-b765-a48e24c35862',
          top_k: 3
        })
      })

      const ragData = await ragRes.json()
      
      // Build answer from RAG context
      let answer = ''
      if (ragData.chunks && ragData.chunks.length > 0) {
        const contextText = ragData.chunks.map((c: any) => c.content).join('\n\n')
        answer = `Based on the school knowledge base:\n\n${contextText}\n\n[Sources: ${ragData.chunks.map((c: any) => c.source).join(', ')}]`
      } else {
        answer = 'I couldn\'t find relevant information in the knowledge base. Try uploading some documents first, or rephrase your question.'
      }

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: answer,
        context: ragData.context,
        sources: ragData.citations
      }

      setMessages(prev => [...prev, assistantMessage])
    } catch (error) {
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: 'Sorry, an error occurred. Please check if the backend is running.'
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="h-[calc(100vh-180px)] flex flex-col">
      <h1 className="text-2xl font-bold text-gray-800 mb-4">🤖 AI Smart Q&A</h1>

      {/* Mode Selection */}
      <div className="flex gap-3 mb-4">
        {modeOptions.map((option) => (
          <button
            key={option.id}
            onClick={() => setMode(option.id)}
            className={`px-4 py-2 rounded-lg transition text-sm ${
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
              <div className={`w-10 h-10 rounded-full flex items-center justify-center shrink-0 ${
                msg.role === 'user' ? 'bg-primary-500' : 'bg-blue-100'
              }`}>
                {msg.role === 'user' ? (
                  <User className="w-5 h-5 text-white" />
                ) : (
                  <Bot className="w-5 h-5 text-blue-600" />
                )}
              </div>
              <div className={`max-w-[75%] rounded-2xl p-4 ${
                msg.role === 'user' 
                  ? 'bg-primary-500 text-white' 
                  : 'bg-gray-50 text-gray-800 border border-gray-200'
              }`}>
                <p className="whitespace-pre-wrap leading-relaxed">{msg.content}</p>
                
                {/* Sources with expandable excerpts */}
                {msg.sources && msg.sources.length > 0 && (
                  <div className="mt-4 pt-4 border-t border-gray-200">
                    <p className="text-sm font-semibold mb-3 flex items-center gap-2">
                      <BookOpen className="w-4 h-4" />
                      📚 Sources ({msg.sources.length})
                    </p>
                    <div className="space-y-2">
                      {msg.sources.map((source, idx) => {
                        const sourceId = `${msg.id}-source-${idx}`
                        const isExpanded = expandedSources.includes(sourceId)
                        return (
                          <div 
                            key={idx} 
                            className="bg-white rounded-lg p-3 border border-gray-100"
                          >
                            <div className="flex items-center justify-between">
                              <div className="flex items-center gap-2">
                                <span className="text-xs bg-blue-100 text-blue-700 px-2 py-1 rounded">
                                  {Math.round(source.score * 100)}% match
                                </span>
                                <span className="font-medium text-sm">{source.source}</span>
                              </div>
                              <button 
                                onClick={() => toggleSource(sourceId)}
                                className="text-gray-400 hover:text-gray-600"
                              >
                                {isExpanded ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
                              </button>
                            </div>
                            {isExpanded && (
                              <p className="mt-2 text-sm text-gray-600 bg-gray-50 p-2 rounded">
                                {source.excerpt}
                              </p>
                            )}
                          </div>
                        )
                      })}
                    </div>
                  </div>
                )}

                {/* Feedback buttons */}
                {msg.role === 'assistant' && (
                  <div className="mt-4 pt-3 border-t border-gray-200 flex gap-3">
                    <button className="text-sm opacity-70 hover:opacity-100 flex items-center gap-1 transition">
                      <ThumbsUp className="w-4 h-4" /> Helpful
                    </button>
                    <button className="text-sm opacity-70 hover:opacity-100 flex items-center gap-1 transition">
                      <ThumbsDown className="w-4 h-4" /> Not accurate
                    </button>
                  </div>
                )}
              </div>
            </div>
          ))}
          
          {loading && (
            <div className="flex gap-3">
              <div className="w-10 h-10 rounded-full bg-blue-100 flex items-center justify-center">
                <Bot className="w-5 h-5 text-blue-600" />
              </div>
              <div className="bg-gray-50 rounded-2xl p-4 border border-gray-200">
                <div className="flex gap-1">
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
                </div>
                <p className="text-sm text-gray-500 mt-2">Searching knowledge base...</p>
              </div>
            </div>
          )}
        </div>

        {/* Input */}
        <div className="p-4 border-t bg-gray-50">
          <div className="flex gap-3">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && !loading && handleSend()}
              placeholder="Ask about math, science, or any school subject..."
              className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            />
            <button
              onClick={handleSend}
              disabled={!input.trim() || loading}
              className="px-6 py-3 bg-primary-500 text-white rounded-lg hover:bg-primary-600 disabled:opacity-50 transition flex items-center gap-2 font-medium"
            >
              <Send className="w-4 h-4" />
              Send
            </button>
          </div>
          <p className="text-xs text-gray-500 mt-2">
            Powered by RAG • Queries school knowledge base
          </p>
        </div>
      </div>
    </div>
  )
}