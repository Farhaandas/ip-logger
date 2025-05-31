from flask import Flask, request, jsonify
from datetime import datetime
import os
import requests

app = Flask(__name__)

# Replace with your actual Google Apps Script Webhook URL
GOOGLE_SHEET_WEBHOOK = "https://script.google.com/macros/s/AKfycbzaqPeEtTSotGpNbKvqpe1TphhykT9c6sDTI0zsJ6K4KrSvVFJTyN3cxvzyIAy_TfHg/exec"

@app.route('/')
def index():
    return """
    <html>
      <head><title>IP Logger</title></head>
      <body>
        <h1>Logging your IP...</h1>
        <p>This page will log your public IP to a Google Sheet.</p>
        <script>
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
        </script>
      </body>
    </html>
    """

@app.route('/log_ip', methods=['POST'])
def log_ip():
    data = request.get_json()

    # Get IP from proxy header (Render) or fallback
    forwarded_for = request.headers.get('X-Forwarded-For', '')
    proxy_ip = forwarded_for.split(',')[0].strip() if forwarded_for else request.remote_addr

    # Use IP from client if available, else proxy IP
    ip = data.get('ip', proxy_ip)

    timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
    log_entry = f"{timestamp} - IP: {ip}"
    
    print(log_entry)  # Log to console (also appears in Render logs)

    # Send to Google Sheet via webhook
    try:
        response = requests.post(GOOGLE_SHEET_WEBHOOK, json={"ip": ip})
        print(f"Sheet log response: {response.text}")
    except Exception as e:
        print(f"Failed to log to Google Sheet: {e}")

    return jsonify({"status": "logged", "ip": ip})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Use PORT env var on Render
    app.run(host="0.0.0.0", port=port, debug=True)
