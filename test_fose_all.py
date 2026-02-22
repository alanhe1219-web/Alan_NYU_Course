import requests
import json

url = "https://bulletins.nyu.edu/class-search/api/?page=fose&route=search"
headers = {'User-Agent': 'Mozilla/5.0'}

# Test a range of recent terms
# 1242 = Fall 2023, 1244 = Spring 2024, 1246 = Summer 2024, 1248 = Fall 2024, 1252 = Spring 2025, 1254 = Summer 2025
for term in ["1254", "1252", "1248", "1246", "1244", "1242"]:
    data = {"other": {"srcdb": term}, "criteria": [{"field": "keyword", "value": "HOU-UF 9101"}]}
    res = requests.post(url, headers=headers, json=data)
    d = res.json()
    if d.get("results"):
        print("Found in term", term, "!")
        print(d["results"][0])
        term_with_results = term
        
        # Now get the specific details for the exact professor!
        details_data = {
            "group": "code:" + d["results"][0]["code"],
            "key": "key:" + d["results"][0]["key"],
            "srcdb": term,
            "matched": "crn:" + d["results"][0]["crn"]
        }
        res_det = requests.post("https://bulletins.nyu.edu/class-search/api/?page=fose&route=details", headers=headers, json=details_data)
        import json
        det_json = res_det.json()
        print(json.dumps(det_json, indent=2))
        
        break
