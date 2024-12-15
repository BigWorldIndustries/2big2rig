import time
from datetime import datetime
import random
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase
cred = credentials.Certificate('bigworld-e4cf4-firebase-adminsdk-g6v6y-8cf756ec6c.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

RESET_VOTES = False
INTERVAL = 60  # increment interval in seconds
ELECTION_ID = 'r9nizviywIETk3k0t5t2'  # Document ID on Firestore
RATE_SCALE = 100 # how much to scale the rate by

def fetch_latest_data():
    try:
        doc = db.collection('elections').document(ELECTION_ID).get()
        return doc.to_dict() if doc.exists else None
    except Exception as e:
        print(f"Failed to fetch data: {e}")
        return None

def store_new_numbers(numbers):
    try:
        db.collection('elections').document(ELECTION_ID).update({
            'simvotes': numbers,
            'sim_timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
    except Exception as e:
        print(f"Failed to store data: {e}")

def reset_numbers():
    data = fetch_latest_data()
    if not data:
        print("No data available to reset.")
        return
    
    for candidate in data['simvotes']:
        for region in data['simvotes'][candidate]:
            data['simvotes'][candidate][region] = 0.0
    
    try:
        db.collection('elections').document(ELECTION_ID).update({
            'simvotes': data['simvotes']
        })
        print("All simvotes have been reset to 0.")
    except Exception as e:
        print(f"Failed to reset simvotes: {e}")


def calculate_sub_rates(total_rate, regions):
    parts = sorted([0] + [random.random() for _ in range(len(regions) - 1)] + [1])
    sub_rates = [parts[i + 1] - parts[i] for i in range(len(regions))]
    return sorted([sub_rate * total_rate for sub_rate in sub_rates])

def increment_numbers():
    data = fetch_latest_data()
    if not data:
        print("No data available.")
        return

    regions = data['regions']  # ordered smallest to largest
    regions_by_bias = data['regions_by_bias'] # ordered for each candidate least favorability to most
    numbers = data['simvotes']

    for candidate, votes in data['votes'].items():
        # a random jitter is applied to prevent candidates on equal votes having exactly identical simvotes
        total_rate = (RATE_SCALE * votes) + (RATE_SCALE*random.random())
        sub_rates1 = calculate_sub_rates(total_rate, regions)
        sub_rates2 = calculate_sub_rates(total_rate, regions)

        # population bias
        for i, region in enumerate(regions):
            numbers[candidate][region] += sub_rates1[i] / 2
        # favorability bias
        for i, region in enumerate(regions_by_bias[candidate]):
            numbers[candidate][region] += sub_rates2[i] / 2

        total_sum = sum(numbers[candidate][region] for region in regions)
        numbers[candidate]['total'] = int(round(total_sum))

    store_new_numbers(numbers)

if __name__ == '__main__':
    if RESET_VOTES:
        reset_numbers()
    while True:
        increment_numbers()
        time.sleep(INTERVAL)