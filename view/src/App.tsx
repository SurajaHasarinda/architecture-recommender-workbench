import './App.css'
import ArchitectureRecommender from './components/ArchitectureRecommender'

function App() {
  return (
    <div className="app">
      <header className="app-header">
        <h1>Architecture Recommendation System</h1>
        <p>AI-powered architecture recommendations for enterprise projects</p>
      </header>
      <main className="app-main">
        <ArchitectureRecommender />
      </main>
    </div>
  )
}

export default App
