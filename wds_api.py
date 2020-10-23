import json
import requests

url   = "https://www.bidocean.com/api/production/request.php"
token = "Pr85SNYWOV3GQdKProdReqstwer53VjZpA6lHoegm"

requestData               = {}
requestData['empid']      = 1140
requestData['date_start'] = '2020-11-01'
requestData['date_end']   = '2020-11-30'
requestData['request']    = 'wds_researcher_stats'
requestData['token']      = token
requestDataJson           = json.dumps(requestData, ensure_ascii = 'False')

result = requests.post(url, json = requestDataJson)
print(result.json())

