import json
import requests
url = 'http://1.7.151.12:8181/bidocean/api/production/request.php'

token = "developement_Pr85SNYWOadeIOlP53VjZpA6lHoegm"

requestData = {}
requestData["empid"] = 1296
requestData["year_month"] = '2020-08'
requestData["request"] = 'emp_production'
requestData["token"] = token

requestDataJson = json.dumps(requestData, ensure_ascii = 'False')
#print(requestDataJson)

result = requests.post(url, json = requestDataJson)
print(result.json())