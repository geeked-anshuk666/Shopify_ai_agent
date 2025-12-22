import os
import time
import requests
import json
import logging
from dotenv import load_dotenv
from typing import Dict, Any, List, Optional, Union
from langchain.tools import tool

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

load_dotenv()

SHOPIFY_SHOP_NAME = os.getenv("SHOPIFY_SHOP_NAME")
SHOPIFY_ACCESS_TOKEN = os.getenv("SHOPIFY_ACCESS_TOKEN")
SHOPIFY_API_VERSION = os.getenv("SHOPIFY_API_VERSION", "2025-07")

BASE_URL = f"https://{SHOPIFY_SHOP_NAME}/admin/api/{SHOPIFY_API_VERSION}"

class ShopifyAPIError(Exception):
    pass

def make_shopify_request(endpoint: str, params: Dict = None, max_retries: int = 5) -> Union[requests.Response, Dict]:
    """
    Makes a GET request to Shopify Admin API.
    Returns:
        requests.Response object if successful (200).
        Dict with "error" key if failed after retries or client error.
    """
    if params is None:
        params = {}
    
    url = f"{BASE_URL}/{endpoint}.json" if not endpoint.startswith("http") else endpoint
    
    headers = {
        "X-Shopify-Access-Token": SHOPIFY_ACCESS_TOKEN,
        "Content-Type": "application/json"
    }
    
    attempt = 0
    while attempt < max_retries:
        try:
            logger.debug(f"Making request to {url} (Attempt {attempt + 1}/{max_retries})")
            response = requests.get(url, headers=headers, params=params, timeout=10)
            
            # Log Call Limit
            if "X-Shopify-Shop-Api-Call-Limit" in response.headers:
                logger.debug(f"API Call Limit: {response.headers['X-Shopify-Shop-Api-Call-Limit']}")

            if response.status_code == 200:
                return response
            
            elif response.status_code == 429:
                retry_after = float(response.headers.get("Retry-After", 2.0))
                logger.warning(f"Rate limited (429). Waiting {retry_after} seconds.")
                time.sleep(retry_after)
                attempt += 1
                continue
                
            else:
                # Client Error (4xx) - likely not temporary, return error immediately except for specific cases?
                # Actually 5xx should be retried, 4xx (except 429) should be returned.
                if 500 <= response.status_code < 600:
                     logger.warning(f"Server Error {response.status_code}. Retrying...")
                     raise requests.exceptions.RequestException(f"Server error {response.status_code}")
                
                # Parse error
                try:
                    error_msg = json.dumps(response.json().get("errors", response.text))
                except:
                    error_msg = response.text
                    
                logger.error(f"API Error {response.status_code}: {error_msg}")
                return {"error": f"API Error {response.status_code}: {error_msg}"}

        except requests.exceptions.RequestException as e:
            logger.error(f"Network/Server error: {str(e)}")
            attempt += 1
            if attempt < max_retries:
                time.sleep(2 ** attempt)
            else:
                return {"error": f"Max retries exceeded: {str(e)}"}
    
    return {"error": "Max retries exceeded"}

@tool
def get_shopify_data(resource: str, query_params: str = "{}") -> str:
    """
    Fetches data from Shopify Admin API using GET requests only.
    Supports resources like 'orders', 'products', 'customers'.
    Auto-pagination included.
    
    Args:
        resource: e.g. 'orders', 'products'
        query_params: JSON string of params
    """
    try:
        params = json.loads(query_params)
    except json.JSONDecodeError:
        return "Error: query_params must be a valid JSON string."

    if "limit" not in params:
        params["limit"] = 50
        
    current_url = resource
    all_data = []
    MAX_RECORDS = 1000
    page_count = 0
    
    try:
        while True:
            response_obj = make_shopify_request(current_url, params)
            
            if isinstance(response_obj, dict) and "error" in response_obj:
                return response_obj["error"]
            
            # response_obj is requests.Response
            try:
                data = response_obj.json()
            except json.JSONDecodeError:
                 return "Error: Failed to decode API response JSON"

            keys = list(data.keys())
            list_key = next((k for k in keys if isinstance(data[k], list)), None)
            
            if list_key:
                items = data[list_key]
                all_data.extend(items)
                page_count += 1
                logger.info(f"Fetched page {page_count} of {resource} ({len(items)} items)")
            else:
                return json.dumps(data)
            
            if len(all_data) >= MAX_RECORDS:
                break
            
            # Pagination
            link_header = response_obj.headers.get("Link")
            if not link_header:
                break
                
            links = link_header.split(",")
            next_link = None
            for link in links:
                if 'rel="next"' in link:
                    next_link = link.split(";")[0].strip("<> ")
                    break
            
            if next_link:
                current_url = next_link
                params = {} 
            else:
                break
        
        return json.dumps({resource: all_data})
        
    except Exception as e:
        logger.error(f"Critical error in get_shopify_data: {str(e)}")
        return f"Error fetching Shopify data: {str(e)}"
