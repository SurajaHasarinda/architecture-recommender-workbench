import os
import logging
from contextlib import asynccontextmanager
from typing import List, Dict, Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from app.config import settings
from app.models.schemas import ProjectContextRequest, ArchitectureRecommendationResponse
from app.services.vector_store import VectorStoreService
from app.services.gemini_service import GeminiService
from app.services.rag_service import RAGService

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global service instances
vector_store: VectorStoreService = None
gemini_service: GeminiService = None
rag_service: RAGService = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global vector_store, gemini_service, rag_service
    
    logger.info("Starting up the application...")
    
    # Validate environment variables
    api_key = settings.google_api_key
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable is not set")
    
    try:
        # Initialize services
        logger.info("Initializing Gemini service...")
        gemini_service = GeminiService(api_key=api_key)
        
        logger.info("Initializing Vector Store...")
        vector_store = VectorStoreService(
            persist_directory=settings.chroma_persist_directory,
            collection_name=settings.chroma_collection_name
        )
        
        # Load and index architecture documents
        logger.info("Loading architecture documents...")
        docs_dir = settings.docs_directory
        if not os.path.exists(docs_dir):
            logger.warning(f"Architecture docs directory not found: {docs_dir}")
            raise FileNotFoundError(f"Directory {docs_dir} does not exist")
        
        # Load documents and populate vector store
        from app.utils.document_loader import load_architecture_documents
        documents = load_architecture_documents(docs_dir)
        logger.info(f"Loaded {len(documents)} architecture documents")
        
        # Generate embeddings and store in ChromaDB
        vector_store.add_documents(documents, gemini_service)
        logger.info("Documents indexed successfully in ChromaDB")
        
        # Initialize RAG service
        rag_service = RAGService(
            vector_store=vector_store,
            gemini_service=gemini_service
        )
        
        logger.info("Application startup complete!")
        
    except Exception as e:
        logger.error(f"Error during startup: {str(e)}")
        raise
    
    yield  # Application runs here
    
    # Cleanup on shutdown
    logger.info("Shutting down the application...")


# Initialize FastAPI app with lifespan
app = FastAPI(
    title=settings.app_name,
    description="AI-powered architecture recommendation system using RAG",
    version=settings.app_version,
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=settings.cors_credentials,
    allow_methods=settings.cors_methods,
    allow_headers=settings.cors_headers,
)


@app.get("/")
async def root():
    return {
        "status": "healthy",
        "service": settings.app_name,
        "version": settings.app_version
    }


@app.post("/api/recommend-architecture", response_model=ArchitectureRecommendationResponse)
async def recommend_architecture(request: ProjectContextRequest):
    try:
        logger.info("Received architecture recommendation request")
        logger.debug(f"User context: {request.context[:100]}...")
        
        # Validate services are initialized
        if not rag_service:
            raise HTTPException(
                status_code=503,
                detail="RAG service not initialized. Please try again later."
            )
        
        # Get recommendation using RAG pipeline
        result = await rag_service.get_architecture_recommendation(request.context)
        
        logger.info(f"Successfully generated recommendation: {result['selectedArchitecture']}")
        return ArchitectureRecommendationResponse(**result)
        
    except Exception as e:
        logger.error(f"Error processing recommendation request: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Error generating recommendation: {str(e)}"
        )


@app.get("/api/health")
async def health_check():
    health_status = {
        "status": "healthy",
        "services": {
            "vector_store": vector_store is not None,
            "gemini_service": gemini_service is not None,
            "rag_service": rag_service is not None
        }
    }
    
    if not all(health_status["services"].values()):
        health_status["status"] = "degraded"
        
    return health_status


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
        log_level=settings.log_level.lower()
    )
