import { useState, useRef, useEffect } from 'react'
import { Send, Loader2, Download, RefreshCw } from 'lucide-react'
import MermaidDiagram from './MermaidDiagram'
import PDFExporter from './PDFExporter'
import type { ArchitectureRecommendationResponse } from '../types'
import './ArchitectureRecommender.css'

const ArchitectureRecommender = () => {
  const [context, setContext] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [recommendation, setRecommendation] = useState<ArchitectureRecommendationResponse | null>(null)
  const [error, setError] = useState<string | null>(null)
  const textareaRef = useRef<HTMLTextAreaElement>(null)

  // Auto-resize textarea
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto'
      textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`
    }
  }, [context])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!context.trim()) return

    setIsLoading(true)
    setError(null)

    try {
      const response = await fetch('http://localhost:8000/api/recommend-architecture', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ context: context.trim() }),
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const data: ArchitectureRecommendationResponse = await response.json()
      setRecommendation(data)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred')
      console.error('Error:', err)
    } finally {
      setIsLoading(false)
    }
  }

  const handleReset = () => {
    setContext('')
    setRecommendation(null)
    setError(null)
  }

  const handleExportDiagram = async () => {
    if (!recommendation) return
    
    try {
      setIsLoading(true)
      await PDFExporter.exportToPDF({
        recommendation,
        userContext: context
      })
    } catch (error) {
      console.error('Error exporting PDF:', error)
      setError('Failed to export PDF. Please try again.')
    } finally {
      setIsLoading(false)
    }
  }



  return (
    <div className="architecture-recommender">
      <div className="input-section">
        <form onSubmit={handleSubmit} className="context-form">
          <div className="form-group">
            <label htmlFor="context" className="form-label">
              Project Context Description
            </label>
            <div className="textarea-container">
              <textarea
                ref={textareaRef}
                id="context"
                value={context}
                onChange={(e) => setContext(e.target.value)}
                placeholder="Describe your project requirements, team size, timeline, budget constraints, expected user load, and any specific technical requirements..."
                className="context-textarea"
                rows={4}
                disabled={isLoading}
                minLength={10}
                required
              />
              <div className="character-count">
                {context.length} characters
              </div>
            </div>
          </div>
          
          <div className="form-actions">
            <button
              type="button"
              onClick={handleReset}
              className="reset-btn"
              disabled={isLoading || (!context && !recommendation)}
            >
              <RefreshCw size={16} />
              Reset
            </button>
            <button
              type="submit"
              disabled={isLoading || !context.trim()}
              className="submit-btn"
            >
              {isLoading ? (
                <>
                  <Loader2 size={16} className="animate-spin" />
                  Analyzing...
                </>
              ) : (
                <>
                  <Send size={16} />
                  Get Recommendation
                </>
              )}
            </button>
          </div>
        </form>
      </div>

      {error && (
        <div className="error-message">
          <div className="error-content">
            <strong>Error:</strong> {error}
            <button 
              onClick={() => setError(null)}
              className="error-close"
              aria-label="Close error"
            >
              ×
            </button>
          </div>
        </div>
      )}

      {recommendation && (
        <div className="recommendation-section">
          <div className="recommendation-header">
            <h2>Recommended Architecture</h2>
            <button
              onClick={handleExportDiagram}
              className="export-btn"
              title="Export as Professional PDF Report"
              disabled={isLoading}
            >
              <Download size={16} />
              Export PDF
            </button>
          </div>

          <div className="architecture-title">
            <h3>{recommendation.selectedArchitecture}</h3>
          </div>

          <div className="explanation-section">
            <h4>Analysis & Reasoning</h4>
            <p>{recommendation.explanation}</p>
          </div>

          <div className="diagram-section">
            <div className="diagram-header">
              <h4>Architecture Diagram</h4>
              <div className="diagram-controls">
                <button
                  type="button"
                  className="zoom-btn"
                  onClick={() => {
                    const container = document.querySelector('.mermaid-diagram svg') as SVGElement
                    if (container) {
                      const currentScale = container.style.transform?.match(/scale\(([\d.]+)\)/)?.[1] || '0.85'
                      const newScale = Math.min(parseFloat(currentScale) + 0.1, 1.2)
                      container.style.transform = `scale(${newScale})`
                    }
                  }}
                  title="Zoom In"
                >
                  +
                </button>
                <button
                  type="button"
                  className="zoom-btn"
                  onClick={() => {
                    const container = document.querySelector('.mermaid-diagram svg') as SVGElement
                    if (container) {
                      const currentScale = container.style.transform?.match(/scale\(([\d.]+)\)/)?.[1] || '0.85'
                      const newScale = Math.max(parseFloat(currentScale) - 0.1, 0.4)
                      container.style.transform = `scale(${newScale})`
                    }
                  }}
                  title="Zoom Out"
                >
                  -
                </button>
                <button
                  type="button"
                  className="zoom-btn"
                  onClick={() => {
                    const container = document.querySelector('.mermaid-diagram svg') as SVGElement
                    if (container) {
                      container.style.transform = 'scale(0.85)'
                    }
                  }}
                  title="Reset Zoom"
                >
                  ↻
                </button>
              </div>
            </div>
            <div className="diagram-container">
              <MermaidDiagram diagramCode={recommendation.diagramCode} />
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default ArchitectureRecommender