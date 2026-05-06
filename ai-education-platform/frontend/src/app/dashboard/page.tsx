'use client'

import { Book, MessageCircle, FileText, Users, TrendingUp, Clock } from 'lucide-react'

export default function DashboardHome() {
  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-800 mb-6">控制台</h1>

      {/* Stats Cards */}
      <div className="grid md:grid-cols-4 gap-6 mb-8">
        <StatCard icon={Book} label="知識庫文檔" value="1,234" color="bg-blue-500" />
        <StatCard icon={MessageCircle} label="問答記錄" value="5,678" color="bg-green-500" />
        <StatCard icon={FileText} label="生成試卷" value="89" color="bg-purple-500" />
        <StatCard icon={Users} label="活躍用戶" value="456" color="bg-orange-500" />
      </div>

      {/* Quick Actions */}
      <div className="grid md:grid-cols-3 gap-6 mb-8">
        <QuickAction 
          title="上傳教材"
          description="添加 PDF、Word、PPT 文件到知識庫"
          icon="📤"
          href="/dashboard/knowledge"
        />
        <QuickAction 
          title="開始問答"
          description="向 AI 提問任何學習問題"
          icon="💬"
          href="/dashboard/qa"
        />
        <QuickAction 
          title="生成試卷"
          description="根據課題自動生成練習題目"
          icon="📝"
          href="/dashboard/assessment"
        />
      </div>

      {/* Recent Activity */}
      <div className="bg-white rounded-xl shadow-sm p-6">
        <h2 className="text-lg font-semibold text-gray-800 mb-4">最近活動</h2>
        <div className="space-y-4">
          <ActivityItem 
            icon="📚"
            text="上傳了「中三中文閱讀理解教材.pdf」"
            time="5 分鐘前"
          />
          <ActivityItem 
            icon="💬"
            text="回答了關於「DSE數學」的問題"
            time="15 分鐘前"
          />
          <ActivityItem 
            icon="✅"
            text="完成了「英文語法測驗」，得分 85%"
            time="1 小時前"
          />
        </div>
      </div>
    </div>
  )
}

function StatCard({ icon: Icon, label, value, color }: { icon: any; label: string; value: string; color: string }) {
  return (
    <div className="bg-white rounded-xl shadow-sm p-6">
      <div className="flex items-center gap-4">
        <div className={`${color} p-3 rounded-lg`}>
          <Icon className="w-6 h-6 text-white" />
        </div>
        <div>
          <div className="text-2xl font-bold text-gray-800">{value}</div>
          <div className="text-gray-500 text-sm">{label}</div>
        </div>
      </div>
    </div>
  )
}

function QuickAction({ title, description, icon, href }: { title: string; description: string; icon: string; href: string }) {
  return (
    <a href={href} className="bg-white rounded-xl shadow-sm p-6 hover:shadow-md transition group">
      <div className="text-3xl mb-3">{icon}</div>
      <h3 className="font-semibold text-gray-800 group-hover:text-primary-600">{title}</h3>
      <p className="text-gray-500 text-sm mt-1">{description}</p>
    </a>
  )
}

function ActivityItem({ icon, text, time }: { icon: string; text: string; time: string }) {
  return (
    <div className="flex items-center gap-4 p-3 bg-gray-50 rounded-lg">
      <div className="text-2xl">{icon}</div>
      <div className="flex-1">
        <div className="text-gray-800">{text}</div>
        <div className="text-gray-500 text-sm flex items-center gap-1">
          <Clock className="w-3 h-3" />
          {time}
        </div>
      </div>
    </div>
  )
}
