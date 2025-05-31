from flask import Flask, request, jsonify
from datetime import datetime
import os
import sys
import requests

app = Flask(__name__)

# Optional: Use your Google Apps Script webhook URL here
GOOGLE_SHEET_WEBHOOK = "https://script.google.com/macros/s/YOUR_SCRIPT_ID/exec"

@app.route('/')
def index():
    return """
    <html>
      <head><title>IP Logger</title></head>
      <body>
        <h1>Logging your IP...</h1>
        <p>This page logs your IP address to the server and optionally to Google Sheets.</p>

        <script>
          window.onload = function () {
            fetch('https://api.ipify.org?format=json')
              .then(response => response.json())
              .then(data => {
                console.log("Your Public IP is:", data.ip);
                fetch('/log_ip', {
                  method: 'POST',
                  headers: {'Content-Type': 'application/json'},
                  body: JSON.stringify({ ip: data.ip })
                })
                .then(response => response.json())
                .then(result => console.log("Server Response:", result))
                .catch(error => console.error("POST failed:", error));
              })
              .catch(error => console.error("Fetch IP failed:", error));
          }
        </script>
      </body>
    </html>
    """

@app.route('/log_ip', methods=['POST'])
def log_ip():
    data = request.get_json()

    # Use IP from JS fetch if available, else use proxy or remote IP
    forwarded_for = request.headers.get('X-Forwarded-For', '')
    proxy_ip = forwarded_for.split(',')[0].strip() if forwarded_for else request.remote_addr
    ip = data.get('ip', proxy_ip)

    # Create timestamp and log entry
    timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
    log_entry = f"{timestamp} - IP: {ip}"

    # Print to Render logs
    print(log_entry)
    sys.stdout.flush()

    # Optionally: send to Google Sheet
    try:
        if GOOGLE_SHEET_WEBHOOK and "YOUR_SCRIPT_ID" not in GOOGLE_SHEET_WEBHOOK:
            response = requests.post(GOOGLE_SHEET_WEBHOOK, json={"ip": ip})
            print(f"Google Sheet log response: {response.text}")
    except Exception as e:
        print(f"Failed to send to Google Sheet: {e}")

    return jsonify({"status": "logged", "ip": ip})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # For Render or local
    app.run(host="0.0.0.0", port=port, debug=True)
