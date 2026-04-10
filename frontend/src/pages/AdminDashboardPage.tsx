import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import bcrypt from 'bcryptjs'
import { api } from '../lib/axios'
import type { AdminHealthResponse, EventListResponse } from '../types/api'
import type { Event } from '../types'

const EMPTY_FORM = { title: '', start_at: '', venue_name: '', venue_city: '' }

function ManualAddEventButton() {
  const queryClient = useQueryClient()
  const [open, setOpen] = useState(false)
  const [form, setForm] = useState(EMPTY_FORM)

  const mutation = useMutation({
    mutationFn: () =>
      api.post('/admin/events', {
        ...form,
        start_at: new Date(form.start_at).toISOString(),
      }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['admin', 'events'] })
      setOpen(false)
      setForm(EMPTY_FORM)
    },
  })

  const field = (key: keyof typeof EMPTY_FORM) => ({
    value: form[key],
    onChange: (e: React.ChangeEvent<HTMLInputElement>) =>
      setForm((f) => ({ ...f, [key]: e.target.value })),
    required: true,
    className: 'w-full border border-gray-200 rounded px-2 py-1.5 text-sm focus:outline-none focus:border-gray-400',
  })

  const canSubmit = form.title && form.start_at && form.venue_name && form.venue_city

  return (
    <>
      <button
        onClick={() => setOpen(true)}
        className="ml-2 text-xs px-2 py-0.5 rounded border border-gray-300 text-gray-600 hover:bg-gray-50"
      >
        手動新增
      </button>

      {open && (
        <div className="fixed inset-0 bg-black/40 flex items-center justify-center z-50">
          <div className="bg-white rounded-xl shadow-lg p-6 w-full max-w-sm space-y-4">
            <h3 className="text-sm font-semibold text-gray-800">新增活動</h3>
            <form
              className="space-y-3"
              onSubmit={(e) => { e.preventDefault(); mutation.mutate() }}
            >
              <div>
                <label className="text-xs text-gray-500 mb-1 block">活動名稱 *</label>
                <input {...field('title')} placeholder="演唱會名稱" />
              </div>
              <div>
                <label className="text-xs text-gray-500 mb-1 block">開始時間 *</label>
                <input type="datetime-local" {...field('start_at')} />
              </div>
              <div>
                <label className="text-xs text-gray-500 mb-1 block">場地名稱 *</label>
                <input {...field('venue_name')} placeholder="Legacy Taipei" />
              </div>
              <div>
                <label className="text-xs text-gray-500 mb-1 block">城市 *</label>
                <input {...field('venue_city')} placeholder="台北市" />
              </div>
              {mutation.isError && (
                <p className="text-xs text-red-500">新增失敗，請確認欄位正確</p>
              )}
              <div className="flex gap-2 pt-1">
                <button
                  type="submit"
                  disabled={mutation.isPending || !canSubmit}
                  className="flex-1 text-sm py-1.5 rounded bg-gray-800 text-white hover:bg-gray-700 disabled:opacity-40"
                >
                  {mutation.isPending ? '新增中...' : '確認新增'}
                </button>
                <button
                  type="button"
                  onClick={() => { setOpen(false); setForm(EMPTY_FORM) }}
                  className="flex-1 text-sm py-1.5 rounded border border-gray-200 text-gray-600 hover:bg-gray-50"
                >
                  取消
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </>
  )
}

function ManualScrapeButton({ provider }: { provider: string }) {
  const queryClient = useQueryClient()
  const mutation = useMutation({
    mutationFn: () => api.post(`/admin/scrape/${provider}`),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['admin', 'health'] }),
  })

  return (
    <button
      onClick={() => mutation.mutate()}
      disabled={mutation.isPending}
      className={`text-xs px-2 py-0.5 rounded border ${mutation.isPending ? 'border-gray-300 text-gray-500' : 'border-gray-300 text-gray-600 hover:bg-gray-50'}`}
    >
      {mutation.isPending ? '執行中...' : '手動執行'}
    </button>
  )
}

function PasswordHashGenerator() {
  const [password, setPassword] = useState('')
  const [hash, setHash] = useState('')
  const [loading, setLoading] = useState(false)
  const [copied, setCopied] = useState(false)

  async function generate() {
    if (!password) return
    setLoading(true)
    setHash('')
    const result = await bcrypt.hash(password, 12)
    setHash(result)
    setLoading(false)
  }

  async function copy() {
    await navigator.clipboard.writeText(hash)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  return (
    <div className="rounded-xl border border-gray-200 p-4 space-y-3">
      <p className="text-sm font-medium text-gray-700">產生密碼 Hash</p>
      <div className="flex gap-2">
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && generate()}
          placeholder="輸入新密碼"
          className="flex-1 border border-gray-200 rounded px-2 py-1.5 text-sm focus:outline-none focus:border-gray-400"
        />
        <button
          onClick={generate}
          disabled={loading || !password}
          className="text-xs px-3 py-1.5 rounded bg-gray-800 text-white hover:bg-gray-700 disabled:opacity-40"
        >
          {loading ? '計算中...' : '產生'}
        </button>
      </div>
      {hash && (
        <div className="flex items-center gap-2">
          <code className="flex-1 text-xs bg-gray-50 border border-gray-200 rounded px-2 py-1.5 break-all text-gray-700 select-all">
            {hash}
          </code>
          <button
            onClick={copy}
            className="shrink-0 text-xs px-2 py-1.5 rounded border border-gray-200 text-gray-600 hover:bg-gray-50"
          >
            {copied ? '已複製' : '複製'}
          </button>
        </div>
      )}
      <p className="text-xs text-gray-400">產生後複製並貼入 backend/.env 的 ADMIN_PASSWORD_HASH</p>
    </div>
  )
}

function HealthCard({ health }: { health: AdminHealthResponse }) {
  const isOk = !health.has_warning && health.run_at !== null

  return (
    <div className={`rounded-xl border p-4 ${isOk ? 'border-green-200 bg-green-50' : 'border-red-200 bg-red-50'}`}>
      <div className="flex items-center justify-between">
        <span className="text-sm font-medium text-gray-700">爬蟲狀態 · {health.provider}</span>
        <span className={`text-xs font-medium px-2 py-0.5 rounded-full ${isOk ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`}>
          {health.has_warning ? '異常' : health.run_at ? '正常' : '未執行'}
        </span>
        <span>
          <ManualScrapeButton provider={health.provider} />
        </span>
      </div>
      <div className="mt-2 text-xs text-gray-500 space-y-0.5">
        <p>上次執行：{health.run_at ? new Date(health.run_at).toLocaleString('zh-TW') : '—'}</p>
        <p>寫入活動數：{health.events_count ?? '—'}</p>
      </div>
    </div>
  )
}

function EventRow({ event, onToggle }: { event: Event; onToggle: (id: number, field: string, value: boolean) => void }) {
  const isPast = new Date(event.start_at) < new Date()

  return (
    <tr className={`border-t border-gray-100 text-sm ${event.is_hidden ? 'opacity-40' : ''}`}>
      <td className="py-2 pr-4 text-gray-800 max-w-xs truncate">
        {event.title}
        {isPast && <span className="ml-1 text-xs text-gray-400">（已結束）</span>}
      </td>
      <td className="py-2 pr-4 text-gray-500 whitespace-nowrap">
        {new Date(event.start_at).toLocaleDateString('zh-TW')}
      </td>
      <td className="py-2 pr-4 text-gray-500">{event.venue.name}</td>
      <td className="py-2 pr-4">
        <div className="flex gap-2">
          <button
            onClick={() => onToggle(event.id, 'is_hidden', !event.is_hidden)}
            className={`text-xs px-2 py-0.5 rounded border ${event.is_hidden ? 'border-gray-300 text-gray-500' : 'border-gray-300 text-gray-600 hover:bg-gray-50'}`}
          >
            {event.is_hidden ? '顯示' : '隱藏'}
          </button>
          <button
            onClick={() => onToggle(event.id, 'is_cancelled', !event.is_cancelled)}
            className={`text-xs px-2 py-0.5 rounded border ${event.is_cancelled ? 'border-red-300 text-red-500' : 'border-gray-300 text-gray-600 hover:bg-gray-50'}`}
          >
            {event.is_cancelled ? '取消下架' : '標記取消'}
          </button>
        </div>
      </td>
    </tr>
  )
}

export default function AdminDashboardPage() {
  const navigate = useNavigate()
  const queryClient = useQueryClient()

  const { data: health } = useQuery<AdminHealthResponse>({
    queryKey: ['admin', 'health'],
    queryFn: () => api.get('/admin/health').then((r) => r.data),
  })

  const { data: eventsData } = useQuery<EventListResponse>({
    queryKey: ['admin', 'events'],
    queryFn: () => api.get('/admin/events').then((r) => r.data),
  })

  const patchMutation = useMutation({
    mutationFn: ({ id, field, value }: { id: number; field: string; value: boolean }) =>
      api.patch(`/admin/events/${id}`, { [field]: value }),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['admin', 'events'] }),
  })

  function handleLogout() {
    localStorage.removeItem('admin_token')
    navigate('/admin/login')
  }

  return (
    <div className="max-w-5xl mx-auto px-4 py-8 space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-base font-semibold text-gray-800">管理員儀表板</h1>
        <button onClick={handleLogout} className="text-xs text-gray-400 hover:text-gray-600">
          登出
        </button>
      </div>

      {health && <HealthCard health={health} />}

      <PasswordHashGenerator />

      <div>
        <h2 className="text-sm font-medium text-gray-700 mb-3">
          活動管理
          {eventsData && <span className="ml-2 text-gray-400 font-normal">（共 {eventsData.total} 筆）</span>}
          <ManualAddEventButton />
        </h2>

        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="text-xs text-gray-400 text-left">
                <th className="pb-2 pr-4 font-medium">活動名稱</th>
                <th className="pb-2 pr-4 font-medium">日期</th>
                <th className="pb-2 pr-4 font-medium">場地</th>
                <th className="pb-2 font-medium">操作</th>
              </tr>
            </thead>
            <tbody>
              {eventsData?.items.map((event) => (
                <EventRow
                  key={event.id}
                  event={event}
                  onToggle={(id, field, value) => patchMutation.mutate({ id, field, value })}
                />
              ))}
              {eventsData?.total === 0 && (
                <tr>
                  <td colSpan={4} className="py-8 text-center text-sm text-gray-400">
                    尚無活動資料
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}
