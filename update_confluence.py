import requests
from datetime import datetime
import os
import html

# === Configuration ===
CONFLUENCE_URL = "https://prudential-ps.atlassian.net/wiki"
SPACE_KEY = "~629438789bc7150068cc65ba"  # Replace with your actual space key
EMAIL = os.environ["EMAIL"]
API_TOKEN = os.environ["API_TOKEN"]
GITHUB_HTML_URL = "https://raw.githubusercontent.com/Mia-ki/AI-Fusion-Host/main/latest.html"
PARENT_PAGE_ID = "1301512405"  # Replace with your actual parent page ID

# === Authentication ===
auth = (EMAIL, API_TOKEN)

# === Fetch HTML from GitHub ===
try:
    response = requests.get(GITHUB_HTML_URL)
    response.raise_for_status()
    html_content = response.text
except requests.RequestException as e:
    print(f"❌ Failed to fetch HTML from GitHub: {e}")
    exit(1)

# === Escape HTML for Confluence storage format ===
escaped_html = html.escape(html_content)

# === Prepare Confluence page data ===
page_title = f"AI Digest – Week of {datetime.now().strftime('%b %d, %Y')}"
page_data = {
    "type": "page",
    "title": page_title,
    "space": {"key": SPACE_KEY},
    "ancestors": [{"id": PARENT_PAGE_ID}],
    "body": {
        "storage": {
            "value": escaped_html,
            "representation": "storage"
        }
    }
}

# === Create the page in Confluence ===
try:
    post_url = f"{CONFLUENCE_URL}/rest/api/content"
    headers = {"Content-Type": "application/json"}
    post_response = requests.post(post_url, json=page_data, auth=auth, headers=headers)
    post_response.raise_for_status()
    print(f"✅ Successfully created Confluence page: {page_title}")
except requests.RequestException as e:
    print(f"❌ Failed to create Confluence page: {e}")
    print("Response:", post_response.text)
    exit(1)
