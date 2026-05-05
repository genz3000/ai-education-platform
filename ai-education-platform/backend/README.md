# AI Education Platform - Backend

## Project Structure

```
backend/
├── src/
│   ├── main.py                 # FastAPI application entry
│   ├── config.py              # Configuration management
│   ├── api/
│   │   ├── __init__.py
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── router.py      # Main API router
│   │   │   ├── auth.py        # Authentication endpoints
│   │   │   ├── knowledge.py   # Knowledge base endpoints
│   │   │   ├── qa.py          # Q&A endpoints
│   │   │   ├── assessment.py  # Assessment endpoints
│   │   │   └── analytics.py   # Analytics endpoints
│   │   └── deps.py            # Dependencies
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── school.py
│   │   ├── knowledge.py
│   │   ├── question.py
│   │   ├── assessment.py
│   │   └── analytics.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── knowledge.py
│   │   ├── qa.py
│   │   ├── assessment.py
│   │   └── analytics.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   ├── knowledge_service.py
│   │   ├── qa_service.py
│   │   ├── assessment_service.py
│   │   ├── analytics_service.py
│   │   └── llm_service.py
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── qa_agent.py        # Q&A AI agent
│   │   ├── assessment_agent.py # Assessment AI agent
│   │   ├── teaching_agent.py   # Teaching assistant agent
│   │   └── orchestrator.py     # Agent orchestration
│   ├── rag/
│   │   ├── __init__.py
│   │   ├── embeddings.py      # Embedding service
│   │   ├── vector_store.py    # Vector database operations
│   │   ├── retriever.py       # Retrieval logic
│   │   ├── chunker.py         # Document chunking
│   │   └── reranker.py        # Reranking logic
│   ├── knowledge/
│   │   ├── __init__.py
│   │   ├── document_processor.py
│   │   ├── ocr_service.py
│   │   └── knowledge_graph.py
│   ├── curriculum/
│   │   ├── __init__.py
│   │   ├── dse_matcher.py     # DSE curriculum mapping
│   │   └── tsa_matcher.py     # TSA curriculum mapping
│   ├── assessment/
│   │   ├── __init__.py
│   │   ├── question_generator.py
│   │   ├── grader.py          # AI grading
│   │   └── feedback_generator.py
│   ├── analytics/
│   │   ├── __init__.py
│   │   ├── student_analyzer.py
│   │   ├── class_analyzer.py
│   │   └── predictor.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── security.py
│   │   ├── database.py
│   │   └── logger.py
│   └── middleware/
│       ├── __init__.py
│       ├── auth.py
│       └── cors.py
├── tests/
│   ├── unit/
│   ├── integration/
│   └── fixtures/
├── scripts/
│   ├── init_db.py
│   └── seed_data.py
├── pyproject.toml
└── requirements.txt
```

## Tech Stack

- **Framework**: FastAPI 0.110+
- **Language**: Python 3.11+
- **Database**: PostgreSQL 15+ with pgvector
- **Cache**: Redis 7+
- **ORM**: SQLAlchemy 2.0 + asyncpg
- **LLM**: OpenAI SDK / Anthropic SDK
- **Vector DB**: pgvector (extension)
- **File Storage**: S3-compatible (MinIO for dev)
- **Task Queue**: Celery + Redis

## Getting Started

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment variables
cp .env.example .env

# Initialize database
python scripts/init_db.py

# Start development server
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Run tests
pytest tests/ -v
```

## Environment Variables

```env
# Database
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/ai_education
REDIS_URL=redis://localhost:6379/0

# LLM Services
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

# Vector DB
EMBEDDING_MODEL=text-embedding-3-small
EMBEDDING_DIMENSION=1536

# File Storage
S3_ENDPOINT=http://localhost:9000
S3_ACCESS_KEY=minioadmin
S3_SECRET_KEY=minioadmin
S3_BUCKET=ai-education

# Auth
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# LMS Integration
LMS_TYPE=google_classroom  # google_classroom / microsoft_teams / moodle
LMS_CLIENT_ID=
LMS_CLIENT_SECRET=
```

## API Endpoints

### Authentication
```
POST   /api/v1/auth/register     # Register new user
POST   /api/v1/auth/login        # Login
POST   /api/v1/auth/refresh      # Refresh token
POST   /api/v1/auth/logout       # Logout
GET    /api/v1/auth/me           # Get current user
```

### Knowledge Base
```
POST   /api/v1/knowledge/upload          # Upload document
GET    /api/v1/knowledge/search          # Search knowledge
GET    /api/v1/knowledge/{id}           # Get document
PUT    /api/v1/knowledge/{id}            # Update document
DELETE /api/v1/knowledge/{id}            # Delete document
GET    /api/v1/knowledge/topics          # Get knowledge graph
POST   /api/v1/knowledge/process         # Process document (OCR, chunk)
```

### Q&A
```
POST   /api/v1/qa/ask                   # Ask question
GET    /api/v1/qa/history               # Get chat history
DELETE /api/v1/qa/history/{id}          # Delete conversation
POST   /api/v1/qa/feedback              # Rate answer
```

### Assessment
```
POST   /api/v1/assessment/generate      # Generate questions
POST   /api/v1/assessment/submit         # Submit answers
POST   /api/v1/assessment/grade          # Grade submission
GET    /api/v1/assessment/report         # Get report
GET    /api/v1/assessment/{id}          # Get assessment details
```

### Analytics
```
GET    /api/v1/analytics/student/{id}   # Student analytics
GET    /api/v1/analytics/class/{id}     # Class analytics
GET    /api/v1/analytics/trends          # Learning trends
GET    /api/v1/analytics/recommendations # Get recommendations
```

## RAG Pipeline

```
Document Upload → OCR (if image) → Chunking → Embedding → Vector Store
                                                        ↓
User Query → Embed → Search → Rerank → Context → LLM → Answer
```

### Chunking Strategy
- **Text**: Recursive character splitting (500 tokens, 50 overlap)
- **Tables**: Keep table as single chunk
- **Code**: Function-level splitting

### Retrieval
1. Hybrid search (BM25 + vector similarity)
2. Rerank with Cross-Encoder
3. Deduplicate similar chunks

## AI Agents

### QA Agent
- Uses RAG for context
- Maintains conversation history
- Cites sources from knowledge base

### Assessment Agent
- Generates questions by topic/difficulty
- Grades answers with explanation
- Provides personalized feedback

### Teaching Agent
- Creates lesson plans
- Suggests learning resources
- Identifies knowledge gaps

## Testing

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Run specific test file
pytest tests/unit/test_qa_service.py -v

# Run integration tests (requires DB)
pytest tests/integration/ -v
```

## Deployment

### Docker
```bash
docker build -t ai-education-backend .
docker-compose up -d
```

### Kubernetes
```bash
kubectl apply -f k8s/backend-deployment.yaml
kubectl apply -f k8s/backend-service.yaml
```

## Monitoring

- **Health**: GET /health
- **Metrics**: GET /metrics (Prometheus format)
- **Logs**: Structured JSON logging