import asyncio
import json
import logging
from sqlalchemy import text
from backend.database import engine, Base, Course

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def init_db():
    logger.info("Initializing database...")
    async with engine.begin() as conn:
        # Create pgvector extension if it doesn't exist
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        
        # Create all tables
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database initialized successfully.")

async def populate_db():
    input_file = "scraper/courses_embedded.json"
    
    try:
        with open(input_file, 'r') as f:
            courses_data = json.load(f)
    except FileNotFoundError:
        logger.error(f"{input_file} not found. Ensure scrape.py and embed.py have run.")
        return

    from backend.database import AsyncSessionLocal
    
    logger.info(f"Populating database with {len(courses_data)} courses...")
    
    async with AsyncSessionLocal() as session:
        for course_data in courses_data:
            course = Course(
                code=course_data['code'],
                name=course_data['name'],
                subject=course_data['subject'],
                description=course_data['description'],
                embedding=course_data.get('embedding')
            )
            session.add(course)
        
        await session.commit()
        
    logger.info("Database population complete.")

async def main():
    await init_db()
    await populate_db()

if __name__ == "__main__":
    asyncio.run(main())
