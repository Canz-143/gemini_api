import requests
import json
from app.config import FIRECRAWL_API_KEY

def call_firecrawl_extractor(links):
    # Only send the first 10 links
    limited_links = links[:10]
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
            "Only get the main price and the direct product page URL; one set per URL. "
            "Include product name if available."
        ),
        "schema": {
            "type": "object",
            "properties": {
                "products": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "product_name": {"type": "string"},
                            "price": {"type": "string"},
                            "product_url": {"type": "string"}
                        },
                        "required": ["product_name", "price", "product_url"]
                    }
                }
            },
            "required": ["products"]
        }
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.json()
