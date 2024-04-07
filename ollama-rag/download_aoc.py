import os
import requests
import time
from random import randint

# Create a directory if it doesn't exist
os.makedirs("aoc_data", exist_ok=True)

# Base URL
base_url = "https://adventofcode.com"

# Initialize a session we need to not get blocked
session = requests.Session()
session.headers.update({
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'en-US,en;q=0.9',
    'Cache-Control': 'no-cache',
    'Pragma': 'no-cache',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
})

# Update your cookie here if you want to download the input data
# session.cookies.set('session', '<PUT HERE YOUR SPECIFICS>')

def download_all_years():
    for year in range(2015, 2024):
        download_year(year)

def download_year(year, sleep_time=2):
    for day in range(1, 26):
        try:
            url = f"{base_url}/{year}/day/{day}"
            response = session.get(url)
            print(f"Downloading {url}...")
            
            if response.status_code == 200:
                with open(f"aoc_data/{year}_day{day}.html", "w") as f:
                    f.write(response.text)
                time.sleep(sleep_time + randint(1, 3))  # Randomize wait time
            else:
                print(f"Failed to download {url}: {response.status_code}")
        except Exception as e:
            print(f"Error downloading {url}: {e}")

if __name__ == "__main__":
    download_all_years()
