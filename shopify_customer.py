import shopify
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_shopify_customer(customer_id):
    """
    Fetches customer details from Shopify by ID.
    Returns a dict with first_name, last_name, email if found, else None.
    """
    shop_name = os.getenv("SHOPIFY_SHOP_NAME")
    api_key = os.getenv("SHOPIFY_API_KEY")
    password = os.getenv("SHOPIFY_PASSWORD")
    api_version = os.getenv("SHOPIFY_API_VERSION", "2024-04")

    if not all([shop_name, password]):
        print("Error: Missing Shopify credentials in .env")
        return None

    shop_url = f"{shop_name}.myshopify.com"
    
    try:
        session = shopify.Session(shop_url, api_version, password)
        shopify.ShopifyResource.activate_session(session)
        
        # Shopify IDs in API are usually just the number, but let's handle if it's passed as string
        customer = shopify.Customer.find(customer_id)
        
        if customer:
            return {
                'first_name': customer.first_name,
                'last_name': customer.last_name,
                'email': customer.email,
                'id': customer.id
            }
            
    except Exception as e:
        print(f"Error fetching customer {customer_id} from Shopify: {e}")
        return None
    finally:
        if shopify.ShopifyResource.site:
            shopify.ShopifyResource.clear_session()

if __name__ == "__main__":
    # Test with a dummy ID or one provided via args
    import sys
    if len(sys.argv) > 1:
        print(get_shopify_customer(sys.argv[1]))
    else:
        print("Usage: python shopify_customer.py <customer_id>")
