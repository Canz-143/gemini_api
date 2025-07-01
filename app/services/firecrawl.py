import time
import requests
import json
from app.config import FIRECRAWL_API_KEY

def call_firecrawl_extractor(links):
    # Only send the first 5 links
    limited_links = links[:5]
    print(f"[Firecrawl] Sending URLs (max 10): {limited_links}")  # Log the URLs being sent
    url = "https://api.firecrawl.dev/v1/extract"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {FIRECRAWL_API_KEY}"
    }
    payload = {
        "urls": limited_links,
        "prompt": (
            "Extract the price and product URL from the specified product page. "
            "Only get the main price even if the product is out of stock, and the direct product page URL; one set per URL. "
            "Include website name."
        ),
        "schema": {
            "type": "object",
            "properties": {
                "ecommerce_links": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "website_name": {"type": "string"},
                            "price": {"type": "string"},
                            "website_url": {"type": "string"}
                        },
                        "required": ["website_name", "price", "website_url"]
                    }
                }
            },
            "required": ["ecommerce_links"]
        }
    }
    response = requests.post(url, headers=headers, json=payload)
    firecrawl_result = response.json()

    # If success and id present, poll until status is "completed"
    firecrawl_output = None
    if firecrawl_result.get("success") and firecrawl_result.get("id"):
        firecrawl_id = firecrawl_result["id"]
        print(f"[Firecrawl] Waiting 15 seconds before fetching result for id: {firecrawl_id}")
        time.sleep(15)
        get_url = f"https://api.firecrawl.dev/v1/extract/{firecrawl_id}"
        while True:
            get_response = requests.get(get_url, headers=headers)
            firecrawl_output = get_response.json()
            status = firecrawl_output.get("status") or firecrawl_output.get("data", {}).get("status")
            print(f"[Firecrawl] Status: {status}")
            if status == "completed":
                break
            elif status == "processing":
                print("[Firecrawl] Still processing, waiting 5 seconds...")
                time.sleep(5)
            else:
                # Break on unexpected status to avoid infinite loop
                break
    return {
        "firecrawl_result": firecrawl_result,
        "firecrawl_output": firecrawl_output
    }
