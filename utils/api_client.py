
import requests
BASE_URL = "http://127.0.0.1:8000"

def generate_text(text: str, style: str = "formal", strength: float = 0.5):
    payload = {"text": text, "style": style}
    try:
        res = requests.post(f"{BASE_URL}/generate?strength={strength}", json=payload, timeout=20)
        res.raise_for_status()
        return res.json()
    except Exception as e:
        return {"error": str(e)}

def analyze_text(text: str):
    payload = {"text": text, "style": "formal"}
    try:
        res = requests.post(f"{BASE_URL}/analyze", json=payload, timeout=20)
        res.raise_for_status()
        return res.json()
    except Exception as e:
        return {"error": str(e)}

def upload_file(file_path: str):
    try:
        with open(file_path, "rb") as f:
            files = {"file": (file_path, f)}
            res = requests.post(f"{BASE_URL}/upload", files=files, timeout=60)
            res.raise_for_status()
            return res.json()
    except Exception as e:
        return {"error": str(e)}

def list_styles():
    try:
        res = requests.get(f"{BASE_URL}/styles", timeout=10)
        res.raise_for_status()
        return res.json()
    except Exception as e:
        return {"error": str(e)}
