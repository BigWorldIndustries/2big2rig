from flask import Flask, request, jsonify
import threading
import time
import random

app = Flask(__name__)

# Use a dictionary to store named numbers, each containing three category values
stored_numbers = {}

def increment_numbers():
    while True:
        time.sleep(1)
        with lock:
            for key in stored_numbers:
                total_rate = stored_numbers[key]['rate']
                # Generate random sub-rates that sum to the total_rate
                parts = sorted([0, random.random(), random.random(), 1])
                sub_rates = [parts[i+1] - parts[i] for i in range(3)]
                
                # sorting is unnecessary, but we sort so that the smaller share of votes always go to the same categories & the bigger share of votes always go the same categories
                # this prevents the categories from having an almost equal amount of the total through random distribution over time
                # this means the categories array should be ordered by desired smallest to biggest categories
                scaled_sub_rates = sorted([sub_rate * total_rate for sub_rate in sub_rates]) 
                
                # Increment each category by its sub-rate
                for i, category in enumerate(['alpha', 'beta', 'theta']):
                    stored_numbers[key]['values'][category] += scaled_sub_rates[i]

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
                    stored_numbers[key] = {'rate': rate, 'values': {'alpha': 0.0, 'beta': 0.0, 'theta': 0.0}}
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
