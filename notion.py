import json
import requests
import datetime
import os
from dotenv import load_dotenv


load_dotenv()

NOTION_API_KEY = os.getenv("NOTION_API_KEY")
DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

headers = {
    "Authorization": "Bearer " + NOTION_API_KEY,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

# ---------------- HELPERS -----------------


def create_page_wrapper(json_output: dict, text_content: str):
    res_arr = []
    for request in json_output['requests']:
        data = {
            "Sender Name": {"rich_text": [{"text": {"content": request['sender_name']}}]},
            "Description": {"title": [{"text": {"content": request['email_subject']}}]},
            "Company": {"rich_text": [{"text": {"content": request['client_company']}}]},
            "Date": {"date": {"start": str(datetime.date.today())}},
            "Request Type": {"type": "select", "select": {"name": request['request']}},
            "Status": {"type": "select", "select": {"name": "Todo"}},
            "Sender Email": {"rich_text": [{"text": {"content": request['sender_email']}}]},
            "Location": {"rich_text": [{"text": {"content": request['Location']}}]},
            "VLAN/IP": {"rich_text": [{"text": {"content": request['VLAN/IP']}}]},
            "Location A (DPLC)": {"rich_text": [{"text": {"content": request['Location_A_(DPLC)']}}]},
            "Location B (DPLC)": {"rich_text": [{"text": {"content": request['Location_B_(DPLC)']}}]},
            "Current bandwidth (Mbps)": {"rich_text": [{"text": {"content": request['current_bandwidth_(Mbps)']}}]},
            "Requested bandwidth (Mbps)": {"rich_text": [{"text": {"content": request['requested_bandwidth']}}]},
            "New bandwidth (Mbps)": {"rich_text": [{"text": {"content": request['new_bandwidth']}}]},
            "PIB or DPLC": {"type": "select", "select": {"name": request['PIB_or_DPLC']}},
        }

        print("Adding a request to Notion...")
        res = create_page(data, text_content)
        res_arr.append(res)

    return res_arr


def create_page(data: dict, text_content: str):
    create_url = "https://api.notion.com/v1/pages"

    # Split the text_content by newline characters
    paragraphs = text_content.split('\n')
    print(paragraphs)
    # Create a list of block objects for each paragraph
    children = [
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"type": "text", "text": {"content": paragraph.strip()}}]
            }
        }
        for paragraph in paragraphs
    ]
    payload = {
        "parent": {
            "type": "database_id",
            "database_id": "2bc241cbe7ab4a88abee8fdbc5a52c98",
        },
        "properties": data,
        "children": children
    }

    res = requests.post(create_url, headers=headers, json=payload)

    return res

# --- EXTRA FUNCTIONS ---


def get_pages(num_pages=None):
    """
    If num_pages is None, get all pages, otherwise just the defined number
    """
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"

    get_all = num_pages is None
    page_size = 100 if get_all else num_pages

    payload = {"page_size": page_size}
    response = requests.post(url, json=payload, headers=headers)

    data = response.json()

    with open('db.json', 'w', encoding='utf8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    '''
    results = data["results"]
    while data["has_more"] and get_all:
        payload = {"page_size": page_size, "start_cursor": data["next_cursor"]}
        url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()
        results.extend(data["results"])
    return results
    '''
