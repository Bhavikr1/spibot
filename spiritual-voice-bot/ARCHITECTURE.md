# Spiritual Voice Bot - Technical Architecture

## System Overview

The Spiritual Voice Bot is a multilayered application designed to provide voice-enabled, scripture-grounded spiritual guidance based on Sanatan Dharma texts. The architecture follows modern best practices with clear separation of concerns and scalability in mind.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         Frontend                             │
│  (Next.js + React + TypeScript + Tailwind)                  │
│  - Voice recording & playback                                │
│  - Chat interface                                            │
│  - Citation display                                          │
└────────────────┬────────────────────────────────────────────┘
                 │ HTTP/REST API
                 │
┌────────────────▼────────────────────────────────────────────┐
│                      Backend API                             │
│               (FastAPI + Python)                             │
│  ┌──────────────────────────────────────────────────────┐   │
│  │           Main Application (main.py)                  │   │
│  │  - Request routing                                    │   │
│  │  - Request validation                                 │   │
│  │  - Error handling                                     │   │
│  └───────┬──────────────────────┬───────────────────────┘   │
│          │                      │                            │
│  ┌───────▼─────────┐    ┌──────▼──────────┐                │
│  │  Voice Module   │    │   RAG Pipeline   │                │
│  │  ┌───────────┐  │    │  ┌────────────┐ │                │
│  │  │    ASR    │  │    │  │ Embeddings │ │                │
│  │  │ (Whisper) │  │    │  │   Model    │ │                │
│  │  └───────────┘  │    │  └────────────┘ │                │
│  │  ┌───────────┐  │    │  ┌────────────┐ │                │
│  │  │    TTS    │  │    │  │  Retriever │ │                │
│  │  │ (Coqui)   │  │    │  │  (Semantic │ │                │
│  │  └───────────┘  │    │  │   Search)  │ │                │
│  └─────────────────┘    │  └────────────┘ │                │
│                         │  ┌────────────┐ │                │
│                         │  │  Response  │ │                │
│                         │  │ Generator  │ │                │
│                         │  └────────────┘ │                │
│                         └─────────────────┘                │
└─────────────────────────────────────────────────────────────┘
                          │
                          │ Vector Operations
                          │
┌─────────────────────────▼───────────────────────────────────┐
│                   Vector Database                            │
│                      (Qdrant)                                │
│  - Scripture embeddings storage                              │
│  - Semantic similarity search                                │
│  - Metadata filtering                                        │
└──────────────────────────────────────────────────────────────┘
```

---

## Component Details

### 1. Frontend Layer

**Technology**: Next.js 14 + React 18 + TypeScript

**Responsibilities**:
- User interface rendering
- Voice recording using Web Audio API
- Audio playback
- Real-time message display
- Language selection
- Citation formatting

**Key Files**:
- `pages/index.tsx` - Main chat interface
- `pages/_app.tsx` - App wrapper with global styles
- `styles/globals.css` - Tailwind CSS configuration

**Data Flow**:
```
User Input → Voice Recording/Text Input → API Request → Display Response
         ← Audio Playback ←
```

---

### 2. Backend API Layer

**Technology**: FastAPI + Python 3.10

**Responsibilities**:
- Request validation and routing
- Authentication (future)
- Rate limiting (future)
- Logging and monitoring
- Error handling
- CORS management

**Key Files**:
- `main.py` - FastAPI application & endpoints
- `config.py` - Configuration management
- `.env` - Environment variables

**Endpoints**:

| Endpoint | Method | Purpose | Input | Output |
|----------|--------|---------|-------|--------|
| `/health` | GET | Health check | - | Status |
| `/api/text/query` | POST | Text Q&A | Query text | Answer + citations |
| `/api/voice/query` | POST | Voice Q&A | Audio file | Audio response |
| `/api/scripture/search` | GET | Direct search | Query params | Scripture passages |
| `/api/embeddings/generate` | POST | Utility | Text | Embeddings |

---

### 3. RAG Pipeline

**Technology**: LangChain + Sentence Transformers

**Architecture**:

```
┌─────────────────────────────────────────────────────────────┐
│                    RAG Pipeline Flow                         │
└─────────────────────────────────────────────────────────────┘

User Query
    │
    ▼
┌──────────────────┐
│ Query Embedding  │ ← Sentence Transformer Model
│   Generation     │   (paraphrase-multilingual-mpnet)
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Vector Search    │ ← Cosine Similarity Search
│ (Top-K Retrieval)│   in Qdrant/In-Memory Store
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Re-ranking       │ ← ColBERT (Future)
│  (Optional)      │   Score-based filtering
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Context Building │ ← Combine retrieved passages
│                  │   with metadata
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Response         │ ← Template-based (POC)
│ Generation       │   LLM-based (Production)
└────────┬─────────┘
         │
         ▼
   Final Answer + Citations
```

**Key Components**:

1. **Embedding Model**:
   - Model: `sentence-transformers/paraphrase-multilingual-mpnet-base-v2`
   - Dimension: 768
   - Supports: 50+ languages including English, Hindi, Sanskrit

2. **Vector Store**:
   - POC: In-memory dictionary
   - Production: Qdrant vector database
   - Metadata: Scripture, chapter, verse, topic, language

3. **Retrieval Strategy**:
   - Cosine similarity search
   - Top-K retrieval (default: 5)
   - Minimum similarity threshold: 0.65
   - Metadata filtering by scripture/language

4. **Response Generation**:
   - POC: Template-based with rule matching
   - Production: Fine-tuned Airavata LLM
   - Citation formatting

**Key Files**:
- `rag/pipeline.py` - Main RAG logic
- `rag/__init__.py` - Module initialization

---

### 4. Voice Processing Module

#### 4.1 ASR (Automatic Speech Recognition)

**Technology**: OpenAI Whisper

**Model Selection**:
- POC: `whisper-base` (74M params)
- Production: `whisper-large-v3` (1.5B params)
- Fine-tuned: Custom Sanskrit/Hindi model (future)

**Process**:
```
Audio Bytes → Format Conversion → Whisper Model → Transcription
  (WAV/MP3)    (16kHz, mono)      (base/large)      (Text)
```

**Key Features**:
- Automatic language detection
- Multi-lingual support (English, Hindi, Sanskrit)
- Noise reduction
- Timestamp generation

**Key Files**:
- `voice/asr.py` - ASR implementation

#### 4.2 TTS (Text-to-Speech)

**Technology**: Coqui TTS

**Model Selection**:
- POC: `xtts_v2` (multilingual)
- Production: AI4Bharat Indic-TTS
- Future: Fine-tuned Sanskrit pronunciation model

**Process**:
```
Text → TTS Model → Audio Waveform → Format Conversion → Audio Bytes
                  (numpy array)      (WAV, 22kHz)        (bytes)
```

**Key Features**:
- Multi-lingual synthesis
- Voice cloning capability
- Adjustable speed and pitch
- Multiple speaker support

**Key Files**:
- `voice/tts.py` - TTS implementation

---

### 5. Data Layer

#### 5.1 Scripture Database

**Structure**:
```json
{
  "text": "You have a right to perform your prescribed duties...",
  "reference": "Bhagavad Gita 2.47",
  "scripture": "Bhagavad Gita",
  "chapter": 2,
  "verse": 47,
  "topic": "Karma Yoga",
  "language": "en"
}
```

**Metadata Schema**:
- `text` - The actual verse/passage
- `reference` - Citation format (e.g., "Bhagavad Gita 2.47")
- `scripture` - Source text name
- `chapter` - Chapter number
- `verse` - Verse number
- `topic` - Thematic classification
- `language` - Language code (en, hi, sa)

#### 5.2 Vector Database (Qdrant)

**Configuration**:
```yaml
Collection: sanatan_scriptures
Vector Size: 768
Distance: Cosine
Indexed Fields:
  - scripture
  - language
  - chapter
  - topic
```

**Storage**:
- POC: In-memory Python dictionary
- Production: Qdrant persistent storage
- Volume: `./data/qdrant_storage`

---

## Data Flow Diagrams

### Text Query Flow

```
1. User enters text query
2. Frontend sends POST to /api/text/query
3. Backend validates request
4. RAG pipeline generates query embedding
5. Vector search retrieves top-K passages
6. Response generator creates answer with citations
7. Backend returns JSON response
8. Frontend displays answer and citations
```

### Voice Query Flow

```
1. User clicks mic and speaks
2. Frontend records audio (Web Audio API)
3. Frontend sends audio file to /api/voice/query
4. Backend receives audio bytes
5. ASR transcribes audio to text
6. RAG pipeline processes query
7. TTS synthesizes response to audio
8. Backend returns audio file
9. Frontend plays audio response
```

---

## Configuration Management

### Environment Variables

**Backend** (`.env`):
```bash
# API Settings
API_HOST=0.0.0.0
API_PORT=8000

# Model Settings
LLM_MODEL_NAME=ai4bharat/Airavata
EMBEDDING_MODEL=sentence-transformers/...
LLM_DEVICE=cuda  # or cpu

# Vector DB
QDRANT_HOST=localhost
QDRANT_PORT=6333

# Voice Models
ASR_MODEL=openai/whisper-base
TTS_MODEL=tts_models/multilingual/...

# API Keys
HUGGINGFACE_TOKEN=your_token_here
```

**Frontend** (`.env.local`):
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## Security Considerations

### Current Implementation (POC)

- No authentication
- Open CORS (allow all origins)
- No rate limiting
- No input sanitization (basic validation only)

### Production Requirements

1. **Authentication**:
   - JWT tokens
   - API keys
   - OAuth integration

2. **Authorization**:
   - Role-based access control
   - Query quotas

3. **Input Validation**:
   - Query length limits
   - Audio file size/format validation
   - SQL injection prevention
   - XSS protection

4. **Rate Limiting**:
   - Per-user query limits
   - IP-based throttling
   - DDoS protection

5. **Data Privacy**:
   - Query logging (opt-in)
   - PII detection and removal
   - GDPR compliance

---

## Performance Optimization

### Current Performance (POC)

| Metric | Value | Hardware |
|--------|-------|----------|
| Text Query | 1-2s | CPU (M1 Mac) |
| Voice Query | 3-5s | CPU (M1 Mac) |
| Embedding Generation | 50ms | CPU |
| Vector Search | 10ms | In-memory |

### Optimization Strategies

1. **Model Optimization**:
   - Quantization (INT8/FP16)
   - Model pruning
   - Distillation
   - ONNX conversion

2. **Caching**:
   - Query result caching (Redis)
   - Embedding caching
   - Response caching

3. **Async Processing**:
   - Background tasks (Celery)
   - Streaming responses
   - Batch processing

4. **Hardware Acceleration**:
   - GPU inference (CUDA)
   - TPU support
   - Multi-GPU setup

5. **Database Optimization**:
   - Index optimization
   - Sharding
   - Replication

---

## Scalability Architecture (Production)

```
                          ┌──────────────┐
                          │ Load Balancer│
                          └───────┬──────┘
                                  │
         ┌────────────────────────┼────────────────────────┐
         │                        │                        │
    ┌────▼────┐            ┌─────▼─────┐          ┌──────▼──────┐
    │ Backend │            │  Backend  │          │   Backend   │
    │ Server 1│            │  Server 2 │          │   Server N  │
    └────┬────┘            └─────┬─────┘          └──────┬──────┘
         │                        │                       │
         └────────────────────────┼───────────────────────┘
                                  │
         ┌────────────────────────┼────────────────────────┐
         │                        │                        │
    ┌────▼────┐            ┌─────▼─────┐          ┌──────▼──────┐
    │ Qdrant  │            │   Redis   │          │   Celery    │
    │ Cluster │            │   Cache   │          │    Queue    │
    └─────────┘            └───────────┘          └─────────────┘
```

---

## Monitoring & Observability

### Metrics to Track

1. **Performance Metrics**:
   - Request latency (p50, p95, p99)
   - Throughput (requests/sec)
   - Error rate
   - Voice processing time

2. **Model Metrics**:
   - Retrieval accuracy
   - Citation faithfulness
   - Response relevance
   - ASR word error rate (WER)
   - TTS mean opinion score (MOS)

3. **System Metrics**:
   - CPU/GPU utilization
   - Memory usage
   - Disk I/O
   - Network bandwidth

### Logging Strategy

```python
# Structured logging with loguru
logger.info(
    "Query processed",
    query_id=uuid,
    language=lang,
    latency_ms=latency,
    citations_count=len(citations),
    confidence=score
)
```

### Monitoring Tools (Production)

- **Metrics**: Prometheus + Grafana
- **Logging**: ELK Stack (Elasticsearch, Logstash, Kibana)
- **Tracing**: Jaeger
- **APM**: New Relic / DataDog
- **Alerting**: PagerDuty

---

## Deployment Architecture

### Development

```bash
# Local development
Backend: http://localhost:8000
Frontend: http://localhost:3000
Qdrant: http://localhost:6333
```

### Staging

```bash
# Docker Compose
docker-compose -f docker-compose.staging.yml up
```

### Production

```
Cloud Provider: AWS / GCP / Azure
Container Orchestration: Kubernetes
CI/CD: GitHub Actions
Infrastructure as Code: Terraform
```

**Kubernetes Deployment**:
```
- Backend: 3 replicas (auto-scaling)
- Qdrant: StatefulSet (3 nodes)
- Redis: Cluster mode
- Ingress: NGINX
- SSL: Cert-Manager + Let's Encrypt
```

---

## Technology Stack Summary

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Frontend | Next.js 14 + React | UI framework |
| Frontend | TypeScript | Type safety |
| Frontend | Tailwind CSS | Styling |
| Backend | FastAPI | API framework |
| Backend | Python 3.10 | Language |
| Backend | Pydantic | Validation |
| LLM | Sentence Transformers | Embeddings |
| LLM | Airavata (future) | Generation |
| Voice | Whisper | ASR |
| Voice | Coqui TTS | TTS |
| Database | Qdrant | Vector DB |
| Database | Redis (future) | Caching |
| DevOps | Docker | Containerization |
| DevOps | Docker Compose | Orchestration (dev) |
| DevOps | Kubernetes (future) | Orchestration (prod) |

---

## Future Enhancements

### Phase 2: Fine-tuned LLM
- Train/fine-tune Airavata on spiritual Q&A dataset
- Implement QLoRA for efficient training
- Add model versioning

### Phase 3: Knowledge Graph
- Implement Neo4j database
- Build ontology for Hindu mythology
- Integrate GraphRAG

### Phase 4: Advanced Features
- User memory and personalization
- Multi-turn conversations
- Context management
- Emotional intelligence

### Phase 5: Mobile Apps
- React Native apps
- Offline mode
- Push notifications
- Daily verse feature

### Phase 6: Analytics
- User behavior tracking
- A/B testing framework
- Feedback collection
- Continuous improvement

---

## Conclusion

This architecture provides a solid foundation for a scalable, maintainable spiritual AI companion. The modular design allows for easy upgrades and feature additions while maintaining clean separation of concerns.

**Key Strengths**:
- Modular and extensible
- Scripture-grounded responses
- Multi-lingual support
- Voice-enabled interaction
- Clean API design

**Areas for Growth**:
- Fine-tuned LLM integration
- Knowledge graph addition
- Production-grade security
- Advanced RAG techniques
- Mobile platform support
