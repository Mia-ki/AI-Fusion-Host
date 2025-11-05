import requests
from requests.auth import HTTPBasicAuth
import os
from datetime import datetime

# Config
GITHUB_HTML_URL = "https://mia-ki.github.io/AI-Fusion-Host/latest.html"
CONFLUENCE_BASE_URL = "https://~629438789bc7150068cc65ba.atlassian.net/wiki"
EMAIL = os.environ["CONFLUENCE_EMAIL"]
API_TOKEN = os.environ["CONFLUENCE_API_TOKEN"]

# Step 1: Get today's title
today_title = "AI Fusion – " + datetime.now().strftime("%B %-d, %Y")

# Step 2: Search for the page
search_url = f"{CONFLUENCE_BASE_URL}/rest/api/content?title={today_title}&spaceKey=<your-space-key>&expand=version"
search_response = requests.get(search_url, auth=HTTPBasicAuth(EMAIL, API_TOKEN)).json()

if not search_response["results"]:
    print("❌ Page not found.")
    exit()

page = search_response["results"][0]
page_id = page["id"]
current_version = page["version"]["number"]

# Step 3: Fetch HTML content
html_response = requests.get(GITHUB_HTML_URL)
html_content = html_response.text

# Step 4: Update the page
update_payload = {
    "id": page_id,
    "type": "page",
    "title": today_title,
    "body": {
        "storage": {
            "value": html_content,
            "representation": "storage"
        }
    },
    "version": {
        "number": current_version + 1
    }
}

update_url = f"{CONFLUENCE_BASE_URL}/rest/api/content/{page_id}"
update_response = requests.put(update_url, json=update_payload, auth=HTTPBasicAuth(EMAIL, API_TOKEN))

if update_response.status_code == 200:
    print("✅ Page updated successfully.")
else:
    print(f"❌ Failed to update page: {update_response.status_code}")
    print(update_response.text)
