import { useState, useEffect } from 'react'
import Watchlist from './components/Watchlist'
import TopMovers from './components/TopMovers'
import Header from './components/Header'
import './index.css'

export default function App() {
  const [period, setPeriod] = useState('6d')
  const [refreshing, setRefreshing] = useState(false)

  const handleRefresh = () => {
    setRefreshing(true)
    setTimeout(() => setRefreshing(false), 500)
  }

  return (
    <div className="gradient-bg min-h-screen">
      <Header period={period} setPeriod={setPeriod} onRefresh={handleRefresh} refreshing={refreshing} />

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <Watchlist period={period} key={`watchlist-${period}`} />

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mt-12">
          <TopMovers region="us" period={period} key={`us-${period}`} />
          <TopMovers region="sg" period={period} key={`sg-${period}`} />
        </div>
      </main>
    </div>
  )
}
