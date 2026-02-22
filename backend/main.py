from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import json
import redis.asyncio as redis
from sqlalchemy.future import select
from sentence_transformers import SentenceTransformer
import aiohttp
from backend.database import AsyncSessionLocal, Course, SavedCourse
import os

app = FastAPI(title="NYU Course Search API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Redis configuration
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
redis_client = redis.from_url(REDIS_URL, decode_responses=True)

# Load Embedding model
MODEL_NAME = "nomic-ai/nomic-embed-text-v1.5"
model = None

@app.on_event("startup")
async def startup_event():
    global model
    # Load model on startup to avoid lag on first request
    # Use general document prefix or search query prefix as specified by Nomic
    model = SentenceTransformer(MODEL_NAME, trust_remote_code=True)

class SearchQuery(BaseModel):
    query: str
    top_k: int = 20

class CourseResult(BaseModel):
    code: str
    name: str
    subject: Optional[str]
    description: Optional[str]
    similarity: float

@app.post("/search", response_model=List[CourseResult])
async def search_courses(request: SearchQuery):
    global model
    if not model:
        raise HTTPException(status_code=500, detail="Model not loaded")
        
    # Nomic expects "search_query: " prefix for searching
    embedded_query = model.encode([f"search_query: {request.query}"], convert_to_tensor=False)[0]
    
    async with AsyncSessionLocal() as session:
        # Cosine distance ordering using pgvector (<=>)
        # Higher similarity = lower distance
        stmt = select(
            Course,
            Course.embedding.cosine_distance(embedded_query.tolist()).label("distance")
        ).order_by("distance").limit(request.top_k)
        
        result = await session.execute(stmt)
        
        results = []
        for course, distance in result.all():
            results.append(CourseResult(
                code=course.code,
                name=course.name,
                subject=course.subject,
                description=course.description,
                similarity=1 - distance # Convert distance to similarity
            ))
            
        return results

@app.get("/course/{course_code}/details")
async def get_course_details(course_code: str):
    """
    Dynamically fetches course details (like professors, schedule, prereqs) using the NYU Class Search beta.
    Uses Redis to cache results for 1 day to prevent rate limiting.
    """
    cache_key = f"course_details:{course_code}"
    cached = await redis_client.get(cache_key)
    
    if cached:
        return json.loads(cached)
        
    # Query NYU Class search API or endpoints manually if available.
    # The actual implementation of scraping the dynamic details goes here.
    # For now, we return placeholder live data structure
    
    placeholder_data = {
        "course_code": course_code,
        "available_semesters": ["Fall 2026", "Spring 2026"],
        "professors": ["John Doe", "Jane Smith"],
        "prerequisites": "None",
        "live_status": "Available dynamically from bulletins.nyu.edu/class-search/"
    }
    
    await redis_client.setex(cache_key, 86400, json.dumps(placeholder_data))
    return placeholder_data

@app.post("/search/feedback")
async def submit_feedback(course_code: str, query: str, thumbs_up: bool):
    """
    Endpoint for users to rate search relevance. Usually saved to Postgres
    for evaluating the embeddings later.
    """
    # Placeholder for saving feedback to DB
    return {"status": "Feedback recorded", "course": course_code, "thumbs_up": thumbs_up}

class SaveCourseRequest(BaseModel):
    user_id: str
    course_code: str

@app.post("/planner/add")
async def add_to_planner(request: SaveCourseRequest):
    async with AsyncSessionLocal() as session:
        stmt = select(SavedCourse).where(
            SavedCourse.user_id == request.user_id,
            SavedCourse.course_code == request.course_code
        )
        result = await session.execute(stmt)
        if result.scalar_one_or_none():
            return {"status": "already saved"}
            
        saved = SavedCourse(user_id=request.user_id, course_code=request.course_code)
        session.add(saved)
        await session.commit()
        return {"status": "success"}

@app.post("/planner/remove")
async def remove_from_planner(request: SaveCourseRequest):
    async with AsyncSessionLocal() as session:
        stmt = select(SavedCourse).where(
            SavedCourse.user_id == request.user_id,
            SavedCourse.course_code == request.course_code
        )
        result = await session.execute(stmt)
        existing = result.scalar_one_or_none()
        if existing:
            await session.delete(existing)
            await session.commit()
            return {"status": "removed"}
        return {"status": "not found"}

@app.get("/planner/{user_id}", response_model=List[CourseResult])
async def get_planner(user_id: str):
    async with AsyncSessionLocal() as session:
        stmt = select(Course).join(SavedCourse, Course.code == SavedCourse.course_code).where(SavedCourse.user_id == user_id).order_by(SavedCourse.saved_at.desc())
        
        result = await session.execute(stmt)
        courses = result.scalars().all()
        
        return [
            CourseResult(
                code=c.code,
                name=c.name,
                subject=c.subject,
                description=c.description,
                similarity=1.0
            ) for c in courses
        ]

@app.get("/health")
async def health_check():
    return {"status": "ok"}
