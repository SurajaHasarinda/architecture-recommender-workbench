# API Documentation

## Base URL

```
http://localhost:8000
```

## Authentication

Currently, no authentication is required. The API uses Google Gemini API key configured on the server side.

---

## Endpoints

### 1. Health Check

#### `GET /`

Simple health check endpoint.

**Response**

```json
{
  "status": "healthy",
  "service": "Architecture Recommendation Agent",
  "version": "1.0.0"
}
```

**Status Codes**

- `200 OK`: Service is running

---

### 2. Detailed Health Check

#### `GET /api/health`

Detailed health status of all system components.

**Response**

```json
{
  "status": "healthy",
  "services": {
    "vector_store": true,
    "gemini_service": true,
    "rag_service": true
  }
}
```

**Status Codes**

- `200 OK`: All services operational

---

### 3. Get Architecture Recommendation

#### `POST /api/recommend-architecture`

Get an AI-powered architecture recommendation based on project context.

**Request Body**

```json
{
  "context": "string (min 10 characters)"
}
```

**Parameters**

| Field   | Type   | Required | Description                                                                       |
| ------- | ------ | -------- | --------------------------------------------------------------------------------- |
| context | string | Yes      | User's project description, requirements, and constraints (minimum 10 characters) |

**Example Request**

```json
{
  "context": "I'm building a simple e-commerce application for a startup with 3 developers. We need to launch an MVP quickly within 3 months. Expected user base is around 1000 users initially. Budget is limited and we have no DevOps expertise."
}
```

**Response**

```json
{
  "selectedArchitecture": "string",
  "explanation": "string",
  "diagramCode": "string"
}
```

**Response Fields**

| Field                | Type   | Description                                                                                                   |
| -------------------- | ------ | ------------------------------------------------------------------------------------------------------------- |
| selectedArchitecture | string | Name of the recommended architecture (e.g., "Monolithic Architecture")                                        |
| explanation          | string | Detailed explanation of why this architecture was selected, addressing specific aspects of the user's context |
| diagramCode          | string | Mermaid.js diagram code using `graph TD` syntax                                                               |

**Example Response**

```json
{
  "selectedArchitecture": "Monolithic Architecture",
  "explanation": "Based on your requirements for a startup MVP with a small team of 3 developers, limited budget, and no DevOps expertise, a Monolithic Architecture is the best choice. Here's why:\n\n1. **Rapid Development**: With only 3 months to launch, a monolithic architecture offers the fastest path to deployment. All components are in one codebase, making it simpler to develop and understand.\n\n2. **Small Team Efficiency**: Your team of 3 developers can work effectively without the complexity of managing multiple services, deployment pipelines, or distributed system challenges.\n\n3. **Budget Constraints**: Monolithic applications have minimal infrastructure costs. You can deploy to a single server or simple cloud instance, avoiding the operational overhead of microservices or serverless architectures.\n\n4. **No DevOps Requirement**: Unlike microservices or containerized solutions, monoliths don't require sophisticated DevOps practices, CI/CD pipelines, or container orchestration.\n\n5. **Scale Appropriately**: For 1000 initial users, a well-designed monolith can easily handle the load with vertical scaling if needed.\n\nThis architecture will allow you to focus on building features and validating your product-market fit rather than wrestling with infrastructure complexity.",
  "diagramCode": "graph TD\n    A[User Interface Layer] --> B[Business Logic Layer]\n    B --> C[Data Access Layer]\n    C --> D[(Database)]\n    E[Authentication Module] --> B\n    F[Payment Service] --> B\n    G[Inventory Management] --> B\n    B --> H[External APIs]"
}
```

**Status Codes**

- `200 OK`: Recommendation generated successfully
- `422 Unprocessable Entity`: Invalid input (context too short, etc.)
- `500 Internal Server Error`: Error during processing
- `503 Service Unavailable`: RAG service not initialized

**Error Response**

```json
{
  "detail": "Error message describing what went wrong"
}
```

---

## Request Examples

### Using cURL (Windows PowerShell)

```powershell
curl -X POST "http://localhost:8000/api/recommend-architecture" `
  -H "Content-Type: application/json" `
  -d '{\"context\": \"Building a real-time IoT platform with 1000 sensors\"}'
```

### Using PowerShell Invoke-RestMethod

```powershell
$body = @{
    context = "Building a large-scale enterprise system with 50 developers and millions of users"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/recommend-architecture" `
  -Method Post `
  -Body $body `
  -ContentType "application/json"
```

### Using Python requests

```python
import requests

response = requests.post(
    "http://localhost:8000/api/recommend-architecture",
    json={
        "context": "Creating a seasonal e-commerce site with unpredictable traffic spikes"
    }
)

result = response.json()
print(f"Architecture: {result['selectedArchitecture']}")
print(f"Explanation: {result['explanation']}")
print(f"Diagram:\n{result['diagramCode']}")
```

### Using JavaScript fetch

```javascript
fetch("http://localhost:8000/api/recommend-architecture", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    context:
      "Building a social media platform for a university with 10000 students",
  }),
})
  .then((response) => response.json())
  .then((data) => {
    console.log("Architecture:", data.selectedArchitecture);
    console.log("Explanation:", data.explanation);
    console.log("Diagram Code:", data.diagramCode);
  });
```

---

## Mermaid Diagram Rendering

The `diagramCode` returned by the API uses Mermaid.js `graph TD` (top-down graph) syntax.

### Online Rendering

Visit [Mermaid Live Editor](https://mermaid.live/) and paste the `diagramCode`.

### Frontend Integration

```html
<!DOCTYPE html>
<html>
  <head>
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
  </head>
  <body>
    <div class="mermaid">
      <!-- Paste diagramCode here -->
      graph TD A[Component] --> B[Another Component]
    </div>
    <script>
      mermaid.initialize({ startOnLoad: true });
    </script>
  </body>
</html>
```

### React Integration

```jsx
import React from "react";
import mermaid from "mermaid";

function ArchitectureDiagram({ diagramCode }) {
  React.useEffect(() => {
    mermaid.initialize({ startOnLoad: true });
    mermaid.contentLoaded();
  }, [diagramCode]);

  return <div className="mermaid">{diagramCode}</div>;
}
```

---

## Rate Limits

No explicit rate limiting is currently implemented. However, be aware of:

- **Google Gemini API limits**: Check your quota at https://console.cloud.google.com/
- **Recommended**: 1-2 requests per second for optimal performance

---

## Best Practices

### Context Guidelines

For best results, include in your context:

1. **Team Size**: Number of developers
2. **Timeline**: Development and launch timeline
3. **Scale**: Expected user base and growth
4. **Budget**: Infrastructure budget constraints
5. **Expertise**: Team's technical expertise level
6. **Requirements**: Key functional and non-functional requirements
7. **Constraints**: Any specific limitations or requirements

**Good Example:**

```
"We're building a healthcare patient management system for a hospital network.
Team of 15 developers, need to launch in 6 months. Must handle 50,000 patients
with strict HIPAA compliance. Budget allows for cloud infrastructure. Need high
availability (99.9% uptime). Data security is critical."
```

**Poor Example:**

```
"Need to build an app"
```

### Error Handling

Always check the response status code and handle errors appropriately:

```python
response = requests.post(url, json={"context": user_input})

if response.status_code == 200:
    result = response.json()
    # Process result
elif response.status_code == 422:
    print("Invalid input:", response.json()["detail"])
elif response.status_code == 500:
    print("Server error, please try again later")
```

---

## Response Time

Typical response times:

- **Health Check**: <100ms
- **Architecture Recommendation**: 2-5 seconds
  - Embedding generation: ~500ms
  - Vector search: ~100ms
  - AI generation: 1-4 seconds

---

## Troubleshooting

### 503 Service Unavailable

**Cause**: RAG service not initialized (usually due to missing API key or failed document loading)

**Solution**: Check server logs, verify GOOGLE_API_KEY in .env

### 422 Unprocessable Entity

**Cause**: Invalid request body (context too short, wrong format)

**Solution**: Ensure context is at least 10 characters and properly formatted JSON

### 500 Internal Server Error

**Cause**: Error during RAG pipeline execution

**Solution**: Check server logs for details, verify Gemini API quota

---

## Interactive Documentation

Visit http://localhost:8000/docs for interactive Swagger UI where you can:

- Test endpoints directly from browser
- See detailed request/response schemas
- Try different inputs and see results

---

## OpenAPI Specification

Download the OpenAPI schema:

```
http://localhost:8000/openapi.json
```

---

## Support

For issues or questions:

1. Check application logs
2. Verify your GOOGLE_API_KEY
3. Review the SETUP_GUIDE.md
4. Test with the provided test_api.py script

---

**API Version**: 1.0.0  
**Last Updated**: October 24, 2025
