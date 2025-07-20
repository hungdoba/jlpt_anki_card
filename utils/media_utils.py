import requests
import time
import random

# Utility to download media files (sound/image)
def download_media(url, file_path):
    try:
        r = requests.get(url)
        with open(file_path, "wb") as f:
            f.write(r.content)
        return True
    except Exception as e:
        print(f"Error downloading media: {e}")
        return False

# Utility for random sleep
def random_sleep(seconds_list=[1,2]):
    seconds = random.choice(seconds_list)
    print(f"delay in {seconds}")
    time.sleep(seconds)
