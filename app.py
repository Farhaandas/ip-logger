from flask import Flask, request
import os

app = Flask(__name__)

@app.route('/')
def home():
    ip = request.remote_addr
    print(f"New visitor IP: {ip}")  # Log IP to console (visible in Render logs)
    return f"Your IP address is: {ip}"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Required for Render
    app.run(host="0.0.0.0", port=port)
