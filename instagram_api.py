import requests
import json

def get_profile_pic(username):
    """Get profile picture URL using Instagram's GraphQL API"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "X-IG-App-ID": "936619743392459",
    }
    
    try:
        # First get the user ID
        user_url = f"https://www.instagram.com/api/v1/users/web_profile_info/?username={username}"
        response = requests.get(user_url, headers=headers)
        user_id = response.json()['data']['user']['id']
        
        # Then get the profile picture
        graphql_url = "https://www.instagram.com/graphql/query/"
        params = {
            "query_hash": "e74d51c10ecc0fe6250a295b9bb9db74",
            "variables": json.dumps({"user_id": user_id, "include_chaining": False})
        }
        response = requests.get(graphql_url, headers=headers, params=params)
        return response.json()['data']['user']['profile_pic_url_hd']
    except Exception as e:
        print(f"API Error: {e}")
        return None