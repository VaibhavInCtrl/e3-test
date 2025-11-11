import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { ExternalLink } from 'lucide-react'
import { Button } from '@/components/ui/button'

interface StructuredDataDisplayProps {
  structuredData: Record<string, any> | null
  recordingUrl?: string | null
  durationMs?: number | null
}

function formatKey(key: string): string {
  return key
    .split('_')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ')
}

function formatValue(value: any): string {
  if (value === null || value === undefined) {
    return 'N/A'
  }
  if (typeof value === 'boolean') {
    return value ? 'Yes' : 'No'
  }
  if (typeof value === 'object') {
    return JSON.stringify(value, null, 2)
  }
  return String(value)
}

function formatDuration(ms: number): string {
  const seconds = Math.floor(ms / 1000)
  const minutes = Math.floor(seconds / 60)
  const remainingSeconds = seconds % 60
  return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`
}

export function StructuredDataDisplay({ structuredData, recordingUrl, durationMs }: StructuredDataDisplayProps) {
  if (!structuredData || Object.keys(structuredData).length === 0) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Extracted Information</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-center text-muted-foreground py-4">
            No structured data available yet
          </p>
        </CardContent>
      </Card>
    )
  }

  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between space-y-0">
        <CardTitle>Extracted Information</CardTitle>
        {recordingUrl && (
          <Button variant="outline" size="sm" asChild>
            <a href={recordingUrl} target="_blank" rel="noopener noreferrer">
              <ExternalLink className="mr-2 h-4 w-4" />
              Recording
            </a>
          </Button>
        )}
      </CardHeader>
      <CardContent className="space-y-4">
        {durationMs && (
          <div className="flex items-center gap-2 text-sm text-muted-foreground">
            <span>Duration: {formatDuration(durationMs)}</span>
          </div>
        )}
        
        <div className="space-y-3">
          {Object.entries(structuredData).map(([key, value]) => (
            <div key={key} className="grid grid-cols-3 gap-4 py-2 border-b last:border-0">
              <dt className="text-sm font-medium text-muted-foreground">
                {formatKey(key)}
              </dt>
              <dd className="col-span-2 text-sm font-medium">
                {typeof value === 'boolean' ? (
                  <Badge variant={value ? 'default' : 'secondary'}>
                    {formatValue(value)}
                  </Badge>
                ) : (
                  <span>{formatValue(value)}</span>
                )}
              </dd>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  )
}

