import requests


url = "http://127.0.0.1:3001/api/charts"

try:
    response = requests.get(url)
    response.raise_for_status()  
    data = response.json()
    print("Response Data:")
    print(data)
except requests.exceptions.RequestException as e:
    print(f"Error: {e}")