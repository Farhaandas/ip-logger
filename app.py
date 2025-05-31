from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)
LOG_FILE = "ip_logs.txt"

@app.route('/')
def index():
    return """
    <html>
      <body>
        <h1>Logging your IP</h1>
        <script>
          fetch('https://api.ipify.org?format=json')
            .then(r => r.json())
            .then(data => {
              fetch('/log_ip', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ ip: data.ip })
              });
            });
        </script>
      </body>
    </html>
    """

@app.route('/log_ip', methods=['POST'])
def log_ip():
    print("Log IP route hit")  # Debug print
    data = request.get_json()
    ip = data.get('ip', 'UNKNOWN')
    timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
    log_entry = f"{timestamp} - IP: {ip}"
    print(log_entry)  # This prints in Render logs
    try:
        with open(LOG_FILE, "a") as f:
            f.write(log_entry + "\n")
    except Exception as e:
        print(f"Error writing log: {e}")
    return jsonify({"status": "logged", "ip": ip})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
