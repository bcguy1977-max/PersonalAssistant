import { useState, useEffect } from 'react'
import StockCard from './StockCard'

interface Stock {
  ticker: string
  name: string
  price: number
  pct_change: number
  rank: number
}

interface TopMoversProps {
  region: 'us' | 'sg'
  period: string
}

export default function TopMovers({ region, period }: TopMoversProps) {
  const [stocks, setStocks] = useState<Stock[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const title = region === 'us' ? '🚀 Top US Movers' : '🌏 Top Singapore Movers'

  useEffect(() => {
    const fetchTopMovers = async () => {
      setLoading(true)
      setError(null)
      try {
        const response = await fetch(
          `http://localhost:8000/api/top-movers?region=${region}&period=${period}&limit=5`
        )
        if (!response.ok) throw new Error('Failed to fetch')
        const data = await response.json()
        setStocks(data.data)
      } catch (err) {
        setError('Unable to load movers')
        console.error(err)
      } finally {
        setLoading(false)
      }
    }

    fetchTopMovers()
  }, [region, period])

  return (
    <section className="fade-in">
      <h2 className="text-2xl font-bold mb-6">{title}</h2>
      {loading && (
        <div className="flex justify-center py-12">
          <div className="animate-pulse">Loading movers...</div>
        </div>
      )}
      {error && (
        <div className="bg-rose-500/20 border border-rose-500/50 rounded-lg p-4 text-rose-200">
          {error}
        </div>
      )}
      {!loading && !error && (
        <div className="space-y-3">
          {stocks.map((stock) => (
            <StockCard key={stock.ticker} stock={stock} />
          ))}
        </div>
      )}
    </section>
  )
}
