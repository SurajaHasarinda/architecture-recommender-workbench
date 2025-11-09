from pydantic import BaseModel, Field

class ProjectContextRequest(BaseModel):

    context: str = Field(
        ...,
        min_length=10,
        description="User's project context describing requirements, constraints, and goals"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "context": "I'm building a simple e-commerce application for a startup with 3 developers. We need to launch an MVP quickly within 3 months. Expected user base is around 1000 users initially. Budget is limited."
            }
        }


class ArchitectureRecommendationResponse(BaseModel):
    
    selectedArchitecture: str = Field(
        ...,
        description="Name of the recommended architecture"
    )
    explanation: str = Field(
        ...,
        description="Detailed explanation of why this architecture was selected"
    )
    diagramCode: str = Field(
        ...,
        description="Mermaid.js diagram code (graph TD syntax) for the architecture"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "selectedArchitecture": "Monolithic Architecture",
                "explanation": "Based on your requirements for a startup MVP with a small team of 3 developers and limited budget, a Monolithic Architecture is the best choice. It offers simplicity in development and deployment, which is crucial for meeting your 3-month timeline...",
                "diagramCode": "graph TD\n    A[User Interface] --> B[Business Logic Layer]\n    B --> C[Data Access Layer]\n    C --> D[(Database)]"
            }
        }
