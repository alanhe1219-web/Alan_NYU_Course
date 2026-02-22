# Production Deployment Guide

You can absolutely deploy the NYU Course Search application to the cloud so anyone can access it! Because this application utilizes both a Next.js (React) front-end, a heavy Machine Learning Python backend (`sentence-transformers`), and a vector database (Postgres `pgvector`), there are two main ways to deploy this.

## Option 1: The Managed Cloud Route (Easiest & Most Reliable)
This splits the application across platforms specialized for each task.

### 1. Frontend: Vercel
Vercel is the creator of Next.js and hosts it flawlessly for free.
- Push your code to GitHub.
- Go to [Vercel](https://vercel.com/), create a new project, and import your GitHub repository.
- Set the **Root Directory** to `frontend`.
- Click **Deploy**. Vercel will automatically build and host the React interface.

### 2. Database: Supabase Database (or Neon)
You need a PostgreSQL database that supports the `pgvector` extension.
- Create a free account on [Supabase](https://supabase.com/) or [Neon.tech](https://neon.tech/).
- Create a new project. Both providers have `pgvector` enabled out of the box!
- Copy the **Postgres Connection URI**.

### 3. Backend: Railway or Render
Your Python FastAPI backend is heavy because it loads an AI ML model (`nomic-embed-text`) into memory.
- Go to [Railway](https://railway.app/) or [Render](https://render.com/).
- Connect your GitHub repo. Set the Root Directory to `/`.
- In the environment variables, add `DATABASE_URL` (paste the Supabase URI) and `REDIS_URL` (if you add a Redis add-on in Railway).
- Set the Start Command to: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`

---

## Option 2: The Single VPS Route (AWS / DigitalOcean / Linode)
If you prefer to manage everything on a single Linux server (A "Virtual Private Server" or VPS), you can rent a $10-$20/month Ubuntu server on DigitalOcean, AWS EC2, or Hetzner.

I've written production Dockerfiles and a `docker-compose.prod.yml` for you!

### Steps on your Ubuntu VPS:
1. SSH into your server: `ssh root@your-server-ip`
2. Install Docker and Docker Compose.
3. Clone your repository: `git clone https://github.com/alanhe1219-web/Alan_NYU_Course.git`
4. Enter the folder: `cd Alan_NYU_Course`
5. Run the production stack:
```bash
docker-compose -f docker-compose.prod.yml up -d --build
```

This will automatically:
- Build the optimized Next.js frontend image.
- Build the Python FastAPI image (and download the Machine Learning model).
- Start the `pgvector` database and Redis cache.
- Network them all together on port `80` (Standard HTTP).

*Note: Since the Python container downloads a multi-hundred-megabyte ML model and runs pgvector, we recommend a server with at least 4GB of RAM.*
