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

# Movies
# def update_movie_page(page_id, properties):
#     url = f"https://api.notion.com/v1/pages/{page_id}"
#     headers = {
#         "Authorization": f"Bearer {config.NOTION_TOKEN}",
#         "Notion-Version": config.NOTION_VERSION,
#         "Content-Type": "application/json"
#     }
#     data = {"properties": {

#     }}
#     res = requests.patch(url, headers=headers, json=data)
#     return res.json()