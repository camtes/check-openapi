import requests
import json
import os
import subprocess

URL = "https://data-api.hawkings.education/api/swagger/swagger.json"
FILE_PATH = "data.json"

def get_json_from_url(url):
    response = request.get(url)
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
    elif old_data != new_data:
        print("⚠️ El JSON ha cambiado, actualizando...")
        save_json(FILE_PATH, new_data)
        commit_changes()
    else:
        print("✅ JSON no ha cambiado, no se realizaron cambios.")

if __name__ == "__main__":
    main()
    
