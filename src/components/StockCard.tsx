interface StockCardProps {
  stock: {
    ticker: string
    name: string
    price: number
    pct_change: number
    rank: number | null
  }
}

export default function StockCard({ stock }: StockCardProps) {
  const isPositive = stock.pct_change >= 0

  return (
    <div className="card p-5 rounded-xl">
      <div className="flex items-start justify-between mb-3">
        <div>
          <h3 className="font-bold text-lg">{stock.ticker}</h3>
          <p className="text-slate-400 text-xs mt-0.5 truncate">{stock.name}</p>
        </div>
        {stock.rank && (
          <div className="bg-blue-500/30 text-blue-300 rounded-full w-7 h-7 flex items-center justify-center text-xs font-bold">
            #{stock.rank}
          </div>
        )}
      </div>

      <div className="flex items-baseline gap-2 mb-2">
        <span className="text-2xl font-bold">${stock.price.toFixed(2)}</span>
      </div>

      <div className={`text-sm font-semibold ${isPositive ? 'positive' : 'negative'}`}>
        <span>{isPositive ? '▲' : '▼'} {Math.abs(stock.pct_change).toFixed(2)}%</span>
      </div>
    </div>
  )
}
