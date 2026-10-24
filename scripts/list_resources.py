import requests

r = requests.get('https://data.gov.ro/api/3/action/package_show?id=firme-08-12-2025', timeout=15)
for res in r.json()['result']['resources']:
    print(res.get('name'), '|', res.get('size'), '|', res.get('url'))
