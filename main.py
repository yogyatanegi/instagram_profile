import requests
import json
import re
import sys
import time
import random
from pprint import pprint
from profilepic import pp_download

def banner():
    print('\n\t Instagram Profile Scraper (Enhanced)')
    print('\t' + '='*50 + '\n')

def get_instagram_data(username):
    """Multi-method approach to bypass Instagram's protections"""
    
    # Initial delay before first attempt
    time.sleep(random.uniform(2, 5))
    
    # Method 1: Try official API first
    api_result = try_api_method(username)
    if api_result['success']:
        return api_result
    
    # Delay before fallback method
    time.sleep(random.uniform(2, 5))
    
    # Method 2: Fallback to HTML scraping
    html_result = try_html_method(username)
    if html_result['success']:
        return html_result
    
    # Delay before final fallback
    time.sleep(random.uniform(1, 3))
    
    # Method 3: Final fallback to mobile API
    mobile_result = try_mobile_method(username)
    if mobile_result['success']:
        return mobile_result
    
    return {'success': False, 'error': 'All methods failed'}

def try_api_method(username):
    """Official API method with proper headers"""
    # In try_api_method() function, update the headers:
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "X-IG-App-ID": "936619743392459",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": f"https://www.instagram.com/{username}/",
    }
    try:
        url = f"https://www.instagram.com/api/v1/users/web_profile_info/?username={username}"
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            user = data['data']['user']
            return format_profile_data(user)
    except Exception as e:
        print(f"API method failed: {str(e)}")
    return {'success': False}

def try_html_method(username):
    """HTML scraping fallback"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
    }
    
    try:
        url = f"https://www.instagram.com/{username}/"
        response = requests.get(url, headers=headers, timeout=10)
        shared_data = re.search(r'window\._sharedData\s*=\s*({.+?});', response.text)
        if shared_data:
            data = json.loads(shared_data.group(1))
            user = data['entry_data']['ProfilePage'][0]['graphql']['user']
            return format_profile_data(user)
    except Exception as e:
        print(f"HTML method failed: {str(e)}")
    return {'success': False}

def try_mobile_method(username):
    """Mobile API fallback"""
    headers = {
        "User-Agent": "Instagram 265.0.0.19.301 Android (24/7.0; 640dpi; 1440x2560; samsung; SM-G930F; herolte; samsungexynos8890)",
        "X-IG-App-ID": "567067343352427"
    }
    
    try:
        url = f"https://i.instagram.com/api/v1/users/{username}/info/"
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            user = response.json()['user']
            return format_profile_data(user)
    except Exception as e:
        print(f"Mobile method failed: {str(e)}")
    return {'success': False}

def format_profile_data(user):
    """Standardize profile data format"""
    return {
        'success': True,
        'profile': {
            'name': user.get('full_name'),
            'username': user.get('username'),
            'followers': user.get('edge_followed_by', {}).get('count') or user.get('follower_count'),
            'following': user.get('edge_follow', {}).get('count') or user.get('following_count'),
            'posts': user.get('edge_owner_to_timeline_media', {}).get('count') or user.get('media_count'),
            'bio': user.get('biography'),
            'profile_pic_url': user.get('profile_pic_url_hd') or user.get('hd_profile_pic_url_info', {}).get('url'),
            'is_private': user.get('is_private', False)
        }
    }

if __name__ == "__main__":
    banner()
    
    if len(sys.argv) == 2:
        username = sys.argv[1].replace('@', '')
        print(f"Fetching data for: @{username}")
        
        data = get_instagram_data(username)
        pprint(data)
        
        if data.get('success'):
            if data['profile']['is_private']:
                print("\nAccount is private - cannot download profile picture")
            else:
                pp_download(username, data['profile']['profile_pic_url'])
    else:
        print("Usage: python main.py username")