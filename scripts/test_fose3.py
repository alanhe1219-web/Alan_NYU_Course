import requests
import json

url = "https://bulletins.nyu.edu/class-search/api/?page=fose&route=search"
headers = {'User-Agent': 'Mozilla/5.0'}

for term in ["1254", "1252", "1248", "1246", "1244", "1242"]:
    data = {"other": {"srcdb": term}, "criteria": [{"field": "keyword", "value": "CSCI-UA 473"}]}
    res = requests.post(url, headers=headers, json=data)
    d = res.json()
    if d.get("results"):
        print("Found in term", term)
        print("Instructor:", d["results"][0].get("instr"))
        print("Meeting:", d["results"][0].get("meets"))
        
        details_data = {
            "group": "code:" + d["results"][0]["code"],
            "key": "key:" + d["results"][0]["key"],
            "srcdb": term,
            "matched": "crn:" + d["results"][0]["crn"]
        }
        res_det = requests.post("https://bulletins.nyu.edu/class-search/api/?page=fose&route=details", headers=headers, json=details_data)
        det_json = res_det.json()
        print("Restr:", det_json.get("registration_restrictions"))
        print("Prequisites if any:", det_json.get("description", ""))
        break
