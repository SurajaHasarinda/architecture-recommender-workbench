import logging
from typing import Dict, Any

from app.config import settings

logger = logging.getLogger(__name__)


class RAGService:    
    # System instruction for Gemini defining the AI's role and task
    SYSTEM_INSTRUCTION = """
        You are an expert software architect with deep knowledge of various software architecture patterns and their appropriate use cases.

        Your task is to:
        1. Analyze the user's project context carefully, considering factors like team size, budget, timeline, scalability needs, complexity, and technical constraints.
        2. Review the retrieved architecture documentation provided as context.
        3. Select EXACTLY ONE architecture that best fits the user's requirements.
        4. Provide a detailed, well-reasoned explanation for your choice, addressing specific aspects of the user's context.
        5. Generate Mermaid.js diagram code using `graph TD` (top-down graph) syntax that visually represents the selected architecture.

        STRICT RULES FOR MERMAID DIAGRAM CODE:
        - Use ONLY `graph TD` syntax (not flowchart, class diagram, or any other type)
        - Base the diagram structure on the KeyComponents mentioned in the architecture description
        - Create clear, hierarchical node relationships showing how components interact
        - Use descriptive node labels (e.g., "User Interface", "API Gateway", "Database")
        - Include arrows showing data/request flow between components
        - Keep the diagram clean and focused (5-12 nodes typically)
        - Use appropriate node shapes: rectangles for services/layers, cylinders for databases [(Database)], etc.
        - Ensure the diagram is syntactically correct and will render properly

        Example Mermaid format:
        graph TD
            A[Component Name] --> B[Another Component]
            B --> C[(Database)]
            
        Remember: Generate NEW, APPROPRIATE diagram code based on the selected architecture - do NOT copy pre-existing diagram code.
        """
    
    def __init__(self, vector_store, gemini_service):
        self.vector_store = vector_store
        self.gemini_service = gemini_service
        logger.info("RAG service initialized")
    
    async def get_architecture_recommendation(self, user_context: str, top_k: int = None) -> Dict[str, Any]:
        if top_k is None:
            top_k = settings.top_k_results
            
        try:
            logger.info("Starting RAG pipeline...")
            
            # Step 1: Generate embedding for user's context (query)
            logger.info("Generating query embedding...")
            query_embedding = self.gemini_service.generate_query_embedding(user_context)
            
            # Step 2: Retrieve relevant documents from vector store
            logger.info(f"Retrieving top {top_k} relevant documents from ChromaDB...")
            retrieval_results = self.vector_store.query(
                query_embedding=query_embedding,
                n_results=top_k
            )
            
            retrieved_documents = retrieval_results['documents']
            logger.info(f"Retrieved {len(retrieved_documents)} documents")
            
            # Log retrieval quality (distances)
            if retrieval_results['distances']:
                avg_distance = sum(retrieval_results['distances']) / len(retrieval_results['distances'])
                logger.info(f"Average retrieval distance: {avg_distance:.4f}")
            
            # Step 3: Generate recommendation using Gemini with retrieved context
            logger.info("Generating architecture recommendation with Gemini...")
            recommendation = self.gemini_service.generate_architecture_recommendation(
                user_context=user_context,
                retrieved_contexts=retrieved_documents,
                system_instruction=self.SYSTEM_INSTRUCTION
            )
            
            # Validate response structure
            required_fields = ['selectedArchitecture', 'explanation', 'diagramCode']
            for field in required_fields:
                if field not in recommendation:
                    raise ValueError(f"Missing required field in Gemini response: {field}")
            
            logger.info("RAG pipeline completed successfully")
            
            return recommendation
            
        except Exception as e:
            logger.error(f"Error in RAG pipeline: {str(e)}")
            raise
