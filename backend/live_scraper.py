import asyncio
import aiohttp
import logging

logger = logging.getLogger(__name__)

async def fetch_live_course_details(course_code: str):
    """
    Scrape live NYU Class Search (FOSE) API for real professors and prerequisites.
    """
    url = "https://bulletins.nyu.edu/class-search/api/?page=fose&route=search"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    # Try current and recent terms
    terms = ["1254", "1252", "1248", "1246", "1244", "1242", "1240", "1238"]
    
    professors = set()
    found_description = ""
    found_semesters = set()
    
    async with aiohttp.ClientSession() as session:
        for term in terms:
            data = {"other": {"srcdb": term}, "criteria": [{"field": "keyword", "value": course_code}]}
            try:
                async with session.post(url, headers=headers, json=data, ssl=False) as response:
                    if response.status == 200:
                        res_data = await response.json()
                        results = res_data.get("results", [])
                        
                        if results:
                            # Map term codes roughly
                            if term.endswith("4"): term_name = f"Summer {2000 + int(term[1:3])}"
                            elif term.endswith("2"): term_name = f"Spring {2000 + int(term[1:3])}"
                            elif term.endswith("8"): term_name = f"Fall {2000 + int(term[1:3])}"
                            else: term_name = f"Term {term}"
                            found_semesters.add(term_name)
                            
                            for r in results:
                                instr = r.get("instr", "")
                                if instr:
                                    # Split multiple instructors
                                    for p in instr.split(","):
                                        prof = p.strip()
                                        if prof: professors.add(prof)
                                
                                # Do a details fetch just once to get the full description/prereqs from the first match
                                if not found_description:
                                    det_url = "https://bulletins.nyu.edu/class-search/api/?page=fose&route=details"
                                    det_data = {
                                        "group": f"code:{r['code']}",
                                        "key": f"key:{r['key']}",
                                        "srcdb": term,
                                        "matched": f"crn:{r['crn']}"
                                    }
                                    async with session.post(det_url, headers=headers, json=det_data, ssl=False) as det_resp:
                                        if det_resp.status == 200:
                                            det_json = await det_resp.json()
                                            desc = det_json.get("description", "")
                                            restr = det_json.get("registration_restrictions", "")
                                            notes = det_json.get("clssnotes", "")
                                            if desc: found_description = desc
                                            if restr: found_description += f" \n Restrictions: {restr}"
                                            if notes: found_description += f" \n Notes: {notes}"
            except Exception as e:
                logger.error(f"Live scrape error for {course_code} term {term}: {e}")
                
    import re
    import html
    prereqs = "None"
    extra_notes = ""
    if found_description:
        match = re.search(r'(?:Prerequisite|Prereq)[s]?\s*(?:for[a-z\sA-Z-]*)?:?\s*(.*?)(?:\.\s+(?=[A-Z])|$)', found_description, re.IGNORECASE | re.DOTALL)
        if match:
            prereqs = " ".join(match.group(1).split())
            
        restr_match = re.search(r'Restrictions:\s*(.*?)(?: \n|$)', found_description)
        if restr_match: extra_notes += restr_match.group(1).strip() + ". "
        
        notes_match = re.search(r'Notes:\s*(.*)', found_description)
        if notes_match: extra_notes += notes_match.group(1).strip()

    if extra_notes and prereqs == "None":
        prereqs = extra_notes.strip()
    elif extra_notes:
        prereqs = prereqs + " | Notes: " + extra_notes.strip()
        
    return {
        "professors": list(professors) if professors else ["TBD - Consult Department"],
        "available_semesters": list(found_semesters)[:3] if found_semesters else ["Check NYU Albert"],
        "prerequisites": html.unescape(prereqs) if prereqs else "None",
        "live_status": "Department Listed"
    }

