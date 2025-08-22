# this program will use TTR's localapi to get the toon's district and save the district name to a file in the same directory.
import os
import time
import sys
import requests
import random
if sys.platform == 'win32':
    game_dir = "C:/Program Files (x86)/Toontown Rewritten"
elif sys.platform == 'darwin':
    # game directory is in the Application Support directory
    game_dir = os.path.join(os.environ['HOME'], "Library/Application Support/Toontown Rewritten")
elif sys.platform.startswith('liunx'):
    # lets just let linux users put the executable in the game directory
    game_dir = os.get_cwd()

district_file_path = os.path.join(game_dir, "district.txt")
api_url = "http://localhost:1547/location.json" 

def generate_random_token():
    """Generates a random session token."""
    return ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=32))
authorization_token = generate_random_token()
headers = {
    "Host": "localhost:1547",
    "User-Agent": "DistrictTracker/1.1",
    "Authorization": authorization_token
}


def main():
    connected = False
    # connect to the localapi
    while not connected:
        print("Connecting to the localapi...")
        # try to connect to the localapi
        try:
            response = requests.get(api_url, headers=headers)
            response.raise_for_status()
            connected = True
            break
        except requests.RequestException as e:
            print(f"Error connecting to the localapi: {e}")
            print("Could not connect to the localapi. Please make sure TTR is running and Comapnion App Support is enabled")
            connected = False
            # if the connection fails, wait a bit and try again
            time.sleep(5)
    print("Connected to the localapi.")
    while connected:
        # grab the response again because the district can change
        print("Fetching current district...")
        try:
            response = requests.get(api_url, headers=headers)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Error fetching district: {e}")
            connected = False
            
        district = response.json().get("district", "Unknown")
        print(f"Current district: {district}")
        # save the district to a file
        with open(district_file_path, "w") as district_file:
            district_file.write(district)
        print(f"District saved to {district_file_path}")
        # wait for a bit before checking again
        time.sleep(5)
    # if we reach here, it means we lost connection to the localapi and we should loop back to the beginning
    print("Lost connection to the localapi. Reconnecting...")
    time.sleep(1)
    main()

if __name__ == "__main__":
    main()
