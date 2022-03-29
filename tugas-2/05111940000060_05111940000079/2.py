# import requests module
import requests

# Making a get request
response = requests.get('https://www.its.ac.id/')

# print response
# print(response)

# print headers of response
print('Content-Encoding:', response.headers['Content-Encoding'])
