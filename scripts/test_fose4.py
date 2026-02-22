import requests

headers = {'User-Agent': 'Mozilla/5.0'}
term = "1248" # Fall 2024
data = {"other": {"srcdb": term}, "criteria": [{"field": "keyword", "value": "CSCI-UA 102"}]}
url = "https://bulletins.nyu.edu/class-search/api/?page=fose&route=search"

res = requests.post(url, headers=headers, json=data, verify=False)
d = res.json()
if d.get("results"):
    print("Found!")
    r = d["results"][0]
    det_data = {"group": f"code:{r['code']}", "key": f"key:{r['key']}", "srcdb": term, "matched": f"crn:{r['crn']}"}
    res_det = requests.post("https://bulletins.nyu.edu/class-search/api/?page=fose&route=details", headers=headers, json=det_data, verify=False)
    import json
    print(json.dumps(res_det.json(), indent=2))
