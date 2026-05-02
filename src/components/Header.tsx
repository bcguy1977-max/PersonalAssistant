import { useState } from 'react'

interface HeaderProps {
  period: string
  setPeriod: (p: string) => void
  onRefresh: () => void
  refreshing: boolean
}

const periods = [
  { label: '1d', value: '2d' },
  { label: '5d', value: '6d' },
  { label: '1mo', value: '1mo' },
  { label: '3mo', value: '3mo' },
  { label: '1y', value: '1y' },
]

export default function Header({ period, setPeriod, onRefresh, refreshing }: HeaderProps) {
  return (
    <header className="border-b border-white/10 backdrop-blur-md sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent">
              📈 Personal Assistant
            </h1>
            <p className="text-slate-400 text-sm mt-1">Real-time market snapshot</p>
          </div>

          <div className="flex items-center gap-4">
            <div className="flex gap-2 bg-white/5 p-1 rounded-lg">
              {periods.map((p) => (
                <button
                  key={p.value}
                  onClick={() => setPeriod(p.value)}
                  className={`px-3 py-1 rounded transition-all text-sm font-medium ${
                    period === p.value
                      ? 'bg-blue-500 text-white'
                      : 'text-slate-400 hover:text-slate-200'
                  }`}
                >
                  {p.label}
                </button>
              ))}
            </div>

            <button
              onClick={onRefresh}
              disabled={refreshing}
              className="p-2 rounded-lg bg-white/10 hover:bg-white/20 transition disabled:opacity-50"
              title="Refresh data"
            >
              <svg
                className={`w-5 h-5 transition ${refreshing ? 'animate-spin' : ''}`}
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </header>
  )
}
