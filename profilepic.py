import requests
from tqdm import tqdm
from PIL import Image
import os
from instagram_api import get_profile_pic

def pp_download(username, url=None):
    """Working profile picture downloader"""
    if not url:
        url = get_profile_pic(username)
        if not url:
            print("Failed to get profile picture URL")
            return False

    try:
        print(f"\nDownloading profile picture from: {url}")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
            'Referer': f'https://www.instagram.com/{username}/',
        }
        
        response = requests.get(url, headers=headers, stream=True, timeout=10)
        response.raise_for_status()
        
        filename = f"{username}_profile.jpg"
        
        # Save with progress bar
        file_size = int(response.headers.get('content-length', 0))
        with tqdm(total=file_size, unit='B', unit_scale=True, desc=username, ascii=True) as pbar:
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
                        pbar.update(len(chunk))
        
        # Verify download
        if os.path.exists(filename):
            try:
                img = Image.open(filename)
                img.verify()
                print(f"Successfully saved as {filename}")
                return True
            except:
                os.remove(filename)
                print("Downloaded file is not a valid image")
                return False
        else:
            print("Download failed - no file created")
            return False
            
    except Exception as e:
        print(f"Download error: {str(e)}")
        return False