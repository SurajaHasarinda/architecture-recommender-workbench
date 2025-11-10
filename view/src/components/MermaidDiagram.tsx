import { useEffect, useRef, useState } from 'react'
import mermaid from 'mermaid'
import FallbackDiagram from './FallbackDiagram'

interface MermaidDiagramProps {
  diagramCode: string
}

const MermaidDiagram = ({ diagramCode }: MermaidDiagramProps) => {
  const diagramRef = useRef<HTMLDivElement>(null)
  const [isInitialized, setIsInitialized] = useState(false)
  const [renderFailed, setRenderFailed] = useState(false)

  // Initialize Mermaid once
  useEffect(() => {
    if (!isInitialized) {
      mermaid.initialize({
        startOnLoad: false,
        theme: 'base',
        securityLevel: 'loose',
        themeVariables: {
          primaryColor: '#ffffff',
          primaryTextColor: '#000000',
          primaryBorderColor: '#000000',
          lineColor: '#000000',
          secondaryColor: '#f8f9fa',
          tertiaryColor: '#ffffff',
          background: '#ffffff',
          mainBkg: '#ffffff',
          secondBkg: '#f8f9fa',
          tertiaryBkg: '#e9ecef',
          fontSize: '14px',
          fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
          // Ensure solid white background
          backgroundColorPrimary: '#ffffff',
          backgroundColorSecondary: '#f8f9fa',
          // Node colors - solid white with black borders
          nodeBkg: '#ffffff',
          nodeBorder: '#000000',
          clusterBkg: '#f8f9fa',
          clusterBorder: '#000000',
          // Text colors - all black
          textColor: '#000000',
          titleColor: '#000000',
          nodeTextColor: '#000000',
          // Edge colors - all black
          edgeLabelBackground: '#ffffff',
          edgeLabelColor: '#000000',
          // Force all lines to be black
          cScale0: '#000000',
          cScale1: '#000000',
          cScale2: '#000000',
          // Additional black and white theme variables
          actorBkg: '#ffffff',
          actorBorder: '#000000',
          actorTextColor: '#000000',
          activationBkg: '#f8f9fa',
          activationBorderColor: '#000000',
          sectionBkg: '#ffffff',
          altSectionBkg: '#f8f9fa',
          gridColor: '#000000',
          // Force pie chart colors to grayscale
          c0: '#ffffff',
          c1: '#f8f9fa',
          c2: '#e9ecef',
          c3: '#dee2e6',
          c4: '#ced4da',
          c5: '#adb5bd',
          c6: '#6c757d',
          c7: '#495057',
          pie1: '#ffffff',
          pie2: '#f1f3f4',
          pie3: '#e8eaed',
          pie4: '#dadce0',
          pie5: '#bdc1c6',
          pie6: '#9aa0a6',
          pie7: '#5f6368',
          pie8: '#3c4043',
          pie9: '#202124',
          pie10: '#000000',
          pie11: '#000000',
          pie12: '#000000',
          // Additional overrides to ensure black lines
          stroke: '#000000',
          fill: '#ffffff'
        },
        flowchart: {
          useMaxWidth: false,
          htmlLabels: false,
          curve: 'linear',
          nodeSpacing: 50,
          rankSpacing: 60,
          padding: 20,
        },
        er: {
          useMaxWidth: false,
        },
        sequence: {
          useMaxWidth: false,
        },
        gantt: {
          useMaxWidth: false,
        },
        journey: {
          useMaxWidth: false,
        },
        pie: {
          useMaxWidth: false,
        },
      })
      setIsInitialized(true)
    }
  }, [isInitialized])

  useEffect(() => {
    if (!diagramRef.current || !diagramCode || !isInitialized) return

    const renderDiagram = async () => {
      if (!diagramRef.current) return

      try {
        // Clear previous diagram
        diagramRef.current.innerHTML = 'Loading diagram...'

        // Generate unique ID for this diagram
        const id = `mermaid-diagram-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`

        // Validate and clean the diagram code
        const cleanDiagramCode = diagramCode.trim()
        console.log('Rendering Mermaid diagram:', cleanDiagramCode)

        // Use the modern Mermaid API
        const { svg, bindFunctions } = await mermaid.render(id, cleanDiagramCode)
        
        if (diagramRef.current) {
          diagramRef.current.innerHTML = svg
          
          // Bind any functions if needed
          if (bindFunctions) {
            bindFunctions(diagramRef.current)
          }

          // Add styling to the SVG and force black/white theme
          const svgElement = diagramRef.current.querySelector('svg')
          if (svgElement) {
            svgElement.style.width = '100%'
            svgElement.style.height = 'auto'
            svgElement.style.maxWidth = '100%'
            svgElement.style.display = 'block'
            svgElement.style.margin = '0 auto'
            svgElement.style.background = '#ffffff'
            svgElement.style.backgroundColor = '#ffffff'
            
            // Force all paths to be black
            const paths = svgElement.querySelectorAll('path')
            paths.forEach(path => {
              if (path.getAttribute('stroke') === 'white' || 
                  path.getAttribute('stroke') === '#ffffff' || 
                  path.getAttribute('stroke') === '#fff' ||
                  !path.getAttribute('stroke') ||
                  path.getAttribute('stroke') === 'transparent') {
                path.setAttribute('stroke', '#000000')
                path.style.stroke = '#000000'
              }
            })
            
            // Force all lines to be black
            const lines = svgElement.querySelectorAll('line')
            lines.forEach(line => {
              line.setAttribute('stroke', '#000000')
              line.style.stroke = '#000000'
            })
            
            // Force all polylines to be black
            const polylines = svgElement.querySelectorAll('polyline')
            polylines.forEach(polyline => {
              polyline.setAttribute('stroke', '#000000')
              polyline.style.stroke = '#000000'
            })
          }
        }
      } catch (error) {
        console.error('Mermaid rendering error:', error)
        setRenderFailed(true)
        if (diagramRef.current) {
          diagramRef.current.innerHTML = `
            <div class="diagram-error">
              <p>Error rendering diagram with Mermaid</p>
              <p style="font-size: 0.9rem; color: rgba(255, 150, 150, 0.7); margin-top: 0.5rem;">
                ${error instanceof Error ? error.message : 'Unknown error occurred'}
              </p>
              <details style="margin-top: 1rem;">
                <summary style="cursor: pointer; font-weight: 500; color: rgba(255, 255, 255, 0.8);">Show Diagram Code</summary>
                <pre style="background: rgba(0, 0, 0, 0.3); border: 1px solid rgba(255, 255, 255, 0.1); padding: 1rem; border-radius: 8px; overflow-x: auto; margin-top: 0.5rem;"><code style="color: rgba(255, 255, 255, 0.7);">${diagramCode}</code></pre>
              </details>
            </div>
          `
        }
      }
    }

    // Add a small delay to ensure DOM is ready
    const timeoutId = setTimeout(() => {
      renderDiagram()
    }, 100)

    return () => clearTimeout(timeoutId)
  }, [diagramCode, isInitialized])

  if (renderFailed) {
    return <FallbackDiagram diagramCode={diagramCode} />
  }

  return (
    <div className="mermaid-container">
      <div ref={diagramRef} className="mermaid-diagram" />
    </div>
  )
}

export default MermaidDiagram