'use client'

import { useState } from 'react'
import { FileText, CheckCircle, Clock, Target } from 'lucide-react'

export default function AssessmentPage() {
  const [topic, setTopic] = useState('')
  const [difficulty, setDifficulty] = useState(3)
  const [generating, setGenerating] = useState(false)
  const [questions, setQuestions] = useState<any[]>([])
  const [submitted, setSubmitted] = useState(false)

  const handleGenerate = () => {
    setGenerating(true)
    setTimeout(() => {
      setQuestions([
        { id: 1, type: 'mcq', content: '以下哪個選項描述了正確的學習策略？', options: ['A', 'B', 'C', 'D'] },
        { id: 2, type: 'short', content: '請解釋人工智能在教育領域的應用。' },
        { id: 3, type: 'mcq', content: '香港中學文憑考試（DSE）包含多少個核心科目？', options: ['A', 'B', 'C', 'D'] },
      ])
      setGenerating(false)
    }, 2000)
  }

  const handleSubmit = () => {
    setSubmitted(true)
  }

  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-800 mb-6">AI 評估系統</h1>

      {/* Generate Section */}
      {!questions.length && (
        <div className="bg-white rounded-xl shadow-sm p-6">
          <h2 className="text-lg font-semibold mb-4">生成試卷</h2>
          
          <div className="grid md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">課題</label>
              <select
                value={topic}
                onChange={(e) => setTopic(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg"
              >
                <option value="">選擇課題...</option>
                <option value="chinese">中文閱讀理解</option>
                <option value="math">DSE 數學</option>
                <option value="english">TSA 英文</option>
                <option value="custom">自定義課題</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">難度</label>
              <div className="flex items-center gap-4">
                <input
                  type="range"
                  min="1"
                  max="5"
                  value={difficulty}
                  onChange={(e) => setDifficulty(parseInt(e.target.value))}
                  className="flex-1"
                />
                <span className="px-3 py-1 bg-primary-100 text-primary-700 rounded-lg">
                  {difficulty} 星
                </span>
              </div>
            </div>
          </div>

          <button
            onClick={handleGenerate}
            disabled={!topic || generating}
            className="mt-6 px-6 py-3 bg-primary-500 text-white rounded-lg hover:bg-primary-600 disabled:opacity-50 transition flex items-center gap-2"
          >
            <FileText className="w-5 h-5" />
            {generating ? '生成中...' : '生成試卷'}
          </button>
        </div>
      )}

      {/* Questions */}
      {questions.length > 0 && !submitted && (
        <div className="space-y-4">
          <div className="bg-white rounded-xl shadow-sm p-6">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-lg font-semibold">生成的試卷</h2>
              <span className="px-3 py-1 bg-gray-100 rounded-lg text-sm">
                {questions.length} 題
              </span>
            </div>

            {questions.map((q, idx) => (
              <div key={q.id} className="border-b last:border-0 py-4">
                <div className="flex items-start gap-3">
                  <span className="w-8 h-8 bg-primary-100 text-primary-700 rounded-full flex items-center justify-center font-medium">
                    {idx + 1}
                  </span>
                  <div className="flex-1">
                    <p className="font-medium text-gray-800 mb-3">{q.content}</p>
                    {q.type === 'mcq' && (
                      <div className="grid grid-cols-2 gap-2">
                        {['A', 'B', 'C', 'D'].map((opt) => (
                          <label key={opt} className="flex items-center gap-2 p-2 border rounded-lg hover:bg-gray-50 cursor-pointer">
                            <input type="radio" name={`q-${q.id}`} className="text-primary-600" />
                            <span>{opt}. 選項 {opt}</span>
                          </label>
                        ))}
                      </div>
                    )}
                    {q.type === 'short' && (
                      <textarea
                        className="w-full px-3 py-2 border rounded-lg h-24"
                        placeholder="輸入你的答案..."
                      />
                    )}
                  </div>
                </div>
              </div>
            ))}

            <button
              onClick={handleSubmit}
              className="mt-6 px-6 py-3 bg-green-500 text-white rounded-lg hover:bg-green-600 transition"
            >
              提交答案
            </button>
          </div>
        </div>
      )}

      {/* Results */}
      {submitted && (
        <div className="bg-white rounded-xl shadow-sm p-6">
          <div className="text-center mb-8">
            <div className="w-24 h-24 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <CheckCircle className="w-12 h-12 text-green-500" />
            </div>
            <h2 className="text-2xl font-bold text-gray-800">提交成功！</h2>
            <p className="text-gray-600 mt-2">AI 正在批改中...</p>
          </div>

          <div className="grid md:grid-cols-3 gap-6 mb-8">
            <div className="bg-gray-50 rounded-xl p-6 text-center">
              <Target className="w-8 h-8 text-primary-500 mx-auto mb-2" />
              <div className="text-3xl font-bold text-gray-800">85</div>
              <div className="text-gray-600">總分</div>
            </div>
            <div className="bg-gray-50 rounded-xl p-6 text-center">
              <CheckCircle className="w-8 h-8 text-green-500 mx-auto mb-2" />
              <div className="text-3xl font-bold text-gray-800">85%</div>
              <div className="text-gray-600">正確率</div>
            </div>
            <div className="bg-gray-50 rounded-xl p-6 text-center">
              <Clock className="w-8 h-8 text-orange-500 mx-auto mb-2" />
              <div className="text-3xl font-bold text-gray-800">B</div>
              <div className="text-gray-600">預計等第</div>
            </div>
          </div>

          <div className="border-t pt-6">
            <h3 className="font-semibold text-gray-800 mb-4">📋 詳細反饋</h3>
            <div className="space-y-3">
              <div className="p-3 bg-red-50 rounded-lg text-red-700">
                ❌ 第 2 題：理解偏差，需要加強閱讀理解訓練
              </div>
              <div className="p-3 bg-yellow-50 rounded-lg text-yellow-700">
                ⚠️ 第 5 題：計算錯誤，注意驗算
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
