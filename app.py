from flask import Flask, request, jsonify
from datetime import datetime
import os

app = Flask(__name__)

LOG_FILE = "ip_logs.txt"

@app.route('/')
def index():
    return """
    <html>
      <head><title>IP Logger</title></head>
      <body>
        <h1>Logging your IP...</h1>
        <script>
          fetch('https://api.ipify.org?format=json')
            .then(response => response.json())
            .then(data => {
              fetch('/log_ip', {
                method: 'POST',
                headers: {
                  'Content-Type': 'application/json'
                },
                body: JSON.stringify({ ip: data.ip })
              });
            });
        </script>
        <p>Your IP is being logged.</p>
      </body>
    </html>
    """

@app.route('/log_ip', methods=['POST'])
def log_ip():
    data = request.get_json()
    ip = data.get('ip', 'UNKNOWN')
    timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
    log_entry = f"{timestamp} - IP: {ip}\n"

    print(log_entry.strip())  # This goes to Render logs

    try:
        with open(LOG_FILE, "a") as f:
            f.write(log_entry)
    except Exception as e:
        print(f"Failed to write log: {e}")

    return jsonify({"status": "logged", "ip": ip})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
