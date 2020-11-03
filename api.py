import json
import requests
url = 'https://www.bidocean.com/api/production/request.php'

#token = "developement_Pr85SNYWOadeIOlP53VjZpA6lHoegm"
token = "Pr85SNYWOV3GQdKProdReqstwer53VjZpA6lHoegm"
requestData = {}
requestData["empid"] = 1141
requestData["year_month"] = '2020-09'
requestData["request"] = 'emp_production'
requestData["token"] = token

requestDataJson = json.dumps(requestData, ensure_ascii = 'False')
#print(requestDataJson)

result = requests.post(url, json = requestDataJson)
print(result.text)

