import re
import asyncio
from sqlalchemy.future import select
from backend.database import AsyncSessionLocal, Course

async def run():
    async with AsyncSessionLocal() as session:
        res = await session.execute(select(Course.code, Course.description))
        found = 0
        for code, description in res.all():
            if not description: continue
            
            # Better regex: match Prerequisite(s): ... up to the next sentence starting with a capital letter, or end.
            match = re.search(r'(?:Prerequisite|Prereq|Requirements)[s]?\s*(?:for[a-z\sA-Z-]*)?:?\s*(.*?)(?:\.\s+(?=[A-Z])|$)', description, re.IGNORECASE | re.DOTALL)
            if match:
                prereq_text = match.group(1).strip()
                # Clean up newlines
                prereq_text = " ".join(prereq_text.split())
                if len(prereq_text) < 300 and prereq_text.lower() not in ["", "none", "."]:
                    print(code, ":", prereq_text)
                    found += 1
                if found > 10: break
                
asyncio.run(run())
