import os
import sys
from flask import Flask, request, jsonify
import requests
import logging

app = Flask(__name__)

# Configure logging to ensure output goes to stdout
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', stream=sys.stdout)

PUSHOVER_URL = 'https://api.pushover.net/1/messages.json'

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()

    # Log the full POST message content
    logging.info(f"Received POST data: {data}")

    if not data:
        return jsonify({'error': 'Invalid JSON'}), 400
    
    value1 = data.get('value1')
    value2 = data.get('value2')
    value3 = data.get('value3')
    
    if not value1 or not value2 or not value3:
        return jsonify({'error': 'Missing required fields: value1, value2, value3'}), 400
    
    # Construct a user-friendly message
    message = f"It's your turn in {value1} as {value2}. Current turn: {value3}"
    
    token = os.getenv('PUSHOVER_TOKEN')
    user = os.getenv('PUSHOVER_USER')
    
    if not token or not user:
        return jsonify({'error': 'PushOver credentials not set'}), 500
    
    payload = {
        'token': token,
        'user': user,
        'message': message
    }
    
    response = requests.post(PUSHOVER_URL, data=payload)
    if response.status_code == 200:
        return jsonify({'status': 'Notification sent'}), 200
    else:
        return jsonify({'error': f'Failed to send notification: {response.text}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)