import { useState, useEffect } from 'react'
import StockCard from './StockCard'

interface Stock {
  ticker: string
  name: string
  price: number
  pct_change: number
  rank: number | null
}

interface WatchlistProps {
  period: string
}

export default function Watchlist({ period }: WatchlistProps) {
  const [stocks, setStocks] = useState<Stock[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchWatchlist = async () => {
      setLoading(true)
      setError(null)
      try {
        const response = await fetch(`http://localhost:8000/api/watchlist?period=${period}`)
        if (!response.ok) throw new Error('Failed to fetch')
        const data = await response.json()
        setStocks(data.data)
      } catch (err) {
        setError('Unable to load watchlist')
        console.error(err)
      } finally {
        setLoading(false)
      }
    }

    fetchWatchlist()
  }, [period])

  return (
    <section className="fade-in">
      <h2 className="text-2xl font-bold mb-6">Your Watchlist</h2>
      {loading && (
        <div className="flex justify-center py-12">
          <div className="animate-pulse">Loading watchlist...</div>
        </div>
      )}
      {error && (
        <div className="bg-rose-500/20 border border-rose-500/50 rounded-lg p-4 text-rose-200">
          {error}
        </div>
      )}
      {!loading && !error && (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {stocks.map((stock) => (
            <StockCard key={stock.ticker} stock={stock} />
          ))}
        </div>
      )}
    </section>
  )
}
