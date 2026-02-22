# NYU Course Search (Neo-Editorial Edition)

A beautifully brutalist, semantic search engine for NYU courses powered by AI embeddings, FastAPI, PostgreSQL, and Next.js.


## 🌟 The Vision
This project radically redesigns academic software. Breaking away from generic, clinical interfaces, it uses a **Neo-Editorial Brutalist** aesthetic, featuring high-contrast stark layouts, dramatic oversized typography (`Cormorant Garamond` paired with `Outfit`), and buttery-smooth `framer-motion` reveals to make discovering classes feel like flipping through a premium art archive.

## 🚀 Tech Stack
- **Frontend**: Next.js (App Router), React, Tailwind CSS, Framer Motion, Lucide React
- **Backend**: Python FastAPI, SQLAlchemy, Redis
- **Database**: PostgreSQL with `pgvector`
- **Machine Learning**: `sentence-transformers` utilizing `nomic-ai/nomic-embed-text-v1.5`
- **Environment**: Docker & Colima

## ✨ Features
1. **Semantic Knowledge Retrieval**: Don't just search by title. Search by meaning (e.g. "History of Renaissance Art" or "Math for Machine Learning"). The pgvector cosine similarity engine understands intent.
2. **Neo-Editorial Interface**: A distinctive, high-end "Academic Archive" aesthetic focusing on raw typography and bold composition.
3. **The Curriculum Planner**: An integrated Next.js interface to save, curate, and review courses you intend to take, entirely backed by relational PostgreSQL tables.
4. **Fluid Motion**: Staggered list reveals and dynamic layout changes powered by Framer Motion.

## 🛠️ Local Setup

### 1. Requirements
- Python 3.10+
- Node.js 18+
- Docker (or OrbStack/Colima) for PostgreSQL

### 2. Database & Data Pipeline
Start the `pgvector` enabled PostgreSQL database and Redis:
```bash
docker-compose up -d
```

Since the massive 300MB `courses_embedded.json` file is omitted from source control, you must generate the data and initial database yourself:

```bash
# 1. Scrape the NYU Bulletin
python scraper/scrape.py

# 2. Generate Nomic Embeddings (requires HuggingFace token and downloads ML model)
python scraper/embed.py

# 3. Populate Postgres Database
python backend/populate.py

# 4. Initialize Planner Tables
python backend/init_planner.py
```

### 3. Start the FastAPI Backend
```bash
source venv/bin/activate
pip install -r backend/requirements.txt
export PYTHONPATH=$PYTHONPATH:$(pwd)
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Start the Next.js Frontend
```bash
npm install
npm run dev
```

Visit `http://localhost:3000` to access the Academic Archive.

## 📝 Roadmap
- `@nyu.edu` restricted NextAuth authentication barrier.
- Live course status scraping (fetching real-time prerequisites and professor data from NYU's beta APIs).
- Search relevance "Thumbs Up" ML feedback loop.
