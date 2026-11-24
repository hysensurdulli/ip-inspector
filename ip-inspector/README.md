# IP Inspector

A transparent educational IP-geolocation demo built with Python + Flask.

## Run locally (Windows)

```powershell
py -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000

## Deploy to Render

1. Push this folder to a GitHub repository.
2. In Render choose **New + → Web Service** and connect that repository.
3. Use:
   - Runtime: Python
   - Build command: `pip install -r requirements.txt`
   - Start command: `gunicorn app:app`
4. Deploy. Render will provide the public URL.

The app reads the visitor connection IP to display it to that visitor. It does not save IPs. Approximate location is requested from ipapi.co; it is not a street address or GPS location.
