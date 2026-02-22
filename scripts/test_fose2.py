import requests
import json

url = "https://bulletins.nyu.edu/class-search/api/?page=fose&route=search"
headers = {
    'User-Agent': 'Mozilla/5.0',
    'Content-Type': 'application/json'
}
data = {
    "other": {"srcdb": "1244"}, 
    "criteria": [{"field": "keyword", "value": "HOU-UF 9101"}]
}
res = requests.post(url, headers=headers, json=data)
print(res.status_code)
d = res.json()
print("results:", len(d.get("results", [])))
if d.get("results"):
    print(d["results"][0])

# To get details, usually there is a details route:
# ?page=fose&route=details
if d.get("results"):
    key = d["results"][0]["key"]
    details_data = {
        "group": "code:" + d["results"][0]["code"],
        "key": f"key:{key}",
        "srcdb": "1244",
        "matched": f"crn:{d['results'][0]['crn']}"
    }
    res2 = requests.post("https://bulletins.nyu.edu/class-search/api/?page=fose&route=details", headers=headers, json=details_data)
    print("Details:", res2.status_code)
    print(res2.text[:1000])

