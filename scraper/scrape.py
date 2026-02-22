import asyncio
import aiohttp
from bs4 import BeautifulSoup
import json
import logging
import os
from typing import List, Dict

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

BASE_URL = "https://bulletins.nyu.edu"
COURSES_URL = f"{BASE_URL}/courses/"

async def fetch_page(session: aiohttp.ClientSession, url: str) -> str:
    """Fetches a page asynchronously."""
    async with session.get(url, ssl=False) as response:
        response.raise_for_status()
        return await response.text()

async def get_course_subjects(session: aiohttp.ClientSession) -> List[Dict[str, str]]:
    """Scrapes the main courses page to get all subject URLs."""
    logger.info(f"Fetching main courses page: {COURSES_URL}")
    html = await fetch_page(session, COURSES_URL)
    soup = BeautifulSoup(html, 'html.parser')
    
    subjects = []
    # Find all links that go to /courses/
    links = soup.find_all('a')
    for link in links:
        href = link.get('href', '')
        # Only take subject links like /courses/acct_gb/ (ignore basic /courses/)
        if href.startswith('/courses/') and len(href) > 9 and not href.endswith('.pdf'):
            name = link.text.strip()
            if name and "Download" not in name:
                subjects.append({
                    "name": name,
                    "url": f"{BASE_URL}{href}"
                })
    
    # Deduplicate subjects based on URL
    unique_subjects = {s['url']: s for s in subjects}.values()
    return list(unique_subjects)

async def get_courses_for_subject(session: aiohttp.ClientSession, subject: Dict[str, str]) -> List[Dict[str, str]]:
    """Scrapes all courses for a specific subject."""
    logger.info(f"Fetching courses for subject: {subject['name']}")
    try:
        html = await fetch_page(session, subject['url'])
        soup = BeautifulSoup(html, 'html.parser')
        
        courses = []
        # Find the courseblocks
        course_blocks = soup.find_all('div', class_='courseblock')
        for block in course_blocks:
            code_span = block.find('span', class_='detail-code')
            title_span = block.find('span', class_='detail-title')
            desc_div = block.find('div', class_='courseblockextra')
            
            if code_span and title_span:
                code = code_span.text.strip()
                name = title_span.text.strip()
                desc = desc_div.text.strip() if desc_div else ""
                
                courses.append({
                    "code": code,
                    "name": name,
                    "description": desc,
                    "subject": subject['name']
                })
                
        return courses
    except Exception as e:
        logger.error(f"Failed to fetch or parse {subject['name']}: {e}")
        return []

async def scrape_all_courses() -> List[Dict[str, str]]:
    """Main function to scrape all subjects and courses."""
    async with aiohttp.ClientSession() as session:
        subjects = await get_course_subjects(session)
        logger.info(f"Found {len(subjects)} subjects. Starting to scrape courses...")
        
        all_courses = []
        # Process subjects in batches to avoid overwhelming the server
        batch_size = 10
        for i in range(0, len(subjects), batch_size):
            batch = subjects[i:i + batch_size]
            tasks = [get_courses_for_subject(session, sub) for sub in batch]
            results = await asyncio.gather(*tasks)
            for res in results:
                all_courses.extend(res)
            # Small delay between batches
            await asyncio.sleep(1)
            logger.info(f"Processed {min(i + batch_size, len(subjects))}/{len(subjects)} subjects...")
            
        return all_courses

if __name__ == "__main__":
    courses = asyncio.run(scrape_all_courses())
    logger.info(f"Total courses scraped: {len(courses)}")
    
    # Save to file temporarily as our database representation/seed
    os.makedirs('scraper', exist_ok=True)
    with open('scraper/courses_raw.json', 'w') as f:
        json.dump(courses, f, indent=2)
    logger.info("Saved raw courses to scraper/courses_raw.json")
