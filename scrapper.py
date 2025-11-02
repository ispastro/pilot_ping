import requests

url = "https://corporate.ethiopianairlines.com/AboutEthiopian/careers/vacancies/2"

response = requests.get(url)

print(response.status_code)
print(response.text[:500])