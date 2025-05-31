from flask import Flask, request
from werkzeug.middleware.proxy_fix import ProxyFix
import os
from datetime import datetime

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1)

LOG_FILE = "ip_logs.txt"

@app.route('/')
def home():
    ip = request.remote_addr
    x_forwarded = request.headers.get('X-Forwarded-For', 'N/A')
    all_headers = dict(request.headers)

    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    log_entry = f"{timestamp} - remote_addr: {ip}, X-Forwarded-For: {x_forwarded}\n"

    # Print to console and log file
    print(log_entry.strip())

    try:
        with open(LOG_FILE, "a") as f:
            f.write(log_entry)
    except Exception as e:
        print(f"Error writing to file: {e}")

    # Show all headers for debugging
    headers_display = "\n".join(f"{k}: {v}" for k, v in all_headers.items())
    return f"""
    Your IP (from remote_addr): {ip}<br>
    Your IP (from X-Forwarded-For): {x_forwarded}<br><br>
    <b>Request Headers:</b><br><pre>{headers_display}</pre>
    """

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
