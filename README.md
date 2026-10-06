# 🛍️ ShopMuse AI

### Conversational Shopping Assistant Agent

ShopMuse AI is an intelligent conversational shopping assistant that understands vague and evolving shopping requests, remembers user preferences during a session, retrieves relevant products, ranks them based on fit, explains recommendations, and recovers intelligently when no exact products are available.

---

## ✨ Problem Statement

Traditional e-commerce search requires users to provide structured filters such as category, price, brand, and features.

However, real users often search conversationally:

> "I need a birthday gift for my dad. He's turning 60, loves hiking, but has bad knees. My budget is around $100."

ShopMuse converts this natural-language request into structured shopping intent and uses it to discover suitable products.

---

## 🎯 Key Features

- 🧠 Natural-language intent extraction using Groq LLM
- 💬 Conversational follow-up handling
- 🧠 Session-level preference memory
- 🎯 Constraint and preference extraction
- 🗂️ Catalog attribute mapping
- 🔎 Candidate product retrieval
- 📊 Explainable product ranking
- ✨ AI-generated recommendation explanations
- 🚨 Zero-result detection
- 🔄 Intelligent fallback and budget relaxation
- 💗 Interactive shopping interface
- 🔍 "Why this product?" explanations
- 🛍️ Product detail modal
- 🛡️ Recommendation validation

---

## 🏗️ System Architecture

```text
                         User
                           │
                           ▼
                  ┌─────────────────┐
                  │  React Frontend │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │    FastAPI      │
                  │     Backend     │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │   Orchestrator  │
                  └────────┬────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
  Intent Agent       Memory Agent       Clarification
        │                  │                  │
        └──────────────────┼──────────────────┘
                           │
                           ▼
                  Catalog Mapping Agent
                           │
                           ▼
                 Candidate Retrieval
                           │
                           ▼
                    Ranking Agent
                           │
                           ▼
                  Explanation Agent
                           │
                           ▼
                   Reviewer Agent
                           │
                           ▼
                    Final Results
```

---

## 🤖 Agent Architecture

### 1. Query Ingestion Agent

Cleans and normalizes incoming user queries before processing.

### 2. Intent & Constraint Extraction Agent

Uses Groq LLM to extract:

- Product category
- Recipient
- Occasion
- Budget
- Preferences
- Confidence

### 3. Ambiguity & Clarification Agent

Determines whether sufficient information exists to perform a useful search.

If information is missing, it asks a targeted clarification question.

### 4. Catalog Attribute Mapping Agent

Maps conversational preferences to structured catalog attributes.

For example:

```text
"easy on the knees"
        ↓
joint-friendly
low-impact
supportive
```

### 5. Candidate Retrieval Agent

Searches the product catalog using structured attributes.

### 6. Ranking & Fit Scoring Agent

Ranks candidates using:

- Category relevance
- Preference matching
- Budget fit
- Product rating
- User refinement signals

### 7. Explanation Generation Agent

Uses Groq to generate natural-language explanations for recommendations.

### 8. Zero-Result & Fallback Agent

Detects dead ends and searches for close alternatives by relaxing constraints.

### 9. Session Memory Agent

Maintains conversational context across messages.

Example:

```text
"I need hiking products under $100"
                ↓
"make it lightweight"
                ↓
"actually make it cheaper"
```

The system remembers the hiking requirement and lightweight preference while updating the budget.

### 10. Orchestrator Agent

Coordinates the complete workflow and controls the execution sequence.

---

## 🔄 Example Conversation

### User

> I need something for my dad who's turning 60. He loves hiking but has bad knees. My budget is around $100.

### ShopMuse

Identifies:

```text
Recipient: Father
Occasion: Birthday
Category: Hiking
Preference: Joint-friendly
Budget: $100
```

The system retrieves and ranks suitable products.

---

### User

> Make it lightweight.

ShopMuse remembers the previous request and adds:

```text
Preference: Lightweight
```

The products are re-ranked.

---

### User

> Actually keep it below $60.

ShopMuse updates:

```text
Budget: $60
```

while retaining the previous shopping context.

---

## 🚨 Zero-Result Recovery

If a user requests:

> Hiking products under $10

and no exact products exist, ShopMuse does not simply return an empty result.

Instead:

```text
No exact results
       ↓
Identify constraint
       ↓
Relax budget
       ↓
Find closest alternatives
       ↓
Explain the change
```

---

## 🛠️ Technology Stack

### Frontend

- React
- Vite
- JavaScript
- CSS
- Lucide React

### Backend

- Python
- FastAPI
- Pydantic

### AI

- Groq API
- Llama / OpenAI open-weight models available through Groq

### Data

- JSON product catalog
- In-memory session memory

### Development

- Git
- GitHub
- VS Code

---

## 📁 Project Structure

```text
shopmuse-ai/
│
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
│   │   │
│   │   ├── data/
│   │   │   └── products.json
│   │   │
│   │   ├── models/
│   │   │   └── schemas.py
│   │   │
│   │   ├── tools/
│   │   │   └── catalog_tool.py
│   │   │
│   │   └── main.py
│   │
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── App.jsx
│   │   ├── index.css
│   │   └── main.jsx
│   │
│   └── package.json
│
├── docs/
│
├── .gitignore
└── README.md
```

---

## 🚀 Running the Project

### Backend

```bash
cd backend

python -m venv .venv

.venv\Scripts\Activate.ps1

pip install -r requirements.txt

uvicorn app.main:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

Swagger API documentation:

```text
http://127.0.0.1:8000/docs
```

---

### Frontend

Open another terminal:

```bash
cd frontend

npm install

npm run dev
```

Then open the Vite URL shown in the terminal.

---

## 🔐 Environment Variables

Create:

```text
backend/.env
```

Add:

```env
GROQ_API_KEY=your_api_key_here
```

Never commit `.env` to GitHub.

---

## 🧪 Example Test Cases

| Test                  | Input                | Expected Behaviour                    |
| --------------------- | -------------------- | ------------------------------------- |
| Basic search          | Hiking under $100    | Hiking recommendations                |
| Preference refinement | Make it lightweight  | Re-rank using lightweight preference  |
| Budget refinement     | Keep it below $60    | Update budget while retaining context |
| Ambiguous request     | Something for my dad | Ask for product category              |
| Natural language      | Easy on his knees    | Map to joint-friendly requirements    |
| Zero results          | Hiking under $10     | Suggest close alternatives            |
| Memory                | Make it cheaper      | Retain previous category/preferences  |
| Explanation           | Why this product?    | Show recommendation reasoning         |

---

## 🔮 Future Improvements

- Real e-commerce APIs
- Product image search
- Cross-session preference memory
- Visual product comparison
- Personalized recommendation learning
- Brand preferences
- Price-drop alerts
- Cart and checkout integration
- Vector-based semantic retrieval
- Multilingual shopping conversations

---

## 👩‍💻 Project

**ShopMuse AI — Conversational Shopping Assistant Agent**

Built as an autonomous AI agent system for conversational product discovery.
