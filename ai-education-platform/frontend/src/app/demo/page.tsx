'use client';

import { useState } from 'react';

export default function DemoPage() {
  const [chatMessages, setChatMessages] = useState<Array<{role: string; content: string}>>([]);
  const [inputValue, setInputValue] = useState('');

  const demoKnowledge = [
    { title: 'Primary Math', count: 245, icon: '📐' },
    { title: 'English Materials', count: 189, icon: '📖' },
    { title: 'Science Lab Manual', count: 156, icon: '🔬' },
    { title: 'Chinese Writing', count: 203, icon: '✍️' },
  ];

  const handleSend = () => {
    if (!inputValue.trim()) return;
    
    setChatMessages([...chatMessages, { role: 'user', content: inputValue }]);
    setInputValue('');
    
    // Simulate AI response
    setTimeout(() => {
      setChatMessages(prev => [...prev, {
        role: 'assistant',
        content: 'This is a demo response from AI Assistant. The system is connected to the local knowledge base and can answer questions based on school materials.'
      }]);
    }, 1000);
  };

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
            <a href="/" className="px-4 py-2 text-primary-600 hover:bg-primary-50 rounded-lg transition">Home</a>
            <a href="/register" className="px-4 py-2 bg-primary-500 text-white rounded-lg hover:bg-primary-600 transition">Register</a>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-8">
        {/* Demo Banner */}
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mb-8 text-center">
          <span className="text-yellow-800">🎬 Interactive demo page showcasing main features</span>
        </div>

        {/* Features Grid */}
        <div className="grid md:grid-cols-3 gap-8 mb-12">
          {/* AI Knowledge Base */}
          <div className="bg-white rounded-xl shadow-md p-6">
            <h3 className="text-lg font-semibold text-gray-800 mb-4">📚 AI Knowledge Base</h3>
            <div className="space-y-3">
              {demoKnowledge.map((item, i) => (
                <div key={i} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                  <div className="flex items-center gap-3">
                    <span className="text-2xl">{item.icon}</span>
                    <span className="text-gray-700">{item.title}</span>
                  </div>
                  <span className="text-sm text-gray-500">{item.count} docs</span>
                </div>
              ))}
            </div>
            <button className="w-full mt-4 py-2 bg-primary-100 text-primary-700 rounded-lg hover:bg-primary-200 transition">
              Upload Materials
            </button>
          </div>

          {/* AI Smart Q&A */}
          <div className="bg-white rounded-xl shadow-md p-6">
            <h3 className="text-lg font-semibold text-gray-800 mb-4">💬 AI Smart Q&A</h3>
            <div className="h-64 bg-gray-50 rounded-lg p-4 overflow-y-auto">
              {chatMessages.length === 0 ? (
                <p className="text-gray-400 text-center">Start asking questions...</p>
              ) : (
                chatMessages.map((msg, i) => (
                  <div key={i} className={`mb-3 ${msg.role === 'user' ? 'text-right' : 'text-left'}`}>
                    <div className={`inline-block px-4 py-2 rounded-lg ${msg.role === 'user' ? 'bg-primary-500 text-white' : 'bg-gray-200 text-gray-800'}`}>
                      {msg.content}
                    </div>
                  </div>
                ))
              )}
            </div>
            <div className="flex gap-2 mt-4">
              <input
                type="text"
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && handleSend()}
                placeholder="Ask a question..."
                className="flex-1 px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
              />
              <button onClick={handleSend} className="px-4 py-2 bg-primary-500 text-white rounded-lg hover:bg-primary-600 transition">
                Send
              </button>
            </div>
          </div>

          {/* AI Assessment System */}
          <div className="bg-white rounded-xl shadow-md p-6">
            <h3 className="text-lg font-semibold text-gray-800 mb-4">📝 AI Assessment System</h3>
            <div className="space-y-4">
              <div className="bg-green-50 p-4 rounded-lg">
                <div className="flex justify-between mb-2">
                  <span className="text-green-700">Math Skills</span>
                  <span className="text-green-600 font-semibold">85%</span>
                </div>
                <div className="w-full bg-green-200 rounded-full h-2">
                  <div className="bg-green-500 h-2 rounded-full" style={{width: '85%'}}></div>
                </div>
              </div>
              <div className="bg-blue-50 p-4 rounded-lg">
                <div className="flex justify-between mb-2">
                  <span className="text-blue-700">English Reading</span>
                  <span className="text-blue-600 font-semibold">72%</span>
                </div>
                <div className="w-full bg-blue-200 rounded-full h-2">
                  <div className="bg-blue-500 h-2 rounded-full" style={{width: '72%'}}></div>
                </div>
              </div>
              <div className="bg-purple-50 p-4 rounded-lg">
                <div className="flex justify-between mb-2">
                  <span className="text-purple-700">Science Inquiry</span>
                  <span className="text-purple-600 font-semibold">90%</span>
                </div>
                <div className="w-full bg-purple-200 rounded-full h-2">
                  <div className="bg-purple-500 h-2 rounded-full" style={{width: '90%'}}></div>
                </div>
              </div>
            </div>
            <button className="w-full mt-4 py-2 bg-primary-500 text-white rounded-lg hover:bg-primary-600 transition">
              Start Assessment
            </button>
          </div>
        </div>

        {/* Dashboard Preview */}
        <div className="bg-white rounded-xl shadow-md p-6 mb-8">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">📊 Learning Analytics Dashboard</h3>
          <div className="grid md:grid-cols-4 gap-6">
            <div className="text-center p-6 bg-primary-50 rounded-xl">
              <div className="text-3xl font-bold text-primary-600">156</div>
              <div className="text-gray-600">Tasks Completed</div>
            </div>
            <div className="text-center p-6 bg-green-50 rounded-xl">
              <div className="text-3xl font-bold text-green-600">87%</div>
              <div className="text-gray-600">Accuracy Rate</div>
            </div>
            <div className="text-center p-6 bg-blue-50 rounded-xl">
              <div className="text-3xl font-bold text-blue-600">12h</div>
              <div className="text-gray-600">Study Time</div>
            </div>
            <div className="text-center p-6 bg-purple-50 rounded-xl">
              <div className="text-3xl font-bold text-purple-600">Top 15%</div>
              <div className="text-gray-600">Class Ranking</div>
            </div>
          </div>
        </div>

        {/* CTA */}
        <div className="text-center">
          <p className="text-gray-600 mb-4">Want to experience all features? Register now to get started!</p>
          <a href="/register" className="inline-block px-8 py-3 bg-primary-500 text-white rounded-lg hover:bg-primary-600 transition text-lg">
            Register Now
          </a>
        </div>
      </main>
    </div>
  );
}