import requests

url = "https://bulletins.nyu.edu/class-search/api/?page=fose&route=search"
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Content-Type': 'application/json'
}
data = {
    "other": {"srcdb": "1244"}, # 1244 is typically Spring 2024, maybe need to find the right term code
    "criteria": [{"field": "keyword", "value": "Machine Learning"}]
}

try:
    res = requests.post(url, headers=headers, json=data)
    print(res.status_code)
    print(res.text[:1000])
except Exception as e:
    print(e)
