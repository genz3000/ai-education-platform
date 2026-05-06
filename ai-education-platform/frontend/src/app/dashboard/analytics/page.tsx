'use client'

import { TrendingUp, TrendingDown, AlertTriangle, Book } from 'lucide-react'

export default function AnalyticsPage() {
  const masteryData = [
    { topic: '中文閱讀理解', mastery: 85, trend: 'up' },
    { topic: '寫作技巧', mastery: 78, trend: 'up' },
    { topic: '數學應用題', mastery: 45, trend: 'down' },
    { topic: '英文語法', mastery: 52, trend: 'down' },
    { topic: '科學知識', mastery: 72, trend: 'stable' },
  ]

  const trends = [
    { date: '1/1', score: 65 },
    { date: '1/8', score: 68 },
    { date: '1/15', score: 72 },
    { date: '1/22', score: 70 },
    { date: '1/29', score: 75 },
    { date: '2/5', score: 78 },
    { date: '2/12', score: 82 },
    { date: '2/19', score: 85 },
  ]

  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-800 mb-6">學習分析</h1>

      {/* Overall Stats */}
      <div className="grid md:grid-cols-4 gap-6 mb-8">
        <div className="bg-white rounded-xl shadow-sm p-6">
          <div className="text-sm text-gray-500 mb-1">整體掌握度</div>
          <div className="text-3xl font-bold text-primary-600">72%</div>
        </div>
        <div className="bg-white rounded-xl shadow-sm p-6">
          <div className="text-sm text-gray-500 mb-1">學習時長</div>
          <div className="text-3xl font-bold text-green-600">24h</div>
        </div>
        <div className="bg-white rounded-xl shadow-sm p-6">
          <div className="text-sm text-gray-500 mb-1">正確率</div>
          <div className="text-3xl font-bold text-blue-600">78%</div>
        </div>
        <div className="bg-white rounded-xl shadow-sm p-6">
          <div className="text-sm text-gray-500 mb-1">風險等級</div>
          <div className="text-3xl font-bold text-yellow-600">中</div>
        </div>
      </div>

      <div className="grid md:grid-cols-2 gap-6">
        {/* Learning Trend Chart */}
        <div className="bg-white rounded-xl shadow-sm p-6">
          <h2 className="text-lg font-semibold mb-4">學習趨勢</h2>
          <div className="h-48 flex items-end justify-between gap-2">
            {trends.map((t, i) => (
              <div key={i} className="flex-1 flex flex-col items-center">
                <div 
                  className="w-full bg-primary-500 rounded-t transition-all hover:bg-primary-600"
                  style={{ height: `${t.score}%` }}
                ></div>
                <span className="text-xs text-gray-500 mt-2">{t.date}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Topic Mastery */}
        <div className="bg-white rounded-xl shadow-sm p-6">
          <h2 className="text-lg font-semibold mb-4">課題掌握度</h2>
          <div className="space-y-4">
            {masteryData.map((item, i) => (
              <div key={i}>
                <div className="flex justify-between text-sm mb-1">
                  <span className="text-gray-700">{item.topic}</span>
                  <span className={`flex items-center gap-1 ${
                    item.mastery >= 70 ? 'text-green-600' : item.mastery >= 50 ? 'text-yellow-600' : 'text-red-600'
                  }`}>
                    {item.mastery}%
                    {item.trend === 'up' && <TrendingUp className="w-4 h-4" />}
                    {item.trend === 'down' && <TrendingDown className="w-4 h-4" />}
                  </span>
                </div>
                <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
                  <div 
                    className={`h-full rounded-full ${
                      item.mastery >= 70 ? 'bg-green-500' : item.mastery >= 50 ? 'bg-yellow-500' : 'bg-red-500'
                    }`}
                    style={{ width: `${item.mastery}%` }}
                  ></div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Strengths */}
        <div className="bg-white rounded-xl shadow-sm p-6">
          <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
            <span className="text-2xl">💪</span> 強項
          </h2>
          <div className="space-y-3">
            <div className="flex items-center gap-3 p-3 bg-green-50 rounded-lg">
              <Book className="w-5 h-5 text-green-600" />
              <span className="text-green-800">中文閱讀理解 - 掌握度 85%</span>
            </div>
            <div className="flex items-center gap-3 p-3 bg-green-50 rounded-lg">
              <Book className="w-5 h-5 text-green-600" />
              <span className="text-green-800">寫作技巧 - 掌握度 78%</span>
            </div>
          </div>
        </div>

        {/* Weaknesses */}
        <div className="bg-white rounded-xl shadow-sm p-6">
          <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
            <span className="text-2xl">⚠️</span> 弱項
          </h2>
          <div className="space-y-3">
            <div className="flex items-center gap-3 p-3 bg-red-50 rounded-lg">
              <AlertTriangle className="w-5 h-5 text-red-600" />
              <span className="text-red-800">數學應用題 - 掌握度 45%</span>
            </div>
            <div className="flex items-center gap-3 p-3 bg-yellow-50 rounded-lg">
              <AlertTriangle className="w-5 h-5 text-yellow-600" />
              <span className="text-yellow-800">英文語法 - 掌握度 52%</span>
            </div>
          </div>
        </div>
      </div>

      {/* Recommendations */}
      <div className="bg-white rounded-xl shadow-sm p-6 mt-6">
        <h2 className="text-lg font-semibold mb-4">🎯 學習建議</h2>
        <div className="grid md:grid-cols-3 gap-4">
          <div className="p-4 bg-primary-50 rounded-lg border-l-4 border-primary-500">
            <h3 className="font-medium text-gray-800 mb-2">數學應用題訓練</h3>
            <p className="text-gray-600 text-sm">建議每天練習 10 道應用題</p>
            <span className="inline-block mt-2 px-2 py-1 bg-primary-100 text-primary-700 rounded text-xs">優先</span>
          </div>
          <div className="p-4 bg-blue-50 rounded-lg border-l-4 border-blue-500">
            <h3 className="font-medium text-gray-800 mb-2">英文閱讀訓練</h3>
            <p className="text-gray-600 text-sm">每週完成 2 篇英語閱讀</p>
            <span className="inline-block mt-2 px-2 py-1 bg-blue-100 text-blue-700 rounded text-xs">建議</span>
          </div>
          <div className="p-4 bg-purple-50 rounded-lg border-l-4 border-purple-500">
            <h3 className="font-medium text-gray-800 mb-2">參加課後輔導</h3>
            <p className="text-gray-600 text-sm">針對弱項進行針對性輔導</p>
            <span className="inline-block mt-2 px-2 py-1 bg-purple-100 text-purple-700 rounded text-xs">選修</span>
          </div>
        </div>
      </div>
    </div>
  )
}
