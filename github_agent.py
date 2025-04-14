import base64
import requests
import os

# 📌 Настройки
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO = "Bubi-mubi/Telegram-bot"
FILE_PATH = "test.py"
BRANCH = "main"
COMMIT_MESSAGE = "Auto update via GPT Agent 🤖"

# 🧠 Промяната, която ще правим
FIND_TEXT = "Запази"
REPLACE_TEXT = "Изпрати"

headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

def get_file_info():
    url = f"https://api.github.com/repos/{REPO}/contents/{FILE_PATH}?ref={BRANCH}"
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    return res.json()

def update_file(content_b64, sha):
    decoded = base64.b64decode(content_b64).decode("utf-8")
    updated = decoded.replace(FIND_TEXT, REPLACE_TEXT)
    encoded = base64.b64encode(updated.encode("utf-8")).decode("utf-8")

    url = f"https://api.github.com/repos/{REPO}/contents/{FILE_PATH}"
    data = {
        "message": COMMIT_MESSAGE,
        "content": encoded,
        "branch": BRANCH,
        "sha": sha
    }
    res = requests.put(url, headers=headers, json=data)
    res.raise_for_status()
    print("✅ Файлът е обновен успешно!")

def run():
    info = get_file_info()
    update_file(info["content"], info["sha"])

if __name__ == "__main__":
    run()
