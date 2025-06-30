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
            "You're extracting product data from a list of e-commerce product pages. For each URL, return a single object containing:\n"
            "- the current listed price (not MSRP or discounts unless it's the only one shown),\n"
            "- the canonical or direct product page URL,\n"
            "- and the website name.\n\n"
            "Only return data if all fields are clearly visible. Format the output strictly according to the provided schema under 'ecommerce_links'. "
            "Do not include multiple prices or links per URL."
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
