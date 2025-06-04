'use client'

import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import * as z from 'zod'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Textarea } from '@/components/ui/textarea'
import { Label } from '@/components/ui/label'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Card, CardContent } from '@/components/ui/card'
import { Loader2, Link, FileText } from 'lucide-react'
import api from '@/lib/api'
import type { SummaryCreate, SummaryResponse } from '@/types'

const urlSchema = z.object({
  url: z.string().url('Please enter a valid URL'),
})

const textSchema = z.object({
  text: z.string().min(10, 'Content must be at least 10 characters'),
})

type UrlFormData = z.infer<typeof urlSchema>
type TextFormData = z.infer<typeof textSchema>

interface SummaryFormProps {
  onSummaryCreated: (summary: SummaryResponse) => void
}

export function SummaryForm({ onSummaryCreated }: SummaryFormProps) {
  const [isLoading, setIsLoading] = useState(false)
  const [activeTab, setActiveTab] = useState('url')

  const urlForm = useForm<UrlFormData>({
    resolver: zodResolver(urlSchema),
    defaultValues: {
      url: '',
    },
  })

  const textForm = useForm<TextFormData>({
    resolver: zodResolver(textSchema),
    defaultValues: {
      text: '',
    },
  })

  const onUrlSubmit = async (data: UrlFormData) => {
    setIsLoading(true)
    try {
      const payload: SummaryCreate = {
        url: data.url,
      }
      const response = await api.post<SummaryResponse>('/api/v1/summaries/', payload)
      onSummaryCreated(response.data)
      urlForm.reset()
    } catch (error: any) {
      console.error('Error creating summary:', error)
      // Handle error (show toast, etc.)
    } finally {
      setIsLoading(false)
    }
  }

  const onTextSubmit = async (data: TextFormData) => {
    setIsLoading(true)
    try {
      const payload = {
        text: data.text,
      }
      const response = await api.post('/api/v1/summaries/text', payload)
      // Convert text summary response to match SummaryResponse format
      const summaryResponse: SummaryResponse = {
        id: Date.now(), // Temporary ID since text summaries aren't stored
        summary: response.data.summary,
        key_top: 'Text Summary',
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
      }
      onSummaryCreated(summaryResponse)
      textForm.reset()
    } catch (error: any) {
      console.error('Error creating summary:', error)
      // Handle error (show toast, etc.)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
      <TabsList className="grid w-full grid-cols-2">
        <TabsTrigger value="url" className="flex items-center gap-2">
          <Link className="h-4 w-4" />
          URL
        </TabsTrigger>
        <TabsTrigger value="text" className="flex items-center gap-2">
          <FileText className="h-4 w-4" />
          Text
        </TabsTrigger>
      </TabsList>

      <TabsContent value="url" className="mt-6">
        <Card>
          <CardContent className="pt-6">
            <form onSubmit={urlForm.handleSubmit(onUrlSubmit)} className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="url">URL</Label>
                <Input
                  id="url"
                  type="url"
                  placeholder="https://example.com/article"
                  {...urlForm.register('url')}
                />
                {urlForm.formState.errors.url && (
                  <p className="text-sm text-red-500">
                    {urlForm.formState.errors.url.message}
                  </p>
                )}
              </div>

              <Button type="submit" disabled={isLoading} className="w-full">
                {isLoading ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Generating Summary...
                  </>
                ) : (
                  'Summarize URL'
                )}
              </Button>
            </form>
          </CardContent>
        </Card>
      </TabsContent>

      <TabsContent value="text" className="mt-6">
        <Card>
          <CardContent className="pt-6">
            <form onSubmit={textForm.handleSubmit(onTextSubmit)} className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="text">Text Content</Label>
                <Textarea
                  id="text"
                  placeholder="Paste your text content here..."
                  className="min-h-[200px]"
                  {...textForm.register('text')}
                />
                {textForm.formState.errors.text && (
                  <p className="text-sm text-red-500">
                    {textForm.formState.errors.text.message}
                  </p>
                )}
              </div>

              <Button type="submit" disabled={isLoading} className="w-full">
                {isLoading ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Generating Summary...
                  </>
                ) : (
                  'Summarize Text'
                )}
              </Button>
            </form>
          </CardContent>
        </Card>
      </TabsContent>
    </Tabs>
  )
}