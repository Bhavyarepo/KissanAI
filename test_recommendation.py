import requests
import json

def test_recommendation():
    # Login first to get token
    login_url = "http://localhost:8000/api/auth/login"
    login_data = {
        "email": "real@farmer.com",
        "password": "strongpassword"
    }
    login_response = requests.post(login_url, json=login_data)
    if login_response.status_code != 200:
        print("Login failed")
        return
    
    token = login_response.json()['access_token']
    headers = {"Authorization": f"Bearer {token}"}
    
    # Call recommendation
    # The route is GET /api/recommend/{farmer_id} in api_v2
    farmer_id = 2
    url = f"http://localhost:8000/api/recommend/{farmer_id}"
    
    try:
        response = requests.get(url, headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_recommendation()
