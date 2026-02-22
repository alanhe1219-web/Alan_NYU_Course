import asyncio
from backend.live_scraper import fetch_live_course_details
async def run():
    print("HOU-UF 9101:", await fetch_live_course_details("HOU-UF 9101"))
    print("CSCI-UA 102:", await fetch_live_course_details("CSCI-UA 102"))
    print("CSCI-UA 473:", await fetch_live_course_details("CSCI-UA 473"))

asyncio.run(run())
