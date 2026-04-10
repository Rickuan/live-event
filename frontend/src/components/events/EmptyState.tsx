export default function EmptyState() {
  return (
    <div className="flex flex-col items-center justify-center py-24 text-center">
      <p className="text-gray-400 text-sm">目前沒有符合條件的活動</p>
      <p className="text-gray-300 text-xs mt-1">試著調整篩選條件，或稍後再回來看看</p>
    </div>
  )
}
