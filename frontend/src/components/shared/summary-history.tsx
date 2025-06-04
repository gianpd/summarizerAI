'use client'

import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Calendar, ExternalLink, Search, Trash2 } from 'lucide-react'
import api from '@/lib/api'
import type { SummaryResponse } from '@/types'

interface SummaryHistoryProps {
  refreshTrigger: number
  onSummarySelect: (summary: SummaryResponse) => void
}

export function SummaryHistory({ refreshTrigger, onSummarySelect }: SummaryHistoryProps) {
  const [summaries, setSummaries] = useState<SummaryResponse[]>([])
  const [filteredSummaries, setFilteredSummaries] = useState<SummaryResponse[]>([])
  const [searchTerm, setSearchTerm] = useState('')
  const [isLoading, setIsLoading] = useState(true)

  const fetchSummaries = async () => {
    try {
      setIsLoading(true)
      const response = await api.get<SummaryResponse[]>('/api/v1/summaries/')
      setSummaries(response.data)
      setFilteredSummaries(response.data)
    } catch (error) {
      console.error('Error fetching summaries:', error)
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    fetchSummaries()
  }, [refreshTrigger])

  useEffect(() => {
    const filtered = summaries.filter(summary =>
      (summary.key_top?.toLowerCase().includes(searchTerm.toLowerCase()) ?? false) ||
      (summary.summary?.toLowerCase().includes(searchTerm.toLowerCase()) ?? false)
    )
    setFilteredSummaries(filtered)
  }, [searchTerm, summaries])

  const deleteSummary = async (id: number) => {
    try {
      await api.delete(`/api/v1/summaries/${id}`)
      setSummaries(prev => prev.filter(s => s.id !== id))
    } catch (error) {
      console.error('Error deleting summary:', error)
    }
  }

  if (isLoading) {
    return (
      <div className="text-center py-12">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
        <p className="text-gray-500 mt-4">Loading summaries...</p>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center space-x-4">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
          <Input
            placeholder="Search summaries..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="pl-10"
          />
        </div>
        <Button onClick={fetchSummaries} variant="outline">
          Refresh
        </Button>
      </div>

      {filteredSummaries.length === 0 ? (
        <div className="text-center py-12">
          <div className="text-gray-500 mb-4">
            <svg
              className="mx-auto h-12 w-12"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
              />
            </svg>
          </div>
          <h3 className="text-lg font-medium text-gray-900 mb-2">
            {searchTerm ? 'No matching summaries' : 'No summaries yet'}
          </h3>
          <p className="text-gray-500">
            {searchTerm 
              ? 'Try adjusting your search terms.'
              : 'Create your first summary to get started.'
            }
          </p>
        </div>
      ) : (
        <div className="grid gap-4">
          {filteredSummaries.map((summary) => (
            <Card key={summary.id} className="hover:shadow-md transition-shadow">
              <CardHeader className="pb-3">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <CardTitle className="text-lg">{summary.key_top || 'Untitled'}</CardTitle>
                    <CardDescription className="flex items-center mt-1">
                      <Calendar className="h-4 w-4 mr-1" />
                      {new Date(summary.created_at).toLocaleDateString()}
                      {summary.url && (
                        <a
                          href={summary.url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="ml-4 flex items-center text-blue-600 hover:text-blue-800"
                        >
                          <ExternalLink className="h-4 w-4 mr-1" />
                          Source
                        </a>
                      )}
                    </CardDescription>
                  </div>
                  <div className="flex items-center space-x-2">
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => onSummarySelect(summary)}
                    >
                      View
                    </Button>
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => deleteSummary(summary.id)}
                      className="text-red-600 hover:text-red-800"
                    >
                      <Trash2 className="h-4 w-4" />
                    </Button>
                  </div>
                </div>
              </CardHeader>
              <CardContent className="pt-0">
                <p className="text-gray-600 text-sm line-clamp-3">
                  {summary.summary || 'No summary available'}
                </p>
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  )
}