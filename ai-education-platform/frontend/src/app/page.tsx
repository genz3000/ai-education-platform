'use client'

import { useState } from 'react'
import Link from 'next/link'

export default function Home() {
  const [isLoggedIn, setIsLoggedIn] = useState(false)

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 to-white">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-primary-500 rounded-lg flex items-center justify-center">
              <span className="text-white text-xl">🎓</span>
            </div>
            <h1 className="text-xl font-bold text-gray-800">AI 教育知識庫系統</h1>
          </div>
          <div className="flex gap-3">
            <Link href="/login" className="px-4 py-2 text-primary-600 hover:bg-primary-50 rounded-lg transition">
              登入
            </Link>
            <Link href="/register" className="px-4 py-2 bg-primary-500 text-white rounded-lg hover:bg-primary-600 transition">
              註冊
            </Link>
          </div>
        </div>
      </header>

      {/* Hero */}
      <main className="max-w-7xl mx-auto px-4 py-16">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold text-gray-900 mb-4">
            校本 AI 教學操作系統
          </h2>
          <p className="text-xl text-gray-600 mb-8">
            基於香港教育局「智啟學教」政策，打造智能教學新體驗
          </p>
          <div className="flex gap-4 justify-center">
            <Link href="/register" className="px-8 py-3 bg-primary-500 text-white rounded-lg hover:bg-primary-600 transition text-lg">
              立即開始
            </Link>
            <Link href="/demo" className="px-8 py-3 border-2 border-primary-500 text-primary-600 rounded-lg hover:bg-primary-50 transition text-lg">
              查看演示
            </Link>
          </div>
        </div>

        {/* Features */}
        <div className="grid md:grid-cols-3 gap-8 mb-16">
          <FeatureCard 
            icon="📚"
            title="AI 知識庫"
            description="校本教材智能管理，向量檢索，精準回答"
          />
          <FeatureCard 
            icon="💬"
            title="AI 智能問答"
            description="多輪對話，精準解答，即時回饋"
          />
          <FeatureCard 
            icon="📝"
            title="AI 評估系統"
            description="自動出題，智能批改，個人化學習"
          />
          <FeatureCard 
            icon="📊"
            title="學習分析"
            description="數據驅動，精準定位弱項"
          />
          <FeatureCard 
            icon="👨‍🏫"
            title="教師工具"
            description="教案生成，班級管理，高效備課"
          />
          <FeatureCard 
            icon="🔒"
            title="香港合規"
            description="符合私隱條例，安全可靠"
          />
        </div>

        {/* Stats */}
        <div className="bg-white rounded-2xl shadow-lg p-8">
          <div className="grid md:grid-cols-4 gap-8 text-center">
            <StatItem value="1000+" label="學校使用" />
            <StatItem value="50,000+" label="師生用戶" />
            <StatItem value="1M+" label="問答記錄" />
            <StatItem value="98%" label="準確率" />
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-gray-800 text-white py-8">
        <div className="max-w-7xl mx-auto px-4 text-center">
          <p>© 2024 AI 教育知識庫系統 | 基於香港教育局政策</p>
        </div>
      </footer>
    </div>
  )
}

function FeatureCard({ icon, title, description }: { icon: string; title: string; description: string }) {
  return (
    <div className="bg-white rounded-xl shadow-md p-6 hover:shadow-lg transition">
      <div className="text-4xl mb-4">{icon}</div>
      <h3 className="text-lg font-semibold text-gray-800 mb-2">{title}</h3>
      <p className="text-gray-600">{description}</p>
    </div>
  )
}

function StatItem({ value, label }: { value: string; label: string }) {
  return (
    <div>
      <div className="text-3xl font-bold text-primary-600 mb-1">{value}</div>
      <div className="text-gray-600">{label}</div>
    </div>
  )
}
