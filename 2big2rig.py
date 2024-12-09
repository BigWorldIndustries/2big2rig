from flask import Flask, request, jsonify
import threading
import time
import random
from bigworld_election_2024 import seed_rates, categories, categories_by_bias

app = Flask(__name__)

# Initialize stored_numbers using the initial_rates and categories
stored_numbers = {
    key: {'rate': rate, 'values': {category: 0.0 for category in categories}} 
    for key, rate in seed_rates.items()
}

def increment_numbers():
    while True:
        time.sleep(1)
        with lock:
            for key in stored_numbers:
                total_rate = stored_numbers[key]['rate']
                # Generate random sub-rates that sum to the total_rate

                # Part 1: Population Bias
                # this is a fixed bias applied so that smaller categories get a smaller random assortment of votes and bigger ones get a bigger random assortment of votes
                # this prevents votes from being equally distributed in all categories over time due to randomn distribution
                # categories array should be ordered by desired smallest to biggest categories
                parts1 = sorted([0] + [random.random() for _ in range(len(categories) - 1)] + [1])
                sub_rates1 = [parts1[i+1] - parts1[i] for i in range(len(categories))]
                scaled_sub_rates1 = sorted([sub_rate * total_rate for sub_rate in sub_rates1])
                # Increment each category by the sub-rate
                for i, category in enumerate(categories):
                    # divide by 2 because this accounts for half the rate's weighting
                    stored_numbers[key]['values'][category] += (scaled_sub_rates1[i]) / 2

                # # Part 2: Candidate Bias
                # # this is a bias applied so certain candidates perform better in certain categories they are deemed as favorites
                # # this prevents all categories from having the exact same ratio of votes between candidates
                # # categories_by_bias arrays should be ordered by most favored to least favored factions
                parts2 = sorted([0] + [random.random() for _ in range(len(categories) - 1)] + [1])
                sub_rates2 = [parts2[i+1] - parts2[i] for i in range(len(categories))]
                scaled_sub_rates2 = sorted([sub_rate * total_rate for sub_rate in sub_rates2])
                # Increment each category by the sub-rate
                for i, category in enumerate(categories_by_bias[key]):
                    # divide by 2 because this accounts for half the rate's weighting
                    stored_numbers[key]['values'][category] += (scaled_sub_rates2[i]) / 2

@app.route('/numbers', methods=['GET'])
def get_numbers():
    with lock:
        # Return rounded values for each category and the total for each number
        output = {}
        for key, data in stored_numbers.items():
            rounded_values = {category: int(round(value)) for category, value in data['values'].items()}
            total_value = sum(rounded_values.values())
            output[key] = {'categories': rounded_values, 'total': total_value}
        return jsonify(output)

@app.route('/numbers', methods=['POST'])
def set_number():
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'error': 'No data provided'}), 400

    with lock:
        for key, rate in data.items():
            if isinstance(rate, (int, float)):
                if key in stored_numbers:
                    # Update the rate but maintain current values
                    stored_numbers[key]['rate'] = rate
                else:
                    # Initialize the number with values set to 0.0 for each category
                    stored_numbers[key] = {'rate': rate, 'values': {category: 0.0 for category in categories}}
            else:
                return jsonify({'success': False, 'error': 'Invalid input type for rate'}), 400
        # Return the current status including each category's value and the total
        output = {}
        for key, data in stored_numbers.items():
            rounded_values = {category: int(round(value)) for category, value in data['values'].items()}
            total_value = sum(rounded_values.values())
            output[key] = {'categories': rounded_values, 'total': total_value}
        return jsonify({'success': True, 'new_numbers': output}), 200

if __name__ == '__main__':
    lock = threading.Lock()
    # Start the background thread
    thread = threading.Thread(target=increment_numbers)
    thread.daemon = True
    thread.start()
    app.run(debug=True)
