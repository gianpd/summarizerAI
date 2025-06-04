'use client'

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Copy, ExternalLink, Calendar } from 'lucide-react'
import type { SummaryResponse } from '@/types'

interface SummaryResultProps {
  summary: SummaryResponse | null
}

export function SummaryResult({ summary }: SummaryResultProps) {
  const copyToClipboard = async (text: string) => {
    try {
      await navigator.clipboard.writeText(text)
      // Show success toast
    } catch (error) {
      console.error('Failed to copy text:', error)
    }
  }

  if (!summary) {
    return (
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
        <h3 className="text-lg font-medium text-gray-900 mb-2">No Summary Selected</h3>
        <p className="text-gray-500">
          Create a new summary or select one from your history to view it here.
        </p>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <h2 className="text-2xl font-bold text-gray-900 mb-2">{summary.key_top || 'Untitled'}</h2>
          <div className="flex items-center text-sm text-gray-500 space-x-4">
            <div className="flex items-center">
              <Calendar className="h-4 w-4 mr-1" />
              {new Date(summary.created_at).toLocaleDateString()}
            </div>
            {summary.url && (
              <a
                href={summary.url}
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center text-blue-600 hover:text-blue-800"
              >
                <ExternalLink className="h-4 w-4 mr-1" />
                View Original
              </a>
            )}
          </div>
        </div>
        <Button
          variant="outline"
          size="sm"
          onClick={() => copyToClipboard(summary.summary || '')}
        >
          <Copy className="h-4 w-4 mr-2" />
          Copy Summary
        </Button>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Summary</CardTitle>
          <CardDescription>
            AI-generated summary of the content
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="prose max-w-none">
            <p className="text-gray-700 leading-relaxed whitespace-pre-wrap">
              {summary.summary || 'No summary available'}
            </p>
          </div>
        </CardContent>
      </Card>

      {summary.keywords && (
        <Card>
          <CardHeader>
            <CardTitle>Keywords</CardTitle>
            <CardDescription>
              Key terms extracted from the content
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="prose max-w-none">
              <p className="text-gray-600 text-sm leading-relaxed">
                {summary.keywords}
              </p>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  )
}