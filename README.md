# Architecture Recommendation Agent 🏗️

An AI-powered architecture recommendation system that uses **Retrieval-Augmented Generation (RAG)** with Google Gemini and vector embeddings to provide intelligent software architecture recommendations with automatically generated Mermaid diagrams.

## 🎯 What It Does

Give it your project requirements (team size, scale, budget, timeline, technical constraints), and it will:

- 🤖 **Analyze** your context using AI
- 🔍 **Retrieve** relevant architecture patterns from a knowledge base of 23+ patterns
- 💡 **Recommend** the best architecture (or combination of architectures)
- 📝 **Explain** detailed reasoning for each recommendation
- 📊 **Generate** Mermaid diagrams showing the complete solution

## ✨ Key Features

- **Intelligent Recommendations**: Supports both single architectures (for simple projects) and heterogeneous architectures (combinations for complex systems)
- **Detailed Reasoning**: Each architecture choice comes with specific justification referencing your requirements
- **23+ Architecture Patterns**: Monolithic, Microservices, Event-Driven, Serverless, Layered, MVC, Pipe-and-Filter, Repository, and many more
- **Visual Diagrams**: Auto-generated Mermaid.js diagrams showing architecture components and data flow
- **RAG Pipeline**: Semantic search finds relevant patterns, AI generates contextual recommendations
- **Centralized Configuration**: Single place to manage all settings (`app/config.py`)

## 🏗️ Architecture Patterns Included

**Modern Patterns:**

- Monolithic, Microservices, Serverless, Event-Driven

**Structural Patterns:**

- Layered, Object-Oriented, Main Program and Subroutines

**Data Flow Patterns:**

- Pipe-and-Filter, Batch Sequential

**Data-Centered Patterns:**

- Repository, Blackboard

**Communication Patterns:**

- Client-Server, Peer-to-Peer, Publish-Subscribe, Implicit Invocation

**Presentation Patterns:**

- Model-View-Controller (MVC), State-Logic-Display (Three-Tiered)

**Control Patterns:**

- Sense-Compute-Control, Behavior-Based Approach, Process Control Systems

**Interpreter Patterns:**

- Interpreter, Rule-Based, Mobile-Code

**Meta Patterns:**

- Heterogeneous (combinations of multiple patterns)

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Google API Key (for Gemini API)
- Git

### Installation

1. **Clone the repository:**

```powershell
git clone https://github.com/SurajaHasarinda/architecture-recommender-workbench
cd "architecture-recommender-workbench"
```

2. **Set up environment variables:**

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_google_gemini_api_key_here
```

> 💡 Get your Google API key from: https://makersuite.google.com/app/apikey

3. **Run the setup and run script:**

```powershell
.\start.ps1
```

The API will be available at `http://localhost:8000`

## 🧪 Testing

### Using Swagger UI (Recommended)

Open your browser and go to:

```
http://localhost:8000/docs
```

### Using test_api.py

Run the test script:

```powershell
python test_api.py
```
