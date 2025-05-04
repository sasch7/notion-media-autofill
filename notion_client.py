import requests
import config
import logging
logger = logging.getLogger(__name__)

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
    try:
        res.raise_for_status()
    except requests.exceptions.HTTPError as e:
        logger.error(f"Notion update failed: {res.text}")
        raise e
    return res.json()

def set_page_title_not_found(page_id, title):
    error_data = {
        "properties": {
            "Title": {
                "title": [
                    {
                        "type": "text",
                        "text": {
                            "content": f"❌ {title} not found"
                        }
                    }
                ]
            }
        }
    }
    update_page(page_id, error_data)