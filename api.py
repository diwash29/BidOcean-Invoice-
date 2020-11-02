import json
import requests
url = 'http://www.bidocean.com/api/production/request.php'

token = "Pr85SNYWOV3GQdKProdReqstwer53VjZpA6lHoegm"

requestData = {}
requestData["empid"] = 1296
requestData["year_month"] = '2020-08'
requestData["request"] = 'emp_production'
requestData["token"] = token

requestDataJson = json.dumps(requestData, ensure_ascii = 'False')
#print(requestDataJson)

result = requests.post(url, json = requestDataJson)
print(result.json())