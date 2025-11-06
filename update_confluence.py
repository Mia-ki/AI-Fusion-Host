import requests
from datetime import datetime
import os

# Config
CONFLUENCE_URL = "https://prudential-ps.atlassian.net/wiki"
SPACE_KEY = "~629438789bc7150068cc65ba"  # Use the space key, not the name
EMAIL = os.environ["EMAIL"]
API_TOKEN = os.environ["API_TOKEN"]
GITHUB_HTML_URL = "https://raw.githubusercontent.com/Mia-ki/AI-Fusion-Host/main/latest.html"

# Auth
auth = (EMAIL, API_TOKEN)

# Fetch HTML
html_content = requests.get(GITHUB_HTML_URL).text

# Create page
page_data = {
    "type": "page",
    "title": f"AI Digest – Week of {datetime.now().strftime('%b %d, %Y')}",
    "space": {"key": SPACE_KEY},
    "ancestors": [{"id": 1301512405}],
    "body": {
        "storage": {
            "value": html_content,
            "representation": "storage"
        }
    }
}

response = requests.post(
    f"{CONFLUENCE_URL}/rest/api/content",
    json=page_data,
    auth=auth,
    headers={"Content-Type": "application/json"}
)

print("Status:", response.status_code)
print("Response:", response.text)
