'use client'

import { useState } from 'react'
import { Search, Upload, FileText, Trash2, Eye } from 'lucide-react'

const documents = [
  { id: 1, name: '中三中文閱讀理解教材.pdf', type: 'PDF', size: '2.5MB', chunks: 156, date: '2024-01-15' },
  { id: 2, name: 'DSE 數學試卷範例.docx', type: 'Word', size: '1.2MB', chunks: 89, date: '2024-01-14' },
  { id: 3, name: '教師教案模板.docx', type: 'Word', size: '0.5MB', chunks: 34, date: '2024-01-13' },
  { id: 4, name: 'TSA 英文練習.pdf', type: 'PDF', size: '3.2MB', chunks: 234, date: '2024-01-12' },
]

export default function KnowledgePage() {
  const [searchQuery, setSearchQuery] = useState('')
  const [uploading, setUploading] = useState(false)

  const handleUpload = () => {
    setUploading(true)
    setTimeout(() => setUploading(false), 2000)
  }

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold text-gray-800">知識庫管理</h1>
        <button
          onClick={handleUpload}
          className="flex items-center gap-2 px-4 py-2 bg-primary-500 text-white rounded-lg hover:bg-primary-600 transition"
        >
          <Upload className="w-5 h-5" />
          上傳文檔
        </button>
      </div>

      {/* Search */}
      <div className="bg-white rounded-xl shadow-sm p-4 mb-6">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
          <input
            type="text"
            placeholder="搜索知識庫..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
          />
        </div>
      </div>

      {/* Documents List */}
      <div className="bg-white rounded-xl shadow-sm overflow-hidden">
        <table className="w-full">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">文檔</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">類型</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">大小</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Chunks</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">日期</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">操作</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {documents.map((doc) => (
              <tr key={doc.id} className="hover:bg-gray-50">
                <td className="px-6 py-4">
                  <div className="flex items-center gap-3">
                    <FileText className="w-5 h-5 text-gray-400" />
                    <span className="font-medium text-gray-800">{doc.name}</span>
                  </div>
                </td>
                <td className="px-6 py-4">
                  <span className="px-2 py-1 bg-gray-100 text-gray-600 rounded text-sm">
                    {doc.type}
                  </span>
                </td>
                <td className="px-6 py-4 text-gray-600">{doc.size}</td>
                <td className="px-6 py-4 text-gray-600">{doc.chunks}</td>
                <td className="px-6 py-4 text-gray-600">{doc.date}</td>
                <td className="px-6 py-4">
                  <div className="flex gap-2">
                    <button className="p-2 hover:bg-gray-100 rounded-lg text-gray-600">
                      <Eye className="w-4 h-4" />
                    </button>
                    <button className="p-2 hover:bg-red-50 rounded-lg text-red-600">
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Upload Modal */}
      {uploading && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
          <div className="bg-white rounded-xl p-8 max-w-md w-full mx-4">
            <div className="text-center">
              <div className="w-16 h-16 border-4 border-primary-500 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
              <h3 className="text-lg font-semibold text-gray-800">上傳中...</h3>
              <p className="text-gray-600 mt-2">正在處理文檔並生成向量</p>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
