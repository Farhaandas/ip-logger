from flask import Flask, request
from werkzeug.middleware.proxy_fix import ProxyFix
import os
from datetime import datetime

app = Flask(__name__)

# Trust the proxy to get real IP
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1)

LOG_FILE = "ip_logs.txt"  # File to store IP logs

@app.route('/')
def home():
    ip = request.remote_addr
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    log_entry = f"{timestamp} - IP: {ip}\n"

    # Print to console (Render Logs)
    print(log_entry.strip())

    # Save to file (local filesystem - ephemeral on Render)
    try:
        with open(LOG_FILE, "a") as f:
            f.write(log_entry)
    except Exception as e:
        print(f"Error writing to log file: {e}")

    return f"Your IP address is: {ip}"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Required for Render
    app.run(host="0.0.0.0", port=port)
