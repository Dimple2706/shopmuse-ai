# 🛍️ ShopMuse AI

### Conversational Shopping Assistant using a Planner–Reviewer Multi-Agent Architecture

ShopMuse AI is an **agentic conversational shopping assistant** that helps users discover relevant products through natural-language queries.

Instead of relying on a single recommendation model, ShopMuse uses a **multi-agent workflow** where specialized agents handle query understanding, catalog mapping, retrieval, ranking, explanation, memory, fallback handling, planning, and review.

The system follows a **Planner → Execute → Reviewer → Replan** workflow to make recommendations more reliable and adaptable to user preferences.

---

## ✨ Key Features

* 💬 Natural-language conversational shopping
* 🤖 Multi-agent recommendation architecture
* 🧠 Planner–Reviewer workflow
* 🔄 Automatic replanning when requirements cannot be satisfied
* 🔍 Product retrieval and ranking
* 🎯 Preference-aware recommendations
* 💡 Evidence-based "Why this?" explanations
* 🧠 Session memory for conversational context
* 🛟 Fallback recommendations for difficult/impossible queries
* 🛒 Interactive product cards
* 📋 Product details view
* 🎀 Responsive pink-themed shopping interface
* ⚡ FastAPI backend
* ⚛️ React + Vite frontend
* 📊 Agent workflow designed for observability and debugging

---

# 🏗️ System Architecture

```text
                         ┌───────────────┐
                         │     USER      │
                         └───────┬───────┘
                                 │
                                 ▼
                     ┌─────────────────────┐
                     │    React + Vite     │
                     │     Frontend        │
                     └──────────┬──────────┘
                                │
                                ▼
                     ┌─────────────────────┐
                     │     FastAPI API     │
                     └──────────┬──────────┘
                                │
                                ▼
                 ┌────────────────────────────┐
                 │        ORCHESTRATOR        │
                 │                            │
                 │ Planner → Agents →         │
                 │ Reviewer → Replanning      │
                 └─────────────┬──────────────┘
                               │
       ┌───────────────────────┼──────────────────────┐
       │                       │                      │
       ▼                       ▼                      ▼
┌───────────────┐      ┌────────────────┐     ┌───────────────┐
│ Query / Intent│      │ Catalog &      │     │ Session       │
│ Understanding │      │ Retrieval      │     │ Memory        │
└───────────────┘      └───────┬────────┘     └───────────────┘
                               │
                               ▼
                       ┌───────────────┐
                       │    Ranking    │
                       │     Agent     │
                       └───────┬───────┘
                               │
                               ▼
                       ┌───────────────┐
                       │ Explanation   │
                       │     Agent     │
                       └───────┬───────┘
                               │
                               ▼
                       ┌───────────────┐
                       │   Reviewer    │
                       │     Agent     │
                       └───────┬───────┘
                               │
                     ┌─────────┴─────────┐
                     │                   │
                  APPROVE              REJECT
                     │                   │
                     ▼                   ▼
                 Results UI           Re-plan
                                         │
                                         └──────► Planner
```

---

# 🤖 Multi-Agent Architecture

ShopMuse divides the shopping task into specialized agents.

### 1. Query Ingestion Agent

Receives and preprocesses the user's natural-language shopping request.

**Example:**

> "I need lightweight hiking products under $50."

---

### 2. Intent Extraction Agent

Extracts important shopping requirements such as:

* Category
* Budget
* Activity
* Product attributes
* Preferences
* Constraints

Example:

```text
Category: Hiking
Budget: <$50
Preference: Lightweight
```

---

### 3. Clarification Agent

Handles ambiguous queries and identifies information that may be required before making recommendations.

For example:

```text
User:
"I need something good for hiking."

System:
"What is your preferred budget?"
```

---

### 4. Catalog Mapping Agent

Maps natural-language requirements to attributes available in the product catalog.

For example:

```text
"lightweight"
        ↓
weight attribute

"waterproof"
        ↓
waterproof attribute
```

This allows the system to connect conversational requirements with structured catalog data.

---

### 5. Candidate Retrieval Agent

Retrieves products that potentially satisfy the user's requirements.

The retrieval stage narrows the catalog down to relevant candidates before ranking.

---

### 6. Ranking Agent

Ranks retrieved candidates according to factors such as:

* User preferences
* Budget
* Category relevance
* Product attributes
* Requirement matching

The highest-quality candidates are presented to the user.

---

### 7. Explanation Agent

Generates explanations for why a product was recommended.

The explanation is grounded in available product information and recommendation evidence rather than inventing unsupported product attributes.

Example:

```text
✓ Within your $50 budget
✓ Lightweight
✓ Suitable for hiking
```

---

### 8. Reviewer Agent

Reviews the generated recommendation plan and checks whether the user's requirements can actually be satisfied.

The Reviewer can identify unsupported or unavailable requirements.

---

### 9. Planner Agent

Creates the recommendation plan and coordinates the shopping workflow.

The Planner can also create a revised plan when the Reviewer rejects the original plan.

---

### 10. Fallback Agent

Handles cases where the exact request cannot be satisfied.

Instead of returning no result, ShopMuse can provide the closest available alternatives and explain the limitation.

---

### 11. Session Memory Agent

Maintains relevant conversational context so that subsequent queries can build on previous preferences.

Example:

```text
User:
"Show me hiking products under $50."

User:
"Make it cheaper."

System:
Updates the existing shopping context
instead of treating the second query independently.
```

---

# 🔄 Planner–Reviewer Workflow

The core agentic behavior of ShopMuse is the **Planner–Reviewer loop**.

```text
User Query
    │
    ▼
Planner
    │
    ▼
Agent Execution
    │
    ▼
Recommendations
    │
    ▼
Reviewer
    │
    ├──────────────► APPROVED
    │                    │
    │                    ▼
    │               Final Results
    │
    └──────────────► REJECTED
                         │
                         ▼
                     Re-planning
                         │
                         ▼
                       Planner
```

### Example

User requests:

> "I need a waterproof, lightweight and comfortable hiking product under $50."

If the catalog cannot satisfy all requirements, the Reviewer identifies the unsupported constraint.

The Planner then revises the plan rather than blindly returning an invalid recommendation.

```text
Initial Requirements
        │
        ▼
Waterproof + Lightweight + Comfortable
        │
        ▼
     Reviewer
        │
        ▼
Waterproof requirement unavailable
        │
        ▼
      Re-plan
        │
        ▼
Lightweight + Comfortable
        │
        ▼
Updated Recommendations
```

This demonstrates that the system is **adaptive rather than a simple single-pass recommender**.

---

# 🧠 Example Interaction

### User

```text
I need lightweight hiking products under $50.
```

### ShopMuse

```text
Intent:
Hiking

Budget:
$50

Preference:
Lightweight
```

The system retrieves and ranks relevant products and displays them through interactive product cards.

Users can then:

* View product details
* See why a product was recommended
* Continue the conversation
* Modify their preferences

---

# 🛟 Fallback Handling

ShopMuse is designed to handle cases where the exact request cannot be fulfilled.

For example:

```text
User:
"Show me hiking gear under $10."
```

If there are no suitable products under the requested budget, the system can switch to a fallback strategy and provide the closest relevant alternatives instead of failing silently.

This makes the conversational experience more robust.

---

# 💡 Explainability

Each recommendation can provide a **"Why this?"** explanation.

The explanation focuses on attributes supported by the catalog and recommendation process.

Example:

```text
Why this product?

✓ Matches hiking category
✓ Fits your budget
✓ Lightweight
✓ Matches your requested preferences
```

The system avoids presenting unsupported product characteristics as facts.

---

# 🎨 Frontend

The frontend is built with **React and Vite**.

### Main UI components

* Conversational shopping interface
* Product cards
* Product details modal
* Recommendation explanations
* Interactive controls
* Responsive layout
* Pink / feminine shopping aesthetic

---

# ⚙️ Backend

The backend uses **FastAPI** to expose the shopping assistant functionality.

The backend coordinates:

```text
User Request
     ↓
FastAPI
     ↓
Orchestrator
     ↓
Multi-Agent Workflow
     ↓
Recommendation Response
     ↓
Frontend
```

---

# 📁 Project Structure

```text
shopmuse-ai/
│
├── backend/
│   └── app/
│       ├── agents/
│       │   ├── clarification_agent.py
│       │   ├── explanation_agent.py
│       │   ├── mapping_agent.py
│       │   ├── orchestrator.py
│       │   ├── planner.py
│       │   ├── ranking_agent.py
│       │   ├── retrieval_agent.py
│       │   ├── reviewer.py
│       │   └── ...
│       │
│       ├── data/
│       │   └── products.json
│       │
│       └── main.py
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   └── ProductCard.jsx
│   │   ├── App.jsx
│   │   └── index.css
│   │
│   └── package.json
│
├── .gitignore
└── README.md
```

---

# 🛠️ Tech Stack

| Layer           | Technology         |
| --------------- | ------------------ |
| Frontend        | React              |
| Build Tool      | Vite               |
| Styling         | CSS                |
| Backend         | FastAPI            |
| Language        | Python             |
| Product Data    | JSON               |
| Architecture    | Multi-Agent System |
| Workflow        | Planner–Reviewer   |
| Version Control | Git + GitHub       |

---

# 🚀 Running the Project Locally

## 1. Clone the repository

```bash
git clone https://github.com/Dimple2706/shopmuse-ai.git
cd shopmuse-ai
```

## 2. Backend Setup

Navigate to the backend:

```bash
cd backend
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

The backend will run on:

```text
http://127.0.0.1:8000
```

---

## 3. Frontend Setup

Open another terminal and navigate to:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

The frontend will be available at:

```text
http://localhost:5173
```

---

# 🧪 Testing Scenarios

ShopMuse was tested against multiple conversational scenarios.

| Scenario                | Expected Behavior          |
| ----------------------- | -------------------------- |
| Normal shopping query   | Relevant recommendations   |
| Budget constraint       | Budget-aware ranking       |
| Multiple preferences    | Multi-constraint retrieval |
| Ambiguous query         | Clarification              |
| Unsupported requirement | Reviewer identifies issue  |
| Changed preference      | Planner replans            |
| Impossible budget       | Fallback recommendations   |
| "Why this?"             | Evidence-based explanation |
| Follow-up query         | Session context maintained |

---

# 🔍 Why ShopMuse is Agentic

Traditional recommendation systems often follow a fixed pipeline:

```text
Query → Search → Results
```

ShopMuse instead uses:

```text
Query
  ↓
Planning
  ↓
Specialized Agents
  ↓
Retrieval
  ↓
Ranking
  ↓
Review
  ↓
Replanning if required
  ↓
Explanation
  ↓
Results
```

The system can therefore **reason about requirements, evaluate its own recommendation plan, and adapt the workflow when constraints cannot be satisfied**.

---

# 🎯 Project Objectives

The project demonstrates:

* Agentic system design
* Multi-agent coordination
* Planning and task decomposition
* Reviewer-based validation
* Dynamic replanning
* Conversational memory
* Product retrieval and ranking
* Explainable recommendations
* Fallback strategies
* Full-stack AI application development

---

# 🔮 Future Scope

Possible future improvements include:

* Real-time e-commerce APIs
* Larger product catalogs
* Vector database integration
* User accounts and persistent preferences
* Price tracking
* Product comparison
* Shopping-cart integration
* Personalized recommendation models
* Advanced observability dashboards
* Production deployment
* Human-in-the-loop review

---

# 👩‍💻 Author

**Dimple Bhojwani**

Computer Engineering
VESIT

### GitHub

`https://github.com/Dimple2706/shopmuse-ai`

---

## ⭐ Project Summary

**ShopMuse AI is a conversational, multi-agent shopping assistant that combines planning, retrieval, ranking, explanation, memory, review, and dynamic replanning to provide adaptive product recommendations through a simple conversational interface.**
