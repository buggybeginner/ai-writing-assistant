import json
import os

PROFILE_DIR = "data/profiles"
os.makedirs(PROFILE_DIR, exist_ok=True)

def save_style_profile(username: str, profile: dict):
    path = os.path.join(PROFILE_DIR, f"{username}.json")
    with open(path, "w") as f:
        json.dump(profile, f, indent=4)

def load_style_profile(username: str):
    path = os.path.join(PROFILE_DIR, f"{username}.json")
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return None
