import requests
import json
import os
import subprocess

# API config.
URL = os.getenv("JSON_URL")
FILE_PATH = "data.json"

# Telegram config.
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_message(message):
    """Send a message to the Telegram channel."""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        print(f"✅ Message sent to Telegram: {message}")
    except Exception as e:
        print(f"❌ Error sending message to Telegram: {e}")

def get_json_from_url(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def load_local_json(file_path):
    if not os.path.exists(file_path):
        return None
    with open(file_path, 'r') as file:
        return json.load(file)

def save_json(file_path, data):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)

def commit_changes():
    subprocess.run(["git", "config", "--global", "user.name", "GitHub Actions"])
    subprocess.run(["git", "config", "--global", "user.email", "actions@github.com"])
    subprocess.run(["git", "add", FILE_PATH])
    subprocess.run(["git", "commit", "-m", "🔄 JSON actualizado automáticamente"])
    subprocess.run(["git", "push"])
    
def main():
    new_data = get_json_from_url(URL)
    old_data = load_local_json(FILE_PATH)

    if old_data is None:
        print("📥 Guardando JSON por primera vez...")
        save_json(FILE_PATH, new_data)
        commit_changes()
        send_message("📥 JSON guardado por primera vez.")
    elif old_data != new_data:
        print("⚠️ El JSON ha cambiado, actualizando...")
        save_json(FILE_PATH, new_data)
        commit_changes()
        send_message("⚠️ ¡Atención! El JSON ha cambiado y ha sido actualizado.")
    else:
        print("✅ JSON no ha cambiado, no se realizaron cambios.")

if __name__ == "__main__":
    main()
    
