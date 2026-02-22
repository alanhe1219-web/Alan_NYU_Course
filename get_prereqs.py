import asyncio
import re
from sqlalchemy.future import select
from backend.database import AsyncSessionLocal, Course

async def run():
    async with AsyncSessionLocal() as session:
        res = await session.execute(select(Course.code, Course.description))
        found = 0
        for code, description in res.all():
            if not description: continue
            
            # More flexible prerequisite regex
            match = re.search(r'(?:Prerequisite|Prereq)[s]?\s*:?\s*(.*?)(?=(?:\. [A-Z])|$)', description, re.IGNORECASE | re.DOTALL)
            if match:
                prereq_text = match.group(1).strip()
                # Exclude if it's too long (maybe grabbed the rest of the text)
                if len(prereq_text) < 200:
                    print(code, ":", prereq_text)
                    found += 1
                if found > 15: break
                
asyncio.run(run())
