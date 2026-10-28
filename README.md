# 🛍️ ShopMuse AI
### RAG-Powered Conversational Shopping Assistant | Multi-Agent Product Discovery System

ShopMuse AI is an intelligent conversational shopping assistant that helps users discover products through natural-language conversations.

Instead of relying only on traditional keyword searches and filters, ShopMuse understands shopping intent, extracts constraints, remembers preferences, retrieves relevant products, ranks recommendations, and explains why each product is suitable.

The upgraded system integrates **Retrieval-Augmented Generation (RAG), ChromaDB, MongoDB, and a multi-agent architecture** to support semantic product discovery, grounded recommendations, and responsible AI-assisted shopping.

## ✨ Key Features

- **Conversational Product Discovery:** Understands vague, complex, and evolving shopping requests.
- **Multi-Agent Architecture:** Uses 10 specialized agents coordinated by an Orchestrator, Planner, and Reviewer.
- **RAG-Based Recommendations:** Retrieves relevant product context before generating recommendation explanations.
- **Hybrid Product Retrieval:** Combines semantic similarity search with structured catalog filtering.
- **ChromaDB Vector Database:** Stores product embeddings for semantic retrieval.
- **MongoDB Catalog Storage:** Maintains structured product records, prices, ratings, categories, and stock availability.
- **Session Memory:** Retains shopping preferences across follow-up messages.
- **Intelligent Clarification:** Requests additional information when essential shopping requirements are missing.
- **Constraint-Aware Ranking:** Evaluates products using budget, category, preferences, and ratings.
- **Planner–Reviewer Workflow:** Plans retrieval steps, validates recommendations, and supports replanning.
- **Explainable Recommendations:** Provides product-specific explanations and matching reasons.
- **Zero-Result Fallback:** Suggests alternatives when suitable products are unavailable.
- **Product Comparison:** Allows users to compare up to three recommended products.
- **ShopMuse Pick:** Highlights the highest-ranked recommendation.
- **Guardrails:** Provides input validation, constraint checks, and product-claim verification.
- **Governance:** Introduces privacy-conscious logging, access-control provisions, and responsible recommendation safeguards.

## 🧠 Multi-Agent Architecture

ShopMuse retains its original 10 agents, with additional planning and reviewing components.

| Agent | Responsibility |
|---|---|
| Query Ingestion Agent | Normalizes incoming user queries |
| Intent & Constraint Extraction Agent | Identifies categories, budgets, preferences, recipients, and occasions |
| Ambiguity & Clarification Agent | Requests missing information |
| Catalog Attribute Mapping Agent | Converts shopping intent into searchable catalog attributes |
| Candidate Retrieval Agent | Retrieves relevant products through the tool layer |
| Ranking & Fit Scoring Agent | Scores products based on suitability |
| Explanation Generation Agent | Produces grounded product explanations |
| Zero-Result & Fallback Agent | Handles unsuccessful searches |
| Session Memory Agent | Maintains conversational context |
| Orchestrator Agent | Coordinates the end-to-end workflow |
| Planner Agent | Creates execution plans and supports replanning |
| Reviewer Agent | Validates recommendations against requirements |

## 🏗️ System Architecture

```text
                    USER
                      |
                React Frontend
                      |
                FastAPI Backend
                      |
                 Orchestrator
                      |
                    Planner
                      |
               Query Ingestion
                      |
          Intent & Constraint Extraction
                      |
                Clarification
                      |
              Attribute Mapping
                      |
              RAG / Hybrid Retrieval
                      |
              API / Tool Layer
                      |
          +-----------+-----------+
          |                       |
       ChromaDB                 MongoDB
   Semantic Search         Structured Catalog
   Product Embeddings      Price, Stock, Details
          |                       |
          +-----------+-----------+
                      |
              Candidate Retrieval
                      |
              Ranking & Fit Scoring
                      |
                   Reviewer
                      |
           Approval / Replanning
                      |
              Explanation Agent
                      |
             Final Recommendations
```

**Cross-cutting components:**

- Session Memory
- Input and Output Guardrails
- Governance and Compliance
- Audit Logging
- Error Handling and Fallbacks

## 🔍 RAG and Hybrid Retrieval

ShopMuse uses a retrieval-augmented approach to improve product discovery.

**1. Query Understanding**

The system extracts shopping requirements such as product category, maximum budget, desired features, and user preferences.

**2. Semantic Search**

ChromaDB stores vector embeddings of product information. Semantic retrieval helps identify relevant products even when the user's wording differs from catalog keywords.

**3. Structured Retrieval**

MongoDB supplies authoritative product information, including prices, ratings, availability, categories, and tags.

**4. Hybrid Retrieval**

Semantic results and structured catalog information are combined to identify suitable candidates while enforcing hard constraints.

**5. Recommendation Generation**

The Ranking Agent evaluates retrieved candidates, the Reviewer validates the results, and the Explanation Agent generates descriptions grounded in retrieved product information.

## 🗄️ Database Architecture

### MongoDB — Structured Product Catalog

Stores product information such as:

- Product ID and name
- Category
- Price
- Rating
- Product tags
- Stock availability

### ChromaDB — Vector Database

Stores product embeddings for semantic similarity search.

Each product's vector representation is associated with its catalog identity, allowing retrieved results to be matched against MongoDB records.

**Current catalog:** 114 products and 114 vector embeddings successfully seeded.

## 🛠️ API and Tool Layer

The dedicated tool layer separates agent logic from database implementation details.

It supports operations for product search, product details, semantic search, availability and pricing, and catalog access.

This makes the architecture more modular and allows the retrieval implementation to evolve without unnecessarily rewriting the agents.

## 🛡️ Guardrails and Governance

ShopMuse introduces foundational safeguards for safer product recommendations.

**Guardrails**

- Input validation
- Shopping constraint validation
- Prompt-injection protection measures
- Controlled tool usage
- Product information verification
- Prevention of unsupported product claims

**Governance and Compliance**

- Privacy-conscious handling of user information
- Access-control provisions
- Secure database and tool configuration
- Audit logging
- Responsible product recommendation practices

These controls provide a foundation for responsible AI development and are not a claim of complete security or regulatory certification.

## 💬 Session Memory and Refinement

ShopMuse supports follow-up requests without requiring users to repeat their complete shopping requirements.

**Example conversation:**

**User:** I need lightweight hiking equipment under $100.

**ShopMuse:** Retrieves and ranks relevant hiking products.

**User:** Make it cheaper.

**ShopMuse:** Retains the hiking context and adjusts the budget.

**User:** I also want something comfortable.

**ShopMuse:** Incorporates the additional preference while retaining relevant earlier requirements.

Session memory enables contextual shopping conversations and iterative recommendation refinement.

## 💻 Technology Stack

| Layer | Technology |
|---|---|
| Frontend | React, Vite, JavaScript |
| Styling | CSS, Lucide React |
| Backend | Python, FastAPI |
| LLM Integration | Groq API |
| Structured Database | MongoDB |
| Vector Database | ChromaDB |
| Embeddings | Sentence-transformer-based embedding model |
| Retrieval | Hybrid structured and semantic search |
| Architecture | Multi-Agent System, RAG, Planner–Reviewer |
| API Documentation | FastAPI Swagger UI |

## 📂 Project Structure

```text
shopmuse-ai/
├── backend/
│   ├── app/
│   │   ├── agents/
│   │   │   ├── ingestion_agent.py
│   │   │   ├── intent_agent.py
│   │   │   ├── clarification_agent.py
│   │   │   ├── mapping_agent.py
│   │   │   ├── retrieval_agent.py
│   │   │   ├── ranking_agent.py
│   │   │   ├── explanation_agent.py
│   │   │   ├── fallback_agent.py
│   │   │   ├── memory_agent.py
│   │   │   ├── planner.py
│   │   │   ├── reviewer.py
│   │   │   └── orchestrator.py
│   │   ├── tools/
│   │   │   ├── catalog_tool.py
│   │   │   ├── product_tools.py
│   │   │   └── semantic_tool.py
│   │   ├── security/
│   │   │   └── guardrails.py
│   │   ├── governance/
│   │   │   └── audit.py
│   │   ├── scripts/
│   │   │   └── seed_catalog.py
│   │   ├── data/
│   │   │   └── products.json
│   │   ├── models/
│   │   ├── utils/
│   │   └── main.py
│   ├── tests/
│   ├── .env.example
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ChatBox.jsx
│   │   │   ├── ProductCard.jsx
│   │   │   └── AgentActivity.jsx
│   │   ├── App.jsx
│   │   └── index.css
│   └── package.json
├── docs/
│   └── ARCHITECTURE_V2.md
├── .gitignore
└── README.md
```

## 🚀 Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Dimple2706/shopmuse-ai.git
cd shopmuse-ai
```

### 2. Backend Setup

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 3. Environment Configuration

Create a `.env` file inside `backend` using `.env.example`.

Example configuration:

```env
MONGODB_URI=mongodb://localhost:27017/
MONGODB_DB=shopmuse
GROQ_API_KEY=your_groq_api_key
```

Use your MongoDB Atlas URI instead if you're using a cloud database.

Never commit actual API keys, database passwords, or `.env` files.

### 4. Initialize MongoDB and ChromaDB

Make sure MongoDB is accessible, then run:

```powershell
python -m app.scripts.seed_catalog
```

This imports products into MongoDB and generates ChromaDB embeddings.

The initial run may download an embedding model.

### 5. Start FastAPI

```powershell
uvicorn app.main:app --reload
```

Backend:

`http://127.0.0.1:8000`

API documentation:

`http://127.0.0.1:8000/docs`

### 6. Start React Frontend

Open another terminal:

```powershell
cd frontend
npm install
npm run dev
```

Frontend:

`http://localhost:5173`

## 🧪 Example API Request

**POST `/chat`**

```json
{
  "session_id": "shopmuse-demo-01",
  "message": "I need lightweight hiking equipment under $100 that is comfortable and suitable for someone with knee problems"
}
```

The API returns structured shopping results, including the interpreted intent, execution plan, Reviewer feedback, and recommended products with fit scores and explanations.

## 🧪 Testing and Validation

The project includes foundational tests for guardrail behavior.

Additional recommended integration tests include:

- Semantic retrieval relevance
- MongoDB–ChromaDB product consistency
- Budget and category constraint enforcement
- Session-memory refinement
- Planner–Reviewer replanning
- Unsupported product-claim prevention
- Zero-result fallback
- Database failure handling
- Prompt-injection resistance

Database seeding has been verified with 114 MongoDB product records and 114 ChromaDB vectors. Complete end-to-end security and reliability testing remains necessary.

## 🎯 Project Objective

To develop an intelligent, explainable, and context-aware conversational shopping assistant that combines autonomous agent coordination, semantic product discovery, structured catalog retrieval, and responsible recommendation generation.

## 🔮 Future Enhancements

- Real-time e-commerce marketplace integration
- Personalized recommendations across sessions
- Product images and shopping links
- Natural-language product comparison
- Advanced preference learning
- Persistent conversational memory
- Multilingual shopping assistance
- Recommendation evaluation dashboard
- Deployment and monitoring

---

**ShopMuse AI — Shopping, but make it magical. ✨**

Built as part of **PS-12: Conversational Shopping Assistant Agent**.
