import requests
import time
import json
from datetime import datetime, timedelta

# Function to read authorization data from data.txt
def read_authorizations(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]

# Function to process an account
def process_account(auth_token):
    url = "https://clicker-backend.spin.fi/api/clicks/apply?clicks=1"
    headers = {
        ":authority": "clicker-backend.spin.fi",
        ":method": "POST",
        ":path": "/api/clicks/apply?clicks=1",
        ":scheme": "https",
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-GB,en;q=0.9,en-US;q=0.8",
        "Authorization": f"Bearer {auth_token}",
        "Cache-Control": "no-cache",
        "Content-Length": "0",
        "Origin": "https://clicker.spin.fi",
        "Pragma": "no-cache",
        "Priority": "u=1, i",
        "Referer": "https://clicker.spin.fi/",
        "Sec-Ch-Ua": "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"126\", \"Microsoft Edge\";v=\"126\", \"Microsoft Edge WebView2\";v=\"126\"",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "\"Windows\"",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0"
    }

    try:
        response = requests.post(url, headers=headers)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error processing account: {e}")
        return False

# Function to display countdown timer
def countdown_timer(duration):
    end_time = datetime.now() + timedelta(seconds=duration)
    while datetime.now() < end_time:
        remaining_time = end_time - datetime.now()
        print(f"\rCountdown: {remaining_time}", end="")
        time.sleep(1)
    print("\nCountdown finished. Restarting the process...")

def main():
    # Read authorization tokens
    auth_tokens = read_authorizations('data.txt')
    total_accounts = len(auth_tokens)

    while True:
        print(f"Total accounts to process: {total_accounts}")
        
        for index, auth_token in enumerate(auth_tokens):
            print(f"Processing account {index + 1} of {total_accounts}")
            while process_account(auth_token):
                time.sleep(1)  # Adjust if needed for request rate limiting
            print("Switching to next account...")
            time.sleep(5)  # 5-second delay between account switches
        
        print("All accounts processed. Starting 1-hour countdown.")
        countdown_timer(3600)  # 1-hour countdown in seconds

if __name__ == "__main__":
    main()
