import React from 'react'

interface FallbackDiagramProps {
  diagramCode: string
}

const FallbackDiagram: React.FC<FallbackDiagramProps> = ({ diagramCode }) => {
  // Parse simple Mermaid graph TD syntax for fallback rendering
  const parseSimpleDiagram = (code: string) => {
    const lines = code.split('\n').map(line => line.trim()).filter(line => line)
    const nodes: string[] = []
    const edges: { from: string, to: string, label?: string }[] = []

    lines.forEach(line => {
      if (line.startsWith('graph') || line.startsWith('subgraph') || line.includes('end')) {
        return
      }
      
      // Parse node definitions like "A[Label]" or "DB[(Database)]"
      const nodeMatch = line.match(/(\w+)\[(.*?)\]|\w+\(\((.*?)\)\)/g)
      if (nodeMatch) {
        nodeMatch.forEach(match => {
          const nodeId = match.split('[')[0].split('((')[0]
          if (!nodes.includes(nodeId)) {
            nodes.push(nodeId)
          }
        })
      }

      // Parse edges like "A --> B"
      const edgeMatch = line.match(/(\w+)\s*-->\s*(\w+)/)
      if (edgeMatch) {
        edges.push({
          from: edgeMatch[1],
          to: edgeMatch[2]
        })
      }
    })

    return { nodes, edges }
  }

  const { nodes, edges } = parseSimpleDiagram(diagramCode)

  return (
    <div className="fallback-diagram">
      <div className="fallback-diagram-info">
        <p>Simplified Diagram View</p>
        <small>Mermaid rendering unavailable - showing simplified version</small>
      </div>
      <div className="fallback-nodes">
        {nodes.map((node) => (
          <div key={node} className="fallback-node" data-node={node}>
            {node}
            {edges.filter(edge => edge.from === node).map((edge, edgeIndex) => (
              <div key={edgeIndex} className="fallback-edge">
                → {edge.to}
              </div>
            ))}
          </div>
        ))}
      </div>
      <details className="fallback-diagram-code">
        <summary>View Original Diagram Code</summary>
        <pre><code>{diagramCode}</code></pre>
      </details>
    </div>
  )
}

export default FallbackDiagram