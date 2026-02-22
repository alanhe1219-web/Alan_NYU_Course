import asyncio
from backend.live_scraper import fetch_live_course_details
print(asyncio.run(fetch_live_course_details("HOU-UF 9101")))
print(asyncio.run(fetch_live_course_details("CSCI-UA 473")))
