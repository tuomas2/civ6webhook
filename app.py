import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

PUSHOVER_URL = 'https://api.pushover.net/1/messages.json'

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()

    # Log the full POST message content
    print(f"Received POST data: {data}")

    if not data:
        return jsonify({'error': 'Invalid JSON'}), 400
    
    message = data.get('message', 'No message provided')
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