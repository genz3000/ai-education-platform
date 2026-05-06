import type { Metadata } from 'next'
import './styles/globals.css'

export const metadata: Metadata = {
  title: 'AI 教育知識庫系統',
  description: '校本 AI 教學操作系統',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="zh-HK">
      <body>{children}</body>
    </html>
  )
}
