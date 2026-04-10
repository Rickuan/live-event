import { useRef } from 'react'
import { useNavigate } from 'react-router-dom'

export default function Navbar() {
  const navigate = useNavigate()
  const clickCount = useRef(0)
  const timer = useRef<ReturnType<typeof setTimeout>>()

  function handleLogoClick() {
    clickCount.current += 1
    clearTimeout(timer.current)
    timer.current = setTimeout(() => {
      clickCount.current = 0
    }, 2000)
    if (clickCount.current >= 5) {
      clickCount.current = 0
      navigate('/admin/login')
    }
  }

  return (
    <header className="sticky top-0 z-10 bg-white border-b border-gray-100">
      <div className="max-w-5xl mx-auto px-4 h-14 flex items-center">
        <button
          onClick={handleLogoClick}
          className="text-lg font-semibold tracking-tight text-gray-800 select-none"
        >
          Live Events
        </button>
      </div>
    </header>
  )
}
