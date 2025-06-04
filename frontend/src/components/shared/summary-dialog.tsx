'use client'

import { Button } from '@/components/ui/button'
import { 
  Dialog, 
  DialogContent, 
  DialogDescription, 
  DialogHeader, 
  DialogTitle, 
  DialogTrigger 
} from '@/components/ui/dialog'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Copy, ExternalLink, Calendar, Eye } from 'lucide-react'
import type { SummaryResponse } from '@/types'

interface SummaryDialogProps {
  summary: SummaryResponse
  trigger?: React.ReactNode
}

export function SummaryDialog({ summary, trigger }: SummaryDialogProps) {
  const copyToClipboard = async (text: string) => {
    try {
      await navigator.clipboard.writeText(text)
      // You could add a toast notification here
    } catch (error) {
      console.error('Failed to copy text:', error)
    }
  }

  const defaultTrigger = (
    <Button variant="outline" size="sm">
      <Eye className="h-4 w-4 mr-1" />
      View
    </Button>
  )

  return (
    <Dialog>
      <DialogTrigger asChild>
        {trigger || defaultTrigger}
      </DialogTrigger>
      <DialogContent className="max-w-4xl max-h-[80vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle className="text-xl">{summary.key_top || 'Untitled'}</DialogTitle>
          <DialogDescription className="flex items-center text-sm text-gray-500 space-x-4">
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
          </DialogDescription>
        </DialogHeader>
        
        <div className="space-y-6">
          <div className="flex justify-end">
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
      </DialogContent>
    </Dialog>
  )
}