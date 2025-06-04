'use client'

import { useState } from 'react'
import { SummaryForm } from '@/components/shared/summary-form'
import { SummaryResult } from '@/components/shared/summary-result'
import { SummaryHistory } from '@/components/shared/summary-history'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Brain, FileText, History } from 'lucide-react'
import type { SummaryResponse } from '@/types'

export default function HomePage() {
  const [currentSummary, setCurrentSummary] = useState<SummaryResponse | null>(null)
  const [refreshHistory, setRefreshHistory] = useState(0)

  const handleSummaryCreated = (summary: SummaryResponse) => {
    setCurrentSummary(summary)
    setRefreshHistory(prev => prev + 1)
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="text-center mb-8">
        <div className="flex items-center justify-center mb-4">
          <Brain className="h-12 w-12 text-blue-600 mr-3" />
          <h1 className="text-4xl font-bold text-gray-900">SummarizerAI</h1>
        </div>
        <p className="text-xl text-gray-600 max-w-2xl mx-auto">
          Transform long articles and texts into concise, meaningful summaries using advanced AI technology
        </p>
      </div>

      <div className="max-w-6xl mx-auto">
        <Tabs defaultValue="summarize" className="w-full">
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="summarize" className="flex items-center gap-2">
              <FileText className="h-4 w-4" />
              Summarize
            </TabsTrigger>
            <TabsTrigger value="result" className="flex items-center gap-2">
              <Brain className="h-4 w-4" />
              Result
            </TabsTrigger>
            <TabsTrigger value="history" className="flex items-center gap-2">
              <History className="h-4 w-4" />
              History
            </TabsTrigger>
          </TabsList>

          <TabsContent value="summarize" className="mt-6">
            <Card>
              <CardHeader>
                <CardTitle>Create Summary</CardTitle>
                <CardDescription>
                  Enter a URL or paste text to generate an AI-powered summary
                </CardDescription>
              </CardHeader>
              <CardContent>
                <SummaryForm onSummaryCreated={handleSummaryCreated} />
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="result" className="mt-6">
            <Card>
              <CardHeader>
                <CardTitle>Summary Result</CardTitle>
                <CardDescription>
                  View your generated summary and key insights
                </CardDescription>
              </CardHeader>
              <CardContent>
                <SummaryResult summary={currentSummary} />
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="history" className="mt-6">
            <Card>
              <CardHeader>
                <CardTitle>Summary History</CardTitle>
                <CardDescription>
                  Browse your previously generated summaries
                </CardDescription>
              </CardHeader>
              <CardContent>
                <SummaryHistory
                  refreshTrigger={refreshHistory}
                  onSummarySelect={setCurrentSummary}
                />
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  )
}