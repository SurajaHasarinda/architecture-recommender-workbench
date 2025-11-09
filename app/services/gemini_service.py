import logging
import time
from typing import List, Dict, Any
import google.generativeai as genai

from app.config import settings

logger = logging.getLogger(__name__)


class GeminiService:    
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        genai.configure(api_key=api_key)
        
        # Initialize embedding model
        self.embedding_model_name = settings.embedding_model
        
        # Initialize generation model
        self.generation_model_name = settings.generation_model
        self.generation_model = genai.GenerativeModel(self.generation_model_name)
        
        logger.info(f"Gemini service initialized with models: {self.embedding_model_name}, {self.generation_model_name}")
    
    def generate_embedding(self, text: str) -> List[float]:
        try:
            result = genai.embed_content(
                model=self.embedding_model_name,
                content=text,
                task_type="retrieval_document"
            )
            return result['embedding']
        except Exception as e:
            logger.error(f"Error generating embedding: {str(e)}")
            raise
    
    def generate_embeddings_batch(self, texts: List[str], batch_size: int = 100) -> List[List[float]]:
        embeddings = []
        
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            logger.info(f"Processing embedding batch {i//batch_size + 1}/{(len(texts)-1)//batch_size + 1}")
            
            for text in batch:
                try:
                    embedding = self.generate_embedding(text)
                    embeddings.append(embedding)
                    # Small delay to respect API rate limits
                    time.sleep(0.1)
                except Exception as e:
                    logger.error(f"Error processing text in batch: {str(e)}")
                    # Add a zero vector as placeholder for failed embeddings
                    embeddings.append([0.0] * 768)  # Default dimension for text-embedding-004
        
        return embeddings
    
    def generate_query_embedding(self, query: str) -> List[float]:
        try:
            result = genai.embed_content(
                model=self.embedding_model_name,
                content=query,
                task_type="retrieval_query"
            )
            return result['embedding']
        except Exception as e:
            logger.error(f"Error generating query embedding: {str(e)}")
            raise
    
    def generate_architecture_recommendation(
        self,
        user_context: str,
        retrieved_contexts: List[str],
        system_instruction: str
    ) -> Dict[str, Any]:
        try:
            # Construct the prompt
            context_docs = "\n\n".join([
                f"Context Document {i+1}:\n{doc}"
                for i, doc in enumerate(retrieved_contexts)
            ])
            
            prompt = f"""
                {system_instruction}

                USER'S PROJECT CONTEXT:
                {user_context}

                RETRIEVED CONTEXT DOCUMENTS:
                {context_docs}

                Based on the above information, analyze the user's requirements and select the MOST APPROPRIATE architecture. Provide your response in the required JSON format.
                """
            
            # Define the response schema for JSON mode
            response_schema = {
                "type": "object",
                "properties": {
                    "selectedArchitecture": {
                        "type": "string",
                        "description": "Name of the selected architecture"
                    },
                    "explanation": {
                        "type": "string",
                        "description": "Detailed explanation of why this architecture was chosen"
                    },
                    "diagramCode": {
                        "type": "string",
                        "description": "Mermaid.js diagram code using graph TD syntax"
                    }
                },
                "required": ["selectedArchitecture", "explanation", "diagramCode"]
            }
            
            # Configure generation with JSON output
            generation_config = genai.GenerationConfig(
                response_mime_type="application/json",
                response_schema=response_schema,
                temperature=0.7,
                top_p=0.95,
                max_output_tokens=4096  # Increased for longer responses
            )
            
            logger.info("Sending request to Gemini API for architecture recommendation...")
            
            # Generate response
            response = self.generation_model.generate_content(
                prompt,
                generation_config=generation_config
            )
            
            # Parse JSON response with better error handling
            import json
            import re
            
            response_text = response.text
            logger.debug(f"Raw response: {response_text[:200]}...")
            
            try:
                # Try direct parsing first
                result = json.loads(response_text)
            except json.JSONDecodeError as e:
                logger.warning(f"Initial JSON parsing failed: {str(e)}")
                
                # Try to extract JSON from markdown code blocks if present
                json_match = re.search(r'```json\s*(.*?)\s*```', response_text, re.DOTALL)
                if json_match:
                    response_text = json_match.group(1)
                    logger.info("Extracted JSON from markdown code block")
                
                # Try to clean up common issues
                response_text = response_text.strip()
                
                # Try parsing again
                try:
                    result = json.loads(response_text)
                except json.JSONDecodeError:
                    # If still failing, try to fix escaped newlines in diagramCode
                    response_text = response_text.replace('\\n', '\\\\n')
                    result = json.loads(response_text)
            
            # Validate required fields
            required_fields = ['selectedArchitecture', 'explanation', 'diagramCode']
            for field in required_fields:
                if field not in result:
                    raise ValueError(f"Missing required field: {field}")
            
            logger.info(f"Successfully generated recommendation for: {result.get('selectedArchitecture')}")
            
            return result
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing error: {str(e)}")
            logger.error(f"Response text: {response_text if 'response_text' in locals() else 'N/A'}")
            raise ValueError(f"Failed to parse Gemini response as JSON: {str(e)}")
        except Exception as e:
            logger.error(f"Error generating architecture recommendation: {str(e)}")
            raise
