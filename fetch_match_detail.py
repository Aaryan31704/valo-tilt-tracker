import requests
import pprint
from plyer import notification
import time

region = "ap"
name = "Fragg17"
tag = "2319"

url = f"https://api.henrikdev.xyz/valorant/v3/matches/{region}/{name}/{tag}"

headers = {
    "Authorization": "HDEV-03589aed-46c1-4380-829f-7230df7fc770"
}

already_notified = False

def get_match_data():
    print(f"Pinging servers for {name}#{tag}...")
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            print(f"✅ Successfully fetched match data")
            return response.json()
        else:
            print(f"❌ Failed to fetch. Status Code: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def check_tilt(match):
    global already_notified
    results = []

    for i in range(len(match['data'])):
        single_match = match['data'][i]

        # Skip if not competitive
        if single_match['metadata']['mode'].lower() != 'competitive':
            print(f"Match {i+1} skipped (not competitive)")
            continue

        all_players = single_match['players']['all_players']
        our_player = next(
            (p for p in all_players if p['name'].lower() == name.lower()),
            None
        )

        if our_player is None:
            print(f"Match {i+1}: Player not found, skipping")
            continue

        player_team = our_player['team'].lower()
        won = single_match['teams'][player_team]['has_won']

        result = 'W' if won else 'L'
        results.append(result)
        print(f"Match {i+1} | Team: {player_team} | Result: {result}")

    print(f"\nRecent competitive results: {results}")

    # Check for 3 losses in a row
    if len(results) >= 3 and results[:3] == ['L', 'L', 'L']:
        if not already_notified:
            print("🔴 TILT DETECTED: 3 losses in a row!")
            notification.notify(
                title="🔴 VALORANT TILT ALERT",
                message=f"{name}#{tag} has lost 3 competitive games in a row. Take a break!",
                timeout=10
            )
            already_notified = True
    else:
        print("✅ No tilt detected.")
        already_notified = False  # reset if no longer on loss streak

    return results

def check_tilt_test(results):
    global already_notified

    print(f"Results: {results}")

    if len(results) >= 3 and results[:3] == ['L', 'L', 'L']:
        if not already_notified:
            print("🔴 TILT DETECTED: 3 losses in a row!")
            notification.notify(
                title="🔴 VALORANT TILT ALERT",
                message=f"{name}#{tag} has lost 3 competitive games in a row. Take a break!",
                timeout=10
            )
            already_notified = True
    else:
        print("✅ No tilt detected.")
        already_notified = False

check_tilt_test(['L', 'L', 'L'])


""" while True:
    match_data = get_match_data()
    if match_data:
        check_tilt(match_data)
    print("\nChecking again in 5 minutes...\n")
    time.sleep(300) """