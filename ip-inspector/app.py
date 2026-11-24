from flask import Flask, render_template, request, make_response
from werkzeug.middleware.proxy_fix import ProxyFix
import ipaddress
import requests

app = Flask(__name__)

# Render runs the app behind one trusted proxy.
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1)

@app.route("/")
def home():
    ip = request.remote_addr or "Unknown"
    location = {}

    try:
        parsed_ip = ipaddress.ip_address(ip)
        if parsed_ip.is_global:
            result = requests.get(
                f"https://ipapi.co/{ip}/json/",
                timeout=5
            )
            result.raise_for_status()
            data = result.json()

            if not data.get("error"):
                location = {
                    "country": data.get("country_name") or "Unavailable",
                    "city": data.get("city") or "Unavailable",
                    "region": data.get("region") or "Unavailable",
                    "isp": data.get("org") or "Unavailable",
                }
    except (ValueError, requests.RequestException):
        pass

    response = make_response(
        render_template("index.html", ip=ip, location=location)
    )
    response.headers["Cache-Control"] = "no-store"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "no-referrer"
    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
