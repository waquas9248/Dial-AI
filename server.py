from flask import Flask, request, jsonify
import json
import os
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)

# Path to the JSON file
json_file_path = "data.json"

# Initialize data file if it doesn't exist
if not os.path.exists(json_file_path):
    initial_data = {
        "wildlife": [],
        "police": [],
        "water": [],
        "fire": []
    }
    with open(json_file_path, 'w') as f:
        json.dump(initial_data, f)
    logging.info(f"Initialized data file at {json_file_path} with empty categories.")

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        # Log HTTP request details
        logging.info(f"Received {request.method} request at {request.url}")
        logging.debug(f"Request headers: {request.headers}")
        logging.debug(f"Request data: {request.data}")

        data = request.json
        logging.debug(f"Parsed JSON data: {data}")

        # Validate incoming data structure
        if not isinstance(data, dict) or not all(key in data for key in ["wildlife", "police", "water", "fire"]):
            logging.error("Invalid data structure received.")
            response = jsonify({"status": "error", "message": "Invalid data structure."})
            logging.info(f"Response: {response.get_json()}")
            return response, 400

        # Read existing data
        with open(json_file_path, 'r') as f:
            existing_data = json.load(f)

        # Append new data to the appropriate categories
        for category, cases in data.items():
            if category in existing_data:
                existing_data[category].extend(cases)
                logging.debug(f"Updated category '{category}' with new cases: {cases}")

        # Write updated data back to the file
        with open(json_file_path, 'w') as f:
            json.dump(existing_data, f)
        logging.info("Data updated successfully.")

        response = jsonify({"status": "success", "message": "Data received and updated."})
        logging.info(f"Response: {response.get_json()}")
        return response, 200

    except Exception as e:
        logging.exception("An error occurred while processing the webhook.")
        response = jsonify({"status": "error", "message": "An error occurred while processing the request."})
        logging.info(f"Response: {response.get_json()}")
        return response, 500

if __name__ == '__main__':
    app.run(port=8080)
