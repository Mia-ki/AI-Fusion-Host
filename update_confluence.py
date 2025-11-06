import os
import requests
from datetime import datetime

# === Load secrets from environment ===
EMAIL = os.getenv("EMAIL")
API_TOKEN = os.getenv("API_TOKEN")
SPACE_KEY = "~629438789bc7150068cc65ba"  # Replace with your actual space key
PARENT_PAGE_ID = "1301512405"  # Replace with your actual parent page ID

# === Read HTML content from file ===
with open("latest.html", "r", encoding="utf-8") as file:
    html_content = file.read()

# === Prepare Confluence page data ===
page_title = f"AI Digest – Week of {datetime.now().strftime('%b %d, %Y')}"
page_data = {
    "type": "page",
    "title": page_title,
    "space": {"key": SPACE_KEY},
    "ancestors": [{"id": PARENT_PAGE_ID}],
    "body": {
        "storage": {
            "value": html_content,
            "representation": "storage"
        }
    }
}

# === Send request to Confluence API ===
url = "https://prudential-ps.atlassian.net/wiki/rest/api/content"
auth = (EMAIL, API_TOKEN)
headers = {
    "Content-Type": "application/json"
}

response = requests.post(url, json=page_data, auth=auth, headers=headers)

# === Handle response ===
if response.status_code == 200 or response.status_code == 201:
    print("✅ Confluence page created successfully.")
    print("🔗 Page URL:", response.json().get("_links", {}).get("webui"))
else:
    print("❌ Failed to create page.")
    print("Status Code:", response.status_code)
    print("Response:", response.text)
