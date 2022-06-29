# import requests
# import json


# AUTH_URL = 'http://127.0.0.1:8070/web/session/authenticate/'

# headers = {'Content-type': 'application/json'}


# data = {
#     'params': {
#          'login': 'dev',
#          'password': 'dev',
#          'db': 'dev'
#     }
# }

# res = requests.post(
#     AUTH_URL, 
#     data=json.dumps(data), 
#     headers=headers
# )
# res=res.cookies
# print(res)

# requests.put(url,data,cookies=res)

