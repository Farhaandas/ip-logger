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
    data = request.get_json()

    # Get IP from headers if behind a proxy (e.g., on Render)
    forwarded_for = request.headers.get('X-Forwarded-For', '')
    ip = forwarded_for.split(',')[0].strip() if forwarded_for else request.remote_addr

    # Or override with external IP from the request body if sent
    ip = data.get('ip', ip)

    timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
    log_entry = f"{timestamp} - IP: {ip}"
    
    print(log_entry)

    try:
        with open("ip_logs.txt", "a") as f:
            f.write(log_entry + "\n")
    except Exception as e:
        print(f"Error writing log: {e}")
        
    return jsonify({"status": "logged", "ip": ip})
