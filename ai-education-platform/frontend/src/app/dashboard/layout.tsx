'use client'

import { useState } from 'react'
import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { Home, Book, MessageCircle, FileText, BarChart3, Settings, LogOut } from 'lucide-react'

const menuItems = [
  { href: '/dashboard', icon: Home, label: '首頁' },
  { href: '/dashboard/knowledge', icon: Book, label: '知識庫' },
  { href: '/dashboard/qa', icon: MessageCircle, label: 'AI 問答' },
  { href: '/dashboard/assessment', icon: FileText, label: '評估' },
  { href: '/dashboard/analytics', icon: BarChart3, label: '分析' },
  { href: '/dashboard/settings', icon: Settings, label: '設置' },
]

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  const pathname = usePathname()
  const [sidebarOpen, setSidebarOpen] = useState(true)

  return (
    <div className="min-h-screen bg-gray-100 flex">
      {/* Sidebar */}
      <aside className={`${sidebarOpen ? 'w-64' : 'w-20'} bg-gray-900 text-white transition-all duration-300 flex flex-col`}>
        <div className="p-4 border-b border-gray-700">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-primary-500 rounded-lg flex items-center justify-center">
              <span className="text-xl">🎓</span>
            </div>
            {sidebarOpen && <span className="font-bold">AI 教育</span>}
          </div>
        </div>

        <nav className="flex-1 p-4 space-y-2">
          {menuItems.map((item) => {
            const isActive = pathname === item.href
            return (
              <Link
                key={item.href}
                href={item.href}
                className={`flex items-center gap-3 px-4 py-3 rounded-lg transition ${
                  isActive ? 'bg-primary-600' : 'hover:bg-gray-800'
                }`}
              >
                <item.icon className="w-5 h-5" />
                {sidebarOpen && <span>{item.label}</span>}
              </Link>
            )
          })}
        </nav>

        <div className="p-4 border-t border-gray-700">
          <Link
            href="/login"
            className="flex items-center gap-3 px-4 py-3 rounded-lg hover:bg-gray-800 transition text-red-400"
          >
            <LogOut className="w-5 h-5" />
            {sidebarOpen && <span>登出</span>}
          </Link>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 overflow-auto">
        {/* Top Bar */}
        <header className="bg-white shadow-sm px-6 py-4 flex justify-between items-center">
          <button
            onClick={() => setSidebarOpen(!sidebarOpen)}
            className="p-2 hover:bg-gray-100 rounded-lg"
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>
          <div className="flex items-center gap-4">
            <span className="text-gray-600">欢迎使用</span>
            <div className="w-8 h-8 bg-primary-500 rounded-full flex items-center justify-center text-white">
              U
            </div>
          </div>
        </header>

        {/* Page Content */}
        <div className="p-6">
          {children}
        </div>
      </main>
    </div>
  )
}
