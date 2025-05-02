import requests
import config

def get_page_data(page_id):
    url = f"https://api.notion.com/v1/pages/{page_id}"
    headers = {
        "Authorization": f"Bearer {config.NOTION_TOKEN}",
        "Notion-Version": config.NOTION_VERSION
    }

    res = requests.get(url, headers=headers)
    return res.json()

def update_page(page_id, data):
    url = f"https://api.notion.com/v1/pages/{page_id}"
    headers = {
        "Authorization": f"Bearer {config.NOTION_TOKEN}",
        "Notion-Version": config.NOTION_VERSION,
        "Content-Type": "application/json"
    }

    res = requests.patch(url, headers=headers, json=data)
    res.raise_for_status()
    return res.json()
