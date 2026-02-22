import requests
import pprint 

region = "ap"
name = "S1MPLISTIC"
tag = "D7RK"

url = f"https://api.henrikdev.xyz/valorant/v3/matches/{region}/{name}/{tag}"

headers = {
    "Authorization": "HDEV-03589aed-46c1-4380-829f-7230df7fc770"
}

print(f"Pinging servers for {name}#{tag}...")

try:
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        match_data = response.json()
        latest_match = match_data['data'][0]
        metadata = latest_match['metadata']
        
        print("Metadata keys:", metadata.keys())
        print("Full metadata:")
        pprint.pprint(metadata)

    else:
        print(f"❌ Failed to fetch. Status Code: {response.status_code}")

except Exception as e:
    print(f"Error: {e}")