from flask import Flask, request, jsonify
import threading
import time

app = Flask(__name__)

# Use a dictionary to store named numbers with their current values and rate factors
stored_numbers = {}

def increment_numbers():
    while True:
        time.sleep(1)
        with lock:
            for key in stored_numbers:
                # Increment by the rate factor, keeping float precision
                stored_numbers[key]['value'] += stored_numbers[key]['rate']

@app.route('/numbers', methods=['GET'])
def get_numbers():
    with lock:
        # Return values rounded to the nearest integer for display
        rounded_values = {key: int(round(value['value'])) for key, value in stored_numbers.items()}
        return jsonify(rounded_values)

@app.route('/numbers', methods=['POST'])
def set_number():
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'error': 'No data provided'}), 400

    with lock:
        for key, rate in data.items():
            if isinstance(rate, (int, float)):  # Now accepting floats as well
                if key in stored_numbers:
                    # Update the rate factor but maintain the current value
                    stored_numbers[key]['rate'] = rate
                else:
                    # Initialize the number since it does not exist
                    stored_numbers[key] = {'rate': rate, 'value': 0}
            else:
                return jsonify({'success': False, 'error': 'Invalid input type for rate'}), 400
        # Return current values rounded to nearest integer for user clarity
        rounded_values = {key: int(round(value['value'])) for key, value in stored_numbers.items()}
        return jsonify({'success': True, 'new_numbers': rounded_values}), 200

if __name__ == '__main__':
    lock = threading.Lock()
    # Start the background thread
    thread = threading.Thread(target=increment_numbers)
    thread.daemon = True
    thread.start()
    app.run(debug=True)
