export interface ArchitectureRecommendationResponse {
  selectedArchitecture: string
  explanation: string
  diagramCode: string
}

export interface PDFExportOptions {
  recommendation: ArchitectureRecommendationResponse
  userContext: string
}