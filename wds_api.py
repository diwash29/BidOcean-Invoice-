import json
import requests

url   = "https://www.bidocean.com/api/production/request.php"
token = "Pr85SNYWOV3GQdKProdReqstwer53VjZpA6lHoegm"

requestData               = {}
requestData['empid']      = ""
requestData['date_start'] = '09/01/20'
requestData['date_end']   = '09/30/20'
requestData['request']    = 'wds_researcher_stats'
requestData['token']      = token
requestDataJson           = json.dumps(requestData, ensure_ascii = 'False')

result = requests.post(url, json = requestDataJson)
print(result.json())

