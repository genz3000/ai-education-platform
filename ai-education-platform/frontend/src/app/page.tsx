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
            <h1 className="text-xl font-bold text-gray-800">AI Education Knowledge Base</h1>
          </div>
          <div className="flex gap-3">
            <Link href="/login" className="px-4 py-2 text-primary-600 hover:bg-primary-50 rounded-lg transition">
              Login
            </Link>
            <Link href="/register" className="px-4 py-2 bg-primary-500 text-white rounded-lg hover:bg-primary-600 transition">
              Register
            </Link>
          </div>
        </div>
      </header>

      {/* Hero */}
      <main className="max-w-7xl mx-auto px-4 py-16">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold text-gray-900 mb-4">
            School-Based AI Teaching Platform
          </h2>
          <p className="text-xl text-gray-600 mb-8">
            Built on Hong Kong EDB "Smart Learning" Initiative, delivering intelligent teaching experiences
          </p>
          <div className="flex gap-4 justify-center">
            <Link href="/register" className="px-8 py-3 bg-primary-500 text-white rounded-lg hover:bg-primary-600 transition text-lg">
              Get Started
            </Link>
            <Link href="/demo" className="px-8 py-3 border-2 border-primary-500 text-primary-600 rounded-lg hover:bg-primary-50 transition text-lg">
              View Demo
            </Link>
          </div>
        </div>

        {/* Features */}
        <div className="grid md:grid-cols-3 gap-8 mb-16">
          <FeatureCard 
            icon="📚"
            title="AI Knowledge Base"
            description="School-based material management, vector search, accurate answers"
          />
          <FeatureCard 
            icon="💬"
            title="AI Smart Q&A"
            description="Multi-turn conversation, precise answers, instant feedback"
          />
          <FeatureCard 
            icon="📝"
            title="AI Assessment System"
            description="Auto-generated questions, intelligent grading, personalized learning"
          />
          <FeatureCard 
            icon="📊"
            title="Learning Analytics"
            description="Data-driven insights, precise weak-point identification"
          />
          <FeatureCard 
            icon="👨‍🏫"
            title="Teacher Tools"
            description="Lesson planning, class management, efficient preparation"
          />
          <FeatureCard 
            icon="🔒"
            title="HK Compliance"
            description="Privacy ordinance compliant, safe and reliable"
          />
        </div>

        {/* Stats */}
        <div className="bg-white rounded-2xl shadow-lg p-8">
          <div className="grid md:grid-cols-4 gap-8 text-center">
            <StatItem value="1000+" label="Schools" />
            <StatItem value="50,000+" label="Users" />
            <StatItem value="1M+" label="Q&A Records" />
            <StatItem value="98%" label="Accuracy" />
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-gray-800 text-white py-8">
        <div className="max-w-7xl mx-auto px-4 text-center">
          <p>© 2024 AI Education Knowledge Base | Based on HK EDB Policy</p>
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