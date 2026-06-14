# CreatorCareer AI

**From Content Creator to Digital Entrepreneur**

CreatorCareer AI is an AI-powered creator business intelligence platform built for the **July Challenge: Reimagine Creative Industries with AI**. It helps content creators move from random content posting to a structured creator-business workflow using AI content planning, market analysis, product validation, ethical monetization checking, seven-agent business strategy, downloadable PDF reporting, and saved business history.

> CreatorCareer AI is not just an AI content generator. It is a creator business operating system that helps creators move from content idea to market opportunity, product validation, ethical monetization, 7-agent business strategy, downloadable report, and saved business history.

---

## Live Links

| Resource | Link |
|---|---|
| Live Frontend | https://creator-career-ai.vercel.app |
| Live Backend | https://creatorcareer-ai.onrender.com |
| Backend API Docs | https://creatorcareer-ai.onrender.com/docs |
| GitHub Repository | https://github.com/yousunlotif-bappy/CreatorCareer-AI |

---

## Project Summary

Many creators can produce content, but they struggle to turn their niche, audience, and creativity into a real digital business. CreatorCareer AI solves this by guiding creators through a complete business-building workflow:

```text
Creator Profile
→ AI Content Package
→ Market Analysis
→ Product Validation
→ Affiliate & Dropshipping Roadmap
→ Ethical Monetization Checker
→ 7-Agent Creator Business Dashboard
→ PDF Business Report
→ Saved History
```

The platform gives creators practical outputs such as content scripts, product ideas, business-readiness scores, ethical risk checks, affiliate strategies, 30-day action plans, six-month roadmaps, and downloadable reports.

---

## Selected Challenge Theme

**Reimagine Creative Industries with AI**

CreatorCareer AI fits this theme by helping creators work smarter, create faster, and transform creative content into structured digital business opportunities. It demonstrates how AI can act as a creative partner and business assistant rather than only a text generator.

---

## Problem Statement

Content creators often face these real-world challenges:

- They do not know what content to create next.
- They struggle to connect content with product or business opportunities.
- They do not know whether a product idea matches their audience.
- They need guidance on affiliate marketing, dropshipping, and digital products.
- They may accidentally use misleading claims, missing affiliate disclosures, or risky monetization language.
- They lack a structured weekly and six-month growth roadmap.

Most available AI tools only generate captions, scripts, or hashtags. CreatorCareer AI goes further by connecting creativity with business strategy, validation, ethics, and execution planning.

---

## Solution

CreatorCareer AI provides a complete creator-to-business workflow. A creator enters their niche, audience, platform, follower count, business interest, product idea, and income goal. The system then generates structured AI-powered insights, scores, recommendations, and action plans.

The platform helps creators answer:

- What should I create?
- What product can I sell?
- Is my audience a good fit for this idea?
- What is the market opportunity?
- How can I monetize ethically?
- What should I do in the next 7 days?
- What should my 6-month business roadmap look like?

---

## Key Features

### 1. Creator Profile Analyzer

Collects creator information and analyzes the creator’s business readiness.

**Inputs**

- Niche
- Platform
- Audience
- Region
- Followers
- Skill level
- Business interest
- Income goal
- Available time
- Current challenge

**Outputs**

- Creator summary
- Creator stage
- Niche positioning
- Audience opportunity
- Business opportunity
- Readiness score
- Recommended next action

---

### 2. AI Content Package Generator

Turns one topic or story idea into a full content package.

**Outputs**

- Viral title ideas
- Hook
- Voiceover script
- Caption
- Hashtags
- Thumbnail text
- CTA
- Scene breakdown
- B-roll ideas
- Editing notes
- AI video generation prompt

---

### 3. AI Market Analysis

Analyzes the creator’s niche, audience, region, platform, and business direction to suggest product opportunities.

**Outputs**

- Market summary
- Demand level
- Competition level
- Recommended products
- Digital product ideas
- Affiliate product ideas
- Dropshipping product ideas
- Best platforms
- Risk level
- Opportunity score
- Next best action

---

### 4. Product Validation Score

Validates whether a product idea is worth testing before launch.

**Scoring logic**

```text
Audience Fit                 25
Market Demand                20
Competition Level            15
Content Promotion Fit        20
Profit Potential             10
Ease of Starting             10
--------------------------------
Total                       100
```

**Outputs**

- Total validation score
- Score breakdown
- Strengths
- Risks
- Recommendation
- Validation checklist
- Next action

---

### 5. Affiliate & Dropshipping Roadmap

Creates a practical monetization roadmap for creators who want to start with affiliate products, dropshipping, or low-risk monetization ideas.

**Outputs**

- Affiliate product ideas
- Dropshipping product ideas
- Best product fit
- Content promotion plan
- Supplier research checklist
- 30-day roadmap
- Risk analysis
- Ethical disclosure guidance
- Next best action

---

### 6. Ethical Monetization Checker

Checks promotional content for ethical and trust-related risks.

**Detects**

- Missing affiliate disclosure
- Misleading claims
- Overpromising
- Fake urgency
- Clickbait language
- Risky income or guarantee claims

**Outputs**

- Ethical score
- Risk level
- Issues found
- Disclosure status
- Safer rewritten version
- Recommended disclosure
- Platform note
- Next best action

---

### 7. 7-Agent Creator Business Dashboard

The 7-agent dashboard is the core strategy engine of the project.

**Agents**

1. Creator Business Readiness Agent
2. Niche-to-Product Fit Agent
3. Audience-to-Market Matching Agent
4. Content-to-Commerce Roadmap Agent
5. Ethical Monetization Checker Agent
6. Product Validation Checklist Agent
7. 6-Month Creator-to-Business Roadmap Agent

**Each agent returns**

- Score
- Status
- Reason
- Recommendation
- Next action

---

### 8. PDF Business Report Generator

Generates a downloadable creator business report.

**Report sections**

- Creator profile summary
- Overall business opportunity score
- 7-agent analysis summary
- Product validation summary
- Ethical monetization note
- Next 7 days action plan
- 6-month creator-to-business roadmap
- MVP data note

---

### 9. Saved History

Stores and displays previous creator records and generated outputs.

**Saved records include**

- Creator profiles
- Content packages
- Market analysis results
- Product validation scores
- Affiliate roadmaps
- Ethical check results
- 7-agent reports
- PDF reports

This proves the project is not only a static frontend demo. It is a backend-connected MVP with database-backed history.

---

## AI Approach and Architecture

CreatorCareer AI uses a modular AI-ready backend architecture. The project is designed to support IBM Granite through Ollama during local development and can be extended to IBM watsonx for future cloud deployment.

Current AI approach:

- Local explainable AI logic for reliable MVP outputs
- IBM Granite/Ollama-ready architecture
- LangChain/Ollama-ready service layer
- Fallback logic for deployed environments where local Ollama is not available
- Structured scoring engine for product validation and business readiness
- Seven-agent business reasoning workflow

Important deployment note:

> The local development environment can use IBM Granite through Ollama. The live Render deployment may use fallback explainable AI logic if Ollama is not running on the hosted server. The architecture is designed to be watsonx-ready for future cloud AI integration.

---

## System Architecture

```text
Next.js Frontend
        ↓
FastAPI Backend
        ↓
AI / Granite / Ollama-Ready Layer
        ↓
7-Agent Business Logic
        ↓
Scoring Engine
        ↓
Supabase / PostgreSQL Database
        ↓
PDF Report Generator
        ↓
Saved History + Downloadable Reports
```

---

## User Workflow

```text
1. User opens CreatorCareer AI
2. User fills Creator Profile
3. AI analyzes creator niche, audience, and goals
4. User generates AI Content Package
5. User runs Market Analysis
6. User validates a product idea
7. User creates Affiliate/Dropshipping Roadmap
8. User checks Ethical Monetization risk
9. User runs the 7-Agent Business Dashboard
10. User downloads a PDF Business Report
11. User checks Saved History
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Next.js, React, TypeScript |
| Styling | Tailwind CSS |
| Backend | Python, FastAPI |
| AI Layer | IBM Granite/Ollama-ready logic, LangChain-ready service layer |
| Database | Supabase / PostgreSQL |
| Report Generation | Python PDF report generator |
| Deployment | Vercel frontend, Render backend |
| Documentation | Markdown docs, IBM Bob usage logs, screenshots |
| Icons/UI | Lucide React |

---

## Project Structure

```text
CreatorCareer-AI/
│
├── backend/
│   ├── main.py
│   ├── routes/
│   │   ├── profile.py
│   │   ├── content.py
│   │   ├── market.py
│   │   ├── validation.py
│   │   ├── affiliate.py
│   │   ├── ethical.py
│   │   ├── agents.py
│   │   ├── reports.py
│   │   ├── database.py
│   │   └── ai.py
│   ├── services/
│   │   ├── ai_service.py
│   │   ├── local_llm_service.py
│   │   ├── database.py
│   │   ├── report_generator.py
│   │   └── proof.py
│   ├── requirements.txt
│   ├── supabase_schema.sql
│   └── .env.example
│
├── frontend/
│   ├── app/
│   │   ├── dashboard/
│   │   ├── profile/
│   │   ├── content-package/
│   │   ├── market-analysis/
│   │   ├── product-validation/
│   │   ├── affiliate-roadmap/
│   │   ├── ethical-checker/
│   │   ├── seven-agent-dashboard/
│   │   ├── reports/
│   │   ├── history/
│   │   └── settings/
│   ├── components/
│   │   ├── AiProofCard.tsx
│   │   └── LiveSystemStatus.tsx
│   ├── lib/
│   │   ├── api.ts
│   │   └── dashboard-data.ts
│   ├── public/
│   ├── package.json
│   └── .env.example
│
├── docs/
│   ├── CreatorCareer-AI-MVP-Plan.md
│   ├── ibm-bob-planning-notes.md
│   ├── ibm-bob-usage-log.md
│   ├── mvp-scope.md
│   └── screenshots/
│
├── README.md
└── .gitignore
```

---

## API Endpoints

### Health and system

```text
GET  /
GET  /health
GET  /ai/health
GET  /db/health
GET  /db/overview
GET  /cors-debug
```

### Main modules

```text
POST /profile/analyze
POST /content/package
POST /market/analyze
POST /product/validate
POST /affiliate/roadmap
POST /ethical/check
POST /agents/run
POST /report/generate
```

### Database history

```text
GET /db/latest-creators
GET /db/latest-content
GET /db/latest-market-analysis
GET /db/latest-product-scores
GET /db/latest-affiliate-roadmaps
GET /db/latest-ethical-checks
GET /db/latest-seven-agent-reports
GET /db/latest-reports
```

---

## Environment Variables

### Backend `.env`

```env
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_key
SUPABASE_ANON_KEY=your_supabase_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_supabase_service_role_key

FRONTEND_URL=http://localhost:3000,https://creator-career-ai.vercel.app
BACKEND_PUBLIC_URL=http://localhost:8000

OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=granite3.3:2b
```

### Frontend `.env.local`

```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

For production on Vercel:

```env
NEXT_PUBLIC_API_BASE_URL=https://creatorcareer-ai.onrender.com
```

---

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/yousunlotif-bappy/CreatorCareer-AI.git
cd CreatorCareer-AI
```

### 2. Backend setup

```bash
cd backend
python -m venv venv
```

Activate virtual environment on Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create `.env` from `.env.example` and add Supabase credentials.

Run backend:

```bash
uvicorn main:app --reload
```

Backend runs at:

```text
http://localhost:8000
```

API docs:

```text
http://localhost:8000/docs
```

### 3. Frontend setup

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at:

```text
http://localhost:3000
```

---

## Deployment

### Backend deployment

Backend is deployed on Render.

Recommended Render settings:

```text
Root Directory: backend
Environment: Python
Build Command: pip install -r requirements.txt
Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT
```

Render environment variables:

```env
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
FRONTEND_URL=https://creator-career-ai.vercel.app,http://localhost:3000
BACKEND_PUBLIC_URL=https://creatorcareer-ai.onrender.com
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=granite3.3:2b
```

### Frontend deployment

Frontend is deployed on Vercel.

Recommended Vercel settings:

```text
Root Directory: frontend
Framework: Next.js
Build Command: npm run build
Install Command: npm install
Output Directory: .next
```

Vercel environment variable:

```env
NEXT_PUBLIC_API_BASE_URL=https://creatorcareer-ai.onrender.com
```

---

## IBM Bob Usage

IBM Bob was used as the primary development tool throughout the project workflow.

IBM Bob helped with:

- Project planning and MVP scope definition
- Architecture design
- Frontend page structure
- Backend route planning
- API workflow planning
- AI prompt and module logic design
- Supabase/PostgreSQL data planning
- Debugging deployment and CORS issues
- README and documentation planning
- Demo flow preparation

Evidence is included in the `docs/` folder:

```text
docs/ibm-bob-usage-log.md
docs/ibm-bob-planning-notes.md
docs/CreatorCareer-AI-MVP-Plan.md
docs/mvp-scope.md
docs/screenshots/
```

---

## Screenshots

Dashboard screenshot:

```text
docs/screenshots/CCAI-dashboard.png
```

7-Agent dashboard screenshot:

```text
docs/screenshots/7agent.png
```

IBM Bob planning screenshots:

```text
docs/screenshots/ibm-bob-day1-planning.png
docs/screenshots/ibm-bob-day2-planning.png
docs/screenshots/ibm-bob-day3-planning.png
...
docs/screenshots/ibm-bob-day10-planning.png
```

---

## Testing Checklist

### Backend tests

```text
GET  /
GET  /health
GET  /ai/health
GET  /db/health
GET  /db/overview
GET  /cors-debug
```

### Frontend pages

```text
/
/dashboard
/profile
/content-package
/market-analysis
/product-validation
/affiliate-roadmap
/ethical-checker
/seven-agent-dashboard
/reports
/history
/settings
```

### Full user flow

```text
1. Analyze Creator Profile
2. Generate Content Package
3. Run Market Analysis
4. Validate Product Idea
5. Generate Affiliate Roadmap
6. Run Ethical Checker
7. Run 7-Agent Dashboard
8. Generate PDF Report
9. Open Saved History
10. Confirm database records are visible
```

---

## Responsible AI and Ethics

CreatorCareer AI includes an Ethical Monetization Checker to support responsible creator monetization.

The system encourages:

- Transparent affiliate disclosure
- Safer promotional wording
- Avoiding exaggerated income claims
- Avoiding fake urgency
- Avoiding misleading product promises
- Building audience trust

The product validation and business scoring outputs are intended as decision-support tools, not guaranteed financial outcomes.

---

## Why This Project Matters

CreatorCareer AI supports real creators who want to build sustainable digital businesses. Instead of only generating content, it helps creators understand what to create, what to sell, how to validate ideas, how to monetize ethically, and how to follow a structured roadmap.

It helps creators move from:

```text
Random posting
```

to:

```text
Structured creator entrepreneurship
```

---

## Future Scope

Planned future improvements:

- Full IBM watsonx cloud integration
- Real-time market data APIs
- Creator account authentication
- Multi-user saved workspaces
- Advanced analytics dashboard
- A/B testing for hooks, titles, and thumbnails
- Direct social media scheduling integration
- Advanced PDF report templates
- Team collaboration features
- Multilingual creator support

---

## Project Status

Current status:

```text
✅ Frontend deployed
✅ Backend deployed
✅ Supabase database connected
✅ FastAPI docs available
✅ Main module pages available
✅ 7-agent dashboard implemented
✅ PDF report generator implemented
✅ Saved history implemented
✅ IBM Bob documentation included
✅ CORS configured for Vercel frontend
```

MVP status:

```text
Contest-ready MVP with creator-business workflow, AI-ready backend, database storage, PDF reporting, and professional dashboard UI.
```

---

## Author

**Rafik Hossain**  
Project: CreatorCareer AI  
GitHub: https://github.com/yousunlotif-bappy/CreatorCareer-AI

---

## License

This project is created for the IBM AI Builders July Challenge as an MVP/proof of concept. Licensing can be updated based on future open-source or commercial release plans.
