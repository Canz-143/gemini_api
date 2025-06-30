import requests
import json
from app.config import FIRECRAWL_API_KEY

def call_firecrawl_extractor(links):
    # Only send the first 10 links
    limited_links = links[:5]
    print(f"[Firecrawl] Sending URLs (max 5): {limited_links}")  # Log the URLs being sent
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
    return response.json()
