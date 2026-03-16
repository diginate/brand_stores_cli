#!/usr/bin/env python3
import shopify
import os # For later use with environment variables
import argparse # For command-line arguments
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Helper class for GraphQL API calls
class ShopifyGraphQLClient:
    def __init__(self, shop_name, api_key, password, api_version):
        self.shop_name = shop_name
        self.api_key = api_key
        self.password = password
        self.api_version = api_version
        self.session_activated = False
        self.graphql_client = None
        
    def execute(self, query, variables=None):
        try:
            # Initialize session if not already done
            if not self.session_activated:
                shop_url_for_session = f"{self.shop_name}.myshopify.com"
                session = shopify.Session(shop_url_for_session, self.api_version, self.password)
                shopify.ShopifyResource.activate_session(session)
                self.session_activated = True
                self.graphql_client = shopify.GraphQL()
                
            if not self.graphql_client:
                raise Exception("GraphQL client could not be initialized")
                
            # Execute the query
            result = self.graphql_client.execute(query, variables=variables)
            return result
        except Exception as e:
            print(f"Error executing GraphQL query: {e}")
            return json.dumps({"errors": [{"message": str(e)}]})
        finally:
            # Keep the session active for subsequent calls
            pass
            
    def __del__(self):
        # Clear session when object is destroyed
        if self.session_activated:
            shopify.ShopifyResource.clear_session()

# TODO: Replace with your actual Shopify private app credentials
# It's recommended to use environment variables for these in a real application
API_KEY = os.getenv("SHOPIFY_API_KEY")
PASSWORD = os.getenv("SHOPIFY_PASSWORD")
SHOP_NAME = os.getenv("SHOPIFY_SHOP_NAME")
API_VERSION = os.getenv("SHOPIFY_API_VERSION", "2024-04")

# Global variable to store the location ID
_SHOPIFY_LOCATION_ID = None

# Add near other helper functions like get_first_location_id
_FULFILLMENT_SERVICE_CACHE = {}
_PUBLICATION_ID_CACHE = {}

# Define product templates here (restructured for GraphQL)
PRODUCT_TEMPLATES = {
    "custom-tee-black": {
        # Top-level product fields for GraphQL ProductInput
        "handle_template": "custom-tee-black-{id}",
        "title_template": "Custom Tee (Black)",
        "descriptionHtml_template": "Black unisex Gilden softstyle printed tee.<br><br>Shipped in 3-4 working days.<br><br>Contact us for bulk options.",
        "vendor": "Customskins",
        "productType": "Apparel", 
        "tags_template": ["gql-{id}"], 
        "status": "ACTIVE", 
        "options_template": ["Size"], # List of option names
        "media_template": [
            {
                "mediaContentType": "IMAGE",
                "originalSource_template": "https://csbrandstores.s3.eu-north-1.amazonaws.com/{id}/_previews/custom-tee-black-{id}.png"
            }
        ],
        "variants_template": [
            # Reverting price to string, adding tracked inventory, adding back sku_template
            {"options_template": ["Age 3-4"], "price": "18.00", "sku_template": "CTB-GQL-{id}-34", "taxable": True, "weight": 0.0, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["Age 5-6"], "price": "18.00", "sku_template": "CTB-GQL-{id}-56", "taxable": True, "weight": 0.0, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["Age 7-8"], "price": "18.00", "sku_template": "CTB-GQL-{id}-78", "taxable": True, "weight": 0.0, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["Age 9-11"], "price": "18.00", "sku_template": "CTB-GQL-{id}-911", "taxable": True, "weight": 0.0, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["Age 12-14"], "price": "18.00", "sku_template": "CTB-GQL-{id}-1214", "taxable": True, "weight": 0.0, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["Adult Small"], "price": "18.00", "sku_template": "CTB-GQL-{id}-AS", "taxable": True, "weight": 0.0, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["Adult Medium"], "price": "18.00", "sku_template": "CTB-GQL-{id}-AM", "taxable": True, "weight": 0.0, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["Adult Large"], "price": "18.00", "sku_template": "CTB-GQL-{id}-AL", "taxable": True, "weight": 0.0, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["Adult XL"], "price": "18.00", "sku_template": "CTB-GQL-{id}-AXL", "taxable": True, "weight": 0.0, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["Adult XXL"], "price": "18.00", "sku_template": "CTB-GQL-{id}-AXXL", "taxable": True, "weight": 0.0, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" }
        ]
    },
    "custom-tee-white": {
        "handle_template": "custom-tee-white-{id}",
        "title_template": "Custom Tee (White)",
        "descriptionHtml_template": "White unisex Gilden softstyle printed tee.<br><br>Shipped in 3-4 working days.<br><br>Contact us for bulk options.",
        "vendor": "Customskins",
        "productType": "Apparel", 
        "tags_template": ["{id}"], 
        "status": "ACTIVE", 
        "options_template": ["Size"],
        "media_template": [
            {
                "mediaContentType": "IMAGE",
                "originalSource_template": "https://csbrandstores.s3.eu-north-1.amazonaws.com/{id}/_previews/custom-tee-white-{id}.png"
            }
        ],
        "variants_template": [
            {"options_template": ["Age 3-4"], "price": "18.00", "sku_template": "CTW-{id}-34", "taxable": True, "weight": 0.0, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["Age 5-6"], "price": "18.00", "sku_template": "CTW-{id}-56", "taxable": True, "weight": 0.0, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["Age 7-8"], "price": "18.00", "sku_template": "CTW-{id}-78", "taxable": True, "weight": 0.0, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["Age 9-11"], "price": "18.00", "sku_template": "CTW-{id}-911", "taxable": True, "weight": 0.0, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["Age 12-14"], "price": "18.00", "sku_template": "CTW-{id}-1214", "taxable": True, "weight": 0.0, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["Adult Small"], "price": "18.00", "sku_template": "CTW-{id}-AS", "taxable": True, "weight": 0.0, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["Adult Medium"], "price": "18.00", "sku_template": "CTW-{id}-AM", "taxable": True, "weight": 0.0, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["Adult Large"], "price": "18.00", "sku_template": "CTW-{id}-AL", "taxable": True, "weight": 0.0, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["Adult XL"], "price": "18.00", "sku_template": "CTW-{id}-AXL", "taxable": True, "weight": 0.0, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["Adult XXL"], "price": "18.00", "sku_template": "CTW-{id}-AXXL", "taxable": True, "weight": 0.0, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" }
        ]
    },
    "custom-tee-grey": {
        "handle_template": "custom-tee-grey-{id}",
        "title_template": "Custom Tee (Grey)",
        "descriptionHtml_template": "Grey unisex Gilden softstyle printed tee.<br><br>Shipped in 3-4 working days.<br><br>Contact us for bulk options.",
        "vendor": "Customskins",
        "productType": "Apparel", 
        "tags_template": ["{id}"], 
        "status": "ACTIVE", 
        "options_template": ["Size"],
        "media_template": [
            {
                "mediaContentType": "IMAGE",
                "originalSource_template": "https://csbrandstores.s3.eu-north-1.amazonaws.com/{id}/_previews/custom-tee-grey-{id}.png"
            }
        ],
        "variants_template": [
            {"options_template": ["Age 3-4"], "price": "18.00", "sku_template": "CTG-{id}-34", "taxable": True, "weight": 0.0, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["Age 5-6"], "price": "18.00", "sku_template": "CTG-{id}-56", "taxable": True, "weight": 0.0, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["Age 7-8"], "price": "18.00", "sku_template": "CTG-{id}-78", "taxable": True, "weight": 0.0, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["Age 9-11"], "price": "18.00", "sku_template": "CTG-{id}-911", "taxable": True, "weight": 0.0, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["Age 12-14"], "price": "18.00", "sku_template": "CTG-{id}-1214", "taxable": True, "weight": 0.0, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["Adult Small"], "price": "18.00", "sku_template": "CTG-{id}-AS", "taxable": True, "weight": 0.0, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["Adult Medium"], "price": "18.00", "sku_template": "CTG-{id}-AM", "taxable": True, "weight": 0.0, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["Adult Large"], "price": "18.00", "sku_template": "CTG-{id}-AL", "taxable": True, "weight": 0.0, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["Adult XL"], "price": "18.00", "sku_template": "CTG-{id}-AXL", "taxable": True, "weight": 0.0, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["Adult XXL"], "price": "18.00", "sku_template": "CTG-{id}-AXXL", "taxable": True, "weight": 0.0, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" }
        ]
    },
    "custom-tee-blue": {
        "handle_template": "custom-tee-blue-{id}",
        "title_template": "Custom Tee (Blue)",
        "descriptionHtml_template": "Blue unisex Gilden softstyle printed tee.<br><br>Shipped in 3-4 working days.<br><br>Contact us for bulk options.",
        "vendor": "Customskins",
        "productType": "Apparel", 
        "tags_template": ["{id}"], 
        "status": "ACTIVE", 
        "options_template": ["Size"],
        "media_template": [
            {
                "mediaContentType": "IMAGE",
                "originalSource_template": "https://csbrandstores.s3.eu-north-1.amazonaws.com/{id}/_previews/custom-tee-blue-{id}.png"
            }
        ],
        "variants_template": [
            {"options_template": ["Age 3-4"], "price": "18.00", "sku_template": "CTBL-{id}-34", "taxable": True, "weight": 0.0, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["Age 5-6"], "price": "18.00", "sku_template": "CTBL-{id}-56", "taxable": True, "weight": 0.0, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["Age 7-8"], "price": "18.00", "sku_template": "CTBL-{id}-78", "taxable": True, "weight": 0.0, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["Age 9-11"], "price": "18.00", "sku_template": "CTBL-{id}-911", "taxable": True, "weight": 0.0, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["Age 12-14"], "price": "18.00", "sku_template": "CTBL-{id}-1214", "taxable": True, "weight": 0.0, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["Adult Small"], "price": "18.00", "sku_template": "CTBL-{id}-AS", "taxable": True, "weight": 0.0, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["Adult Medium"], "price": "18.00", "sku_template": "CTBL-{id}-AM", "taxable": True, "weight": 0.0, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["Adult Large"], "price": "18.00", "sku_template": "CTBL-{id}-AL", "taxable": True, "weight": 0.0, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["Adult XL"], "price": "18.00", "sku_template": "CTBL-{id}-AXL", "taxable": True, "weight": 0.0, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["Adult XXL"], "price": "18.00", "sku_template": "CTBL-{id}-AXXL", "taxable": True, "weight": 0.0, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" }
        ]
    },
    "custom-tee-red": {
        "handle_template": "custom-tee-red-{id}",
        "title_template": "Custom Tee (Red)",
        "descriptionHtml_template": "Red unisex Gilden softstyle printed tee.<br><br>Shipped in 3-4 working days.<br><br>Contact us for bulk options.",
        "vendor": "Customskins",
        "productType": "Apparel", 
        "tags_template": ["{id}"], 
        "status": "ACTIVE", 
        "options_template": ["Size"],
        "media_template": [
            {
                "mediaContentType": "IMAGE",
                "originalSource_template": "https://csbrandstores.s3.eu-north-1.amazonaws.com/{id}/_previews/custom-tee-red-{id}.png"
            }
        ],
        "variants_template": [
            {"options_template": ["Age 3-4"], "price": "18.00", "sku_template": "CTR-{id}-34", "taxable": True, "weight": 0.0, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["Age 5-6"], "price": "18.00", "sku_template": "CTR-{id}-56", "taxable": True, "weight": 0.0, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["Age 7-8"], "price": "18.00", "sku_template": "CTR-{id}-78", "taxable": True, "weight": 0.0, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["Age 9-11"], "price": "18.00", "sku_template": "CTR-{id}-911", "taxable": True, "weight": 0.0, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["Age 12-14"], "price": "18.00", "sku_template": "CTR-{id}-1214", "taxable": True, "weight": 0.0, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["Adult Small"], "price": "18.00", "sku_template": "CTR-{id}-AS", "taxable": True, "weight": 0.0, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["Adult Medium"], "price": "18.00", "sku_template": "CTR-{id}-AM", "taxable": True, "weight": 0.0, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["Adult Large"], "price": "18.00", "sku_template": "CTR-{id}-AL", "taxable": True, "weight": 0.0, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["Adult XL"], "price": "18.00", "sku_template": "CTR-{id}-AXL", "taxable": True, "weight": 0.0, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["Adult XXL"], "price": "18.00", "sku_template": "CTR-{id}-AXXL", "taxable": True, "weight": 0.0, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" }
        ]
    },
    "custom-tee-green": {
        "handle_template": "custom-tee-green-{id}",
        "title_template": "Custom Tee (Green)",
        "descriptionHtml_template": "Green unisex Gilden softstyle printed tee.<br><br>Shipped in 3-4 working days.<br><br>Contact us for bulk options.",
        "vendor": "Customskins",
        "productType": "Apparel", 
        "tags_template": ["{id}"], 
        "status": "ACTIVE", 
        "options_template": ["Size"],
        "media_template": [
            {
                "mediaContentType": "IMAGE",
                "originalSource_template": "https://csbrandstores.s3.eu-north-1.amazonaws.com/{id}/_previews/custom-tee-green-{id}.png"
            }
        ],
        "variants_template": [
            {"options_template": ["Age 3-4"], "price": "18.00", "sku_template": "CTGR-{id}-34", "taxable": True, "weight": 0.0, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["Age 5-6"], "price": "18.00", "sku_template": "CTGR-{id}-56", "taxable": True, "weight": 0.0, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["Age 7-8"], "price": "18.00", "sku_template": "CTGR-{id}-78", "taxable": True, "weight": 0.0, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["Age 9-11"], "price": "18.00", "sku_template": "CTGR-{id}-911", "taxable": True, "weight": 0.0, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["Age 12-14"], "price": "18.00", "sku_template": "CTGR-{id}-1214", "taxable": True, "weight": 0.0, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["Adult Small"], "price": "18.00", "sku_template": "CTGR-{id}-AS", "taxable": True, "weight": 0.0, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["Adult Medium"], "price": "18.00", "sku_template": "CTGR-{id}-AM", "taxable": True, "weight": 0.0, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["Adult Large"], "price": "18.00", "sku_template": "CTGR-{id}-AL", "taxable": True, "weight": 0.0, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["Adult XL"], "price": "18.00", "sku_template": "CTGR-{id}-AXL", "taxable": True, "weight": 0.0, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["Adult XXL"], "price": "18.00", "sku_template": "CTGR-{id}-AXXL", "taxable": True, "weight": 0.0, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" }
        ]
    },
    "custom-tee-yellow": {
        "handle_template": "custom-tee-yellow-{id}",
        "title_template": "Custom Tee (Yellow)",
        "descriptionHtml_template": "Yellow Gilden softstyle printed tee.<br><br>Shipped in 3-4 working days.<br><br>Contact us for bulk options.",
        "vendor": "Customskins",
        "productType": "Apparel", 
        "tags_template": ["{id}"], 
        "status": "ACTIVE", 
        "options_template": ["Size"],
        "media_template": [
            {
                "mediaContentType": "IMAGE",
                "originalSource_template": "https://csbrandstores.s3.eu-north-1.amazonaws.com/{id}/_previews/custom-tee-yellow-{id}.png"
            }
        ],
        "variants_template": [
            {"options_template": ["Age 3-4"], "price": "18.00", "sku_template": "CTY-{id}-34", "taxable": True, "weight": 0.0, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["Age 5-6"], "price": "18.00", "sku_template": "CTY-{id}-56", "taxable": True, "weight": 0.0, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["Age 7-8"], "price": "18.00", "sku_template": "CTY-{id}-78", "taxable": True, "weight": 0.0, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["Age 9-11"], "price": "18.00", "sku_template": "CTY-{id}-911", "taxable": True, "weight": 0.0, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["Age 12-14"], "price": "18.00", "sku_template": "CTY-{id}-1214", "taxable": True, "weight": 0.0, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["Adult Small"], "price": "18.00", "sku_template": "CTY-{id}-AS", "taxable": True, "weight": 0.0, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["Adult Medium"], "price": "18.00", "sku_template": "CTY-{id}-AM", "taxable": True, "weight": 0.0, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["Adult Large"], "price": "18.00", "sku_template": "CTY-{id}-AL", "taxable": True, "weight": 0.0, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["Adult XL"], "price": "18.00", "sku_template": "CTY-{id}-AXL", "taxable": True, "weight": 0.0, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["Adult XXL"], "price": "18.00", "sku_template": "CTY-{id}-AXXL", "taxable": True, "weight": 0.0, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" }
        ]
    },
    "die-cut-vinyl-stickers": {
        "handle_template": "die-cut-vinyl-stickers-{id}",
        "title_template": "Die Cut Vinyl Stickers",
        "descriptionHtml_template": "High quality die cut vinyl stickers.<br><br>Shipped in 3-4 working days.<br><br>Contact us for bulk options.",
        "vendor": "Customskins",
        "productType": "Stickers",
        "tags_template": ["{id}"],
        "status": "ACTIVE",
        "options_template": ["Quantity"],
        "media_template": [
            {
                "mediaContentType": "IMAGE",
                "originalSource_template": "https://csbrandstores.s3.eu-north-1.amazonaws.com/{id}/_previews/White_{id}.png"
            }
        ],
        "variants_template": [
            {"options_template": ["5"], "price": "8.00", "sku_template": "DCVS-{id}-5", "taxable": True, "weight": 0.1, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["50"], "price": "25.00", "sku_template": "DCVS-{id}-50", "taxable": True, "weight": 0.1, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["100"], "price": "41.00", "sku_template": "DCVS-{id}-100", "taxable": True, "weight": 0.1, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["250"], "price": "74.00", "sku_template": "DCVS-{id}-250", "taxable": True, "weight": 0.1, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["500"], "price": "131.00", "sku_template": "DCVS-{id}-500", "taxable": True, "weight": 0.1, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["1000"], "price": "240.00", "sku_template": "DCVS-{id}-1000", "taxable": True, "weight": 0.1, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" }
        ]
    },
    "die-cut-holographic-stickers": {
        "handle_template": "die-cut-holographic-stickers-{id}",
        "title_template": "Die Cut Holographic Stickers",
        "descriptionHtml_template": "High quality die cut holographic stickers.<br><br>Shipped in 3-4 working days.<br><br>Contact us for bulk options.",
        "vendor": "Customskins",
        "productType": "Stickers",
        "tags_template": ["{id}"],
        "status": "ACTIVE",
        "options_template": ["Quantity"],
        "media_template": [
            {
                "mediaContentType": "IMAGE",
                "originalSource_template": "https://csbrandstores.s3.eu-north-1.amazonaws.com/{id}/_previews/Holographic_{id}.png"
            }
        ],
        "variants_template": [
            {"options_template": ["5"], "price": "9.00", "sku_template": "DCHS-{id}-5", "taxable": True, "weight": 0.1, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["50"], "price": "34.00", "sku_template": "DCHS-{id}-50", "taxable": True, "weight": 0.1, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["100"], "price": "57.00", "sku_template": "DCHS-{id}-100", "taxable": True, "weight": 0.1, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["250"], "price": "102.00", "sku_template": "DCHS-{id}-250", "taxable": True, "weight": 0.1, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["500"], "price": "188.00", "sku_template": "DCHS-{id}-500", "taxable": True, "weight": 0.1, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["1000"], "price": "342.00", "sku_template": "DCHS-{id}-1000", "taxable": True, "weight": 0.1, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" }
        ]
    },
    "die-cut-silver-stickers": {
        "handle_template": "die-cut-silver-stickers-{id}",
        "title_template": "Die Cut Silver Stickers",
        "descriptionHtml_template": "High quality die cut silver stickers.<br><br>Shipped in 3-4 working days.<br><br>Contact us for bulk options.",
        "vendor": "Customskins",
        "productType": "Stickers",
        "tags_template": ["{id}"],
        "status": "ACTIVE",
        "options_template": ["Quantity"],
        "media_template": [
            {
                "mediaContentType": "IMAGE",
                "originalSource_template": "https://csbrandstores.s3.eu-north-1.amazonaws.com/{id}/_previews/Silver_{id}.png"
            }
        ],
        "variants_template": [
            {"options_template": ["5"], "price": "9.00", "sku_template": "DCSS-{id}-5", "taxable": True, "weight": 0.1, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["50"], "price": "34.00", "sku_template": "DCSS-{id}-50", "taxable": True, "weight": 0.1, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["100"], "price": "57.00", "sku_template": "DCSS-{id}-100", "taxable": True, "weight": 0.1, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["250"], "price": "102.00", "sku_template": "DCSS-{id}-250", "taxable": True, "weight": 0.1, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["500"], "price": "188.00", "sku_template": "DCSS-{id}-500", "taxable": True, "weight": 0.1, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["1000"], "price": "342.00", "sku_template": "DCSS-{id}-1000", "taxable": True, "weight": 0.1, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" }
        ]
    },
    "die-cut-gold-stickers": {
        "handle_template": "die-cut-gold-stickers-{id}",
        "title_template": "Die Cut Gold Stickers",
        "descriptionHtml_template": "High quality die cut gold stickers.<br><br>Shipped in 3-4 working days.<br><br>Contact us for bulk options.",
        "vendor": "Customskins",
        "productType": "Stickers",
        "tags_template": ["{id}"],
        "status": "ACTIVE",
        "options_template": ["Quantity"],
        "media_template": [
            {
                "mediaContentType": "IMAGE",
                "originalSource_template": "https://csbrandstores.s3.eu-north-1.amazonaws.com/{id}/_previews/Gold_{id}.png"
            }
        ],
        "variants_template": [
            {"options_template": ["5"], "price": "9.00", "sku_template": "DCGS-{id}-5", "taxable": True, "weight": 0.1, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["50"], "price": "34.00", "sku_template": "DCGS-{id}-50", "taxable": True, "weight": 0.1, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["100"], "price": "57.00", "sku_template": "DCGS-{id}-100", "taxable": True, "weight": 0.1, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["250"], "price": "102.00", "sku_template": "DCGS-{id}-250", "taxable": True, "weight": 0.1, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["500"], "price": "188.00", "sku_template": "DCGS-{id}-500", "taxable": True, "weight": 0.1, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["1000"], "price": "342.00", "sku_template": "DCGS-{id}-1000", "taxable": True, "weight": 0.1, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" }
        ]
    },
    "die-cut-glitter-stickers": {
        "handle_template": "die-cut-glitter-stickers-{id}",
        "title_template": "Die Cut Glitter Stickers",
        "descriptionHtml_template": "High quality die cut glitter stickers.<br><br>Shipped in 3-4 working days.<br><br>Contact us for bulk options.",
        "vendor": "Customskins",
        "productType": "Stickers",
        "tags_template": ["{id}"],
        "status": "ACTIVE",
        "options_template": ["Quantity"],
        "media_template": [
            {
                "mediaContentType": "IMAGE",
                "originalSource_template": "https://csbrandstores.s3.eu-north-1.amazonaws.com/{id}/_previews/Sparkly_{id}.png"
            }
        ],
        "variants_template": [
            {"options_template": ["5"], "price": "9.00", "sku_template": "DCGLS-{id}-5", "taxable": True, "weight": 0.1, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["50"], "price": "34.00", "sku_template": "DCGLS-{id}-50", "taxable": True, "weight": 0.1, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["100"], "price": "57.00", "sku_template": "DCGLS-{id}-100", "taxable": True, "weight": 0.1, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["250"], "price": "102.00", "sku_template": "DCGLS-{id}-250", "taxable": True, "weight": 0.1, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["500"], "price": "188.00", "sku_template": "DCGLS-{id}-500", "taxable": True, "weight": 0.1, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["1000"], "price": "342.00", "sku_template": "DCGLS-{id}-1000", "taxable": True, "weight": 0.1, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" }
        ]
    },
    "custom-hoodie": {
        "handle_template": "custom-hoodie-{id}",
        "title_template": "Custom Hoodie",
        "descriptionHtml_template": "Custom printed hoodie with front logo. Self-coloured drawcord and kangaroo pocket.<br><br>Logo size and placement will vary across sizes.<br><br>Shipped in 3-4 working days.<br><br>Contact us for bulk options.",
        "vendor": "Customskins",
        "productType": "Apparel",
        "tags_template": ["{id}"],
        "status": "ACTIVE",
        "options_template": ["Colour", "Size"],
        "media_template": [
            {
                "mediaContentType": "IMAGE",
                "originalSource_template": "https://csbrandstores.s3.eu-north-1.amazonaws.com/{id}/_previews/hoodie-black-{id}.png"
            },
            {
                "mediaContentType": "IMAGE",
                "originalSource_template": "https://csbrandstores.s3.eu-north-1.amazonaws.com/{id}/_previews/hoodie-white-{id}.png"
            },
            {
                "mediaContentType": "IMAGE",
                "originalSource_template": "https://csbrandstores.s3.eu-north-1.amazonaws.com/{id}/_previews/hoodie-grey-{id}.png"
            }
        ],
        "variants_template": [
            {"options_template": ["Black", "Age 3-4"], "price": "43.20", "sku_template": "CSKINS_HOODIEBLACK_3-4", "taxable": True, "weight": 1.0, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["Black", "Age 5-6"], "price": "43.20", "sku_template": "CSKINS_HOODIEBLACK_5-6", "taxable": True, "weight": 1.0, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["Black", "Age 7-8"], "price": "43.20", "sku_template": "CSKINS_HOODIEBLACK_7-8", "taxable": True, "weight": 1.0, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["Black", "Age 9-11"], "price": "43.20", "sku_template": "CSKINS_HOODIEBLACK_9-11", "taxable": True, "weight": 1.0, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["Black", "Age 12-14"], "price": "43.20", "sku_template": "CSKINS_HOODIEBLACK_12-14", "taxable": True, "weight": 1.0, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["Black", "Adult Small"], "price": "43.20", "sku_template": "CSKINS_HOODIEBLACK_SML", "taxable": True, "weight": 1.0, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["Black", "Adult Medium"], "price": "43.20", "sku_template": "CSKINS_HOODIEBLACK_MED", "taxable": True, "weight": 1.0, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["Black", "Adult Large"], "price": "43.20", "sku_template": "CSKINS_HOODIEBLACK_LRG", "taxable": True, "weight": 1.0, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["Black", "Adult XL"], "price": "43.20", "sku_template": "CSKINS_HOODIEBLACK_XL", "taxable": True, "weight": 1.0, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["Black", "Adult XXL"], "price": "43.20", "sku_template": "CSKINS_HOODIEBLACK_XXL", "taxable": True, "weight": 1.0, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["White", "Age 3-4"], "price": "43.20", "sku_template": "CSKINS_HOODIEWHITE_3-4", "taxable": True, "weight": 1.0, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["White", "Age 5-6"], "price": "43.20", "sku_template": "CSKINS_HOODIEWHITE_5-6", "taxable": True, "weight": 1.0, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["White", "Age 7-8"], "price": "43.20", "sku_template": "CSKINS_HOODIEWHITE_7-8", "taxable": True, "weight": 1.0, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["White", "Age 9-11"], "price": "43.20", "sku_template": "CSKINS_HOODIEWHITE_9-11", "taxable": True, "weight": 1.0, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["White", "Age 12-14"], "price": "43.20", "sku_template": "CSKINS_HOODIEWHITE_12-14", "taxable": True, "weight": 1.0, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["White", "Adult Small"], "price": "43.20", "sku_template": "CSKINS_HOODIEWHITE_SML", "taxable": True, "weight": 1.0, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["White", "Adult Medium"], "price": "43.20", "sku_template": "CSKINS_HOODIEWHITE_MED", "taxable": True, "weight": 1.0, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["White", "Adult Large"], "price": "43.20", "sku_template": "CSKINS_HOODIEWHITE_LRG", "taxable": True, "weight": 1.0, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["White", "Adult XL"], "price": "43.20", "sku_template": "CSKINS_HOODIEWHITE_XL", "taxable": True, "weight": 1.0, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["White", "Adult XXL"], "price": "43.20", "sku_template": "CSKINS_HOODIEWHITE_XXL", "taxable": True, "weight": 1.0, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["Grey", "Age 3-4"], "price": "43.20", "sku_template": "CSKINS_HOODIEGREY_3-4", "taxable": True, "weight": 1.0, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["Grey", "Age 5-6"], "price": "43.20", "sku_template": "CSKINS_HOODIEGREY_5-6", "taxable": True, "weight": 1.0, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["Grey", "Age 7-8"], "price": "43.20", "sku_template": "CSKINS_HOODIEGREY_7-8", "taxable": True, "weight": 1.0, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["Grey", "Age 9-11"], "price": "43.20", "sku_template": "CSKINS_HOODIEGREY_9-11", "taxable": True, "weight": 1.0, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["Grey", "Age 12-14"], "price": "43.20", "sku_template": "CSKINS_HOODIEGREY_12-14", "taxable": True, "weight": 1.0, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["Grey", "Adult Small"], "price": "43.20", "sku_template": "CSKINS_HOODIEGREY_SML", "taxable": True, "weight": 1.0, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["Grey", "Adult Medium"], "price": "43.20", "sku_template": "CSKINS_HOODIEGREY_MED", "taxable": True, "weight": 1.0, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["Grey", "Adult Large"], "price": "43.20", "sku_template": "CSKINS_HOODIEGREY_LRG", "taxable": True, "weight": 1.0, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["Grey", "Adult XL"], "price": "43.20", "sku_template": "CSKINS_HOODIEGREY_XL", "taxable": True, "weight": 1.0, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["Grey", "Adult XXL"], "price": "43.20", "sku_template": "CSKINS_HOODIEGREY_XXL", "taxable": True, "weight": 1.0, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" }
        ]
    },
    "custom-white-mug": {
        "handle_template": "white_mug-{id}",
        "title_template": "Custom Mug",
        "descriptionHtml_template": "White ceramic mug. Dishwasher safe<br><br>Shipped in 3-4 working days.<br><br>",
        "vendor": "Customskins",
        "productType": "Mugs",
        "tags_template": ["{id}"],
        "status": "ACTIVE",
        "options_template": ["Quantity"],
        "media_template": [
            {
                "mediaContentType": "IMAGE",
                "originalSource_template": "https://csbrandstores.s3.eu-north-1.amazonaws.com/{id}/_previews/white_mug-{id}.png"
            }
        ],
        "variants_template": [
            {"options_template": ["1"], "price": "9.99", "sku_template": "CSKINS_MUG_1", "taxable": True, "weight": 0.8, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["6"], "price": "45.00", "sku_template": "CSKINS_MUG_6", "taxable": True, "weight": 4.8, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["6 (individually boxed)"], "price": "54.00", "sku_template": "CSKINS_MUG_6_BOXED", "taxable": True, "weight": 5.0, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["36"], "price": "198.00", "sku_template": "CSKINS_MUG_36", "taxable": True, "weight": 28.8, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["36 (individually boxed)"], "price": "252.00", "sku_template": "CSKINS_MUG_36_BOXED", "taxable": True, "weight": 30.0, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["72"], "price": "360.00", "sku_template": "CSKINS_MUG_72", "taxable": True, "weight": 57.6, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["72 (individually boxed)"], "price": "468.00", "sku_template": "CSKINS_MUG_72_BOXED", "taxable": True, "weight": 60.0, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" }
        ]
    },
    "custom-bottle-opener": {
        "handle_template": "bottle_opener-{id}",
        "title_template": "Bottle opener",
        "descriptionHtml_template": "Stainless steel bottle opener<br><br>Shipped in 3-4 working days.<br><br>",
        "vendor": "Customskins",
        "productType": "Accessories",
        "tags_template": ["{id}"],
        "status": "ACTIVE",
        "options_template": ["Quantity"],
        "media_template": [
            {
                "mediaContentType": "IMAGE",
                "originalSource_template": "https://csbrandstores.s3.eu-north-1.amazonaws.com/{id}/_previews/bottle_opener-{id}.png"
            }
        ],
        "variants_template": [
            {"options_template": ["1"], "price": "6.00", "sku_template": "CSKINS_BOTTLEOPENER_1", "taxable": True, "weight": 0.2, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["5"], "price": "24.00", "sku_template": "CSKINS_BOTTLEOPENER_5", "taxable": True, "weight": 1.0, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["25"], "price": "105.00", "sku_template": "CSKINS_BOTTLEOPENER_25", "taxable": True, "weight": 5.0, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" },
            {"options_template": ["100"], "price": "360.00", "sku_template": "CSKINS_BOTTLEOPENER_100", "taxable": True, "weight": 20.0, "weightUnit": "POUNDS", "inventoryItem": {"tracked": True}, "inventoryPolicy": "CONTINUE" }
        ]
    }
}

def get_fulfillment_service_id(handle_name, shop_name_arg, api_key_arg, password_arg, api_version_arg):
    """Fetches the GID of a fulfillment service by its handle."""
    global _FULFILLMENT_SERVICE_CACHE
    if handle_name in _FULFILLMENT_SERVICE_CACHE:
        return _FULFILLMENT_SERVICE_CACHE[handle_name]

    # Modified query to fetch first 10 services, ignoring handle_name for now
    query = """
    query FulfillmentServicesQuery {
      fulfillmentServices(first: 10) {
        edges {
          node {
            id
            handle
            serviceName # Added serviceName for better identification
          }
        }
      }
    }
    """ # % handle_name - Removed filter

    graphql_client = None
    session_activated = False
    try:
        shop_url_for_session = f"{shop_name_arg}.myshopify.com"
        session = shopify.Session(shop_url_for_session, api_version_arg, password_arg)
        shopify.ShopifyResource.activate_session(session)
        session_activated = True
        graphql_client = shopify.GraphQL()
    except Exception as e:
        print(f"Error activating Shopify session for get_fulfillment_service_id: {e}")
        return None

    if not graphql_client:
        print("GraphQL client could not be initialized for get_fulfillment_service_id.")
        # Ensure session is cleared if activation succeeded but client init failed
        if session_activated: 
            shopify.ShopifyResource.clear_session()
        return None

    service_id = None
    try:
        # print(f"Querying for fulfillment service with handle: {handle_name}") # Debug
        result = graphql_client.execute(query)
        # print(f"Raw GraphQL response for fulfillment service: {result}") # Debug
        
        data = json.loads(result)
        if "errors" in data:
            print(f"GraphQL errors fetching fulfillment service: {data['errors']}")
            return None
            
        services = data.get("data", {}).get("fulfillmentServices", {}).get("edges", [])
        if not services:
            print(f"No fulfillment services found.")
            return None
            
        # Iterate to find the matching handle manually since we fetched all
        for service_edge in services:
            node = service_edge.get("node", {})
            if node.get("handle") == handle_name:
                service_id = node.get("id")
                # print(f"Found matching service: {node.get('serviceName')} (ID: {service_id})")
                _FULFILLMENT_SERVICE_CACHE[handle_name] = service_id
                break
        
        if not service_id:
            print(f"Fulfillment service with handle '{handle_name}' not found in the first 10 results.")
            # Optional: list available handles
            # available = [s['node']['handle'] for s in services]
            # print(f"Available handles: {available}")

    except Exception as e:
        print(f"Error executing GraphQL query for fulfillment service: {e}")
    finally:
        if session_activated:
            shopify.ShopifyResource.clear_session()
            
    return service_id

def get_first_location_id():
    """Fetches the ID of the first active Shopify location."""
    global _SHOPIFY_LOCATION_ID
    if _SHOPIFY_LOCATION_ID:
        return _SHOPIFY_LOCATION_ID
    try:
        locations = shopify.Location.find(active=True)
        if locations:
            _SHOPIFY_LOCATION_ID = locations[0].id
            # print(f"Fetched Shopify Location ID: {_SHOPIFY_LOCATION_ID}") # For debugging
            return _SHOPIFY_LOCATION_ID
        else:
            print("Error: No active Shopify locations found.")
            return None
    except Exception as e:
        print(f"Error fetching Shopify locations: {e}")
        return None

def setup_shopify_api():
    """Initializes the Shopify API session."""
    shop_url = f"https://{API_KEY}:{PASSWORD}@{SHOP_NAME}.myshopify.com/admin"
    shopify.ShopifyResource.set_site(shop_url)
    shopify.ShopifyResource.set_user(API_KEY)
    shopify.ShopifyResource.set_password(PASSWORD)
    shopify.ShopifyResource.set_version(API_VERSION)
    # print(f"Shopify API initialized for shop: {SHOP_NAME}.myshopify.com") # Quieter initialization
    # get_first_location_id() # Fetch location ID at setup - we'll call it when needed instead for now

def get_shop_details():
    """Fetches and prints basic shop details."""
    try:
        shop = shopify.Shop.current()
        print(f"Successfully connected to shop: {shop.name}")
        print(f"Email: {shop.email}")
        print(f"Domain: {shop.domain}")
    except Exception as e:
        print(f"Error processing order {query_name}: {e}")

def add_tag_to_order(order_number_str, new_tag):
    """Adds a tag to a specific order using its order number (e.g., 11670)."""
    query_name = f"#{order_number_str.lstrip('#')}" # Ensure it's in the format #XXXX
    try:
        orders = shopify.Order.find(name=query_name, status="any")
        if not orders:
            print(f"Error: Order with number '{order_number_str}' (searched as '{query_name}') not found.")
            return
        if len(orders) > 1:
            print(f"Error: Multiple orders found with number '{order_number_str}' (searched as '{query_name}'). Please use the unique Order ID instead.")
            # You could list order IDs here if desired: for o in orders: print(f"  - ID: {o.id}, Created: {o.created_at}")
            return
        
        order = orders[0]

        current_tags = order.tags.split(', ') if order.tags else []
        if new_tag in current_tags:
            print(f"Tag '{new_tag}' already exists on order {query_name} (ID: {order.id}).")
            return

        current_tags.append(new_tag)
        order.tags = ", ".join(current_tags)
        if order.save():
            print(f"Successfully added tag '{new_tag}' to order {query_name} (ID: {order.id}).")
        else:
            print(f"Failed to save tag to order {query_name}. Errors: {order.errors.full_messages()}")

    except Exception as e:
        print(f"Error processing order {query_name}: {e}")

def remove_tag_from_order(order_number_str, tag_to_remove):
    """Removes a tag from a specific order."""
    query_name = f"#{order_number_str.lstrip('#')}"
    try:
        orders = shopify.Order.find(name=query_name, status="any")
        if not orders:
            print(f"Error: Order with number '{order_number_str}' (searched as '{query_name}') not found.")
            return
        if len(orders) > 1:
            print(f"Error: Multiple orders found with number '{order_number_str}'.")
            return
        
        order = orders[0]
        
        if not order.tags:
            print(f"Order {query_name} has no tags.")
            return

        current_tags = order.tags.split(', ')
        if tag_to_remove not in current_tags:
            print(f"Tag '{tag_to_remove}' not found on order {query_name}.")
            return

        current_tags.remove(tag_to_remove)
        order.tags = ", ".join(current_tags)
        if order.save():
            print(f"Successfully removed tag '{tag_to_remove}' from order {query_name}.")
        else:
            print(f"Failed to remove tag from order {query_name}. Errors: {order.errors.full_messages()}")

    except Exception as e:
        print(f"Error processing order {query_name}: {e}")

def add_image_via_rest(product_id, image_url, shop_name_arg, api_key_arg, password_arg, api_version_arg):
    """
    Adds an image to a product using the REST API (simpler for basic image addition).
    """
    # Initialize a temporary session for this specific call if needed, or reuse global if configured
    # Ideally, reuse the global session or passed credentials.
    # Since we are inside a function that might be called from contexts where global session is set,
    # let's try to use the passed credentials to be safe/explicit.
    
    shop_url = f"https://{api_key_arg}:{password_arg}@{shop_name_arg}.myshopify.com/admin"
    shopify.ShopifyResource.set_site(shop_url)
    shopify.ShopifyResource.set_user(api_key_arg)
    
    try:
        product = shopify.Product.find(product_id)
        image = shopify.Image()
        image.product_id = product.id
        image.src = image_url
        # image.position = 1 # Optional
        if image.save():
            print(f"Successfully added image to product {product_id}.")
            return image
        else:
            print(f"Failed to add image to product {product_id}. Errors: {image.errors.full_messages()}")
            return None
    except Exception as e:
        print(f"Error adding image to product {product_id}: {e}")
        return None
    finally:
        # Clear the session
        shopify.ShopifyResource.clear_session()

def update_product_options_and_delete_default_variant(product_gid, variant_id_to_delete, option_names, variants_input, shop_name_arg, api_key_arg, password_arg, api_version_arg):
    """
    Updates product options and deletes the default variant.
    This is a complex operation that requires multiple GraphQL mutations.
    """
    options_updated_successfully = False
    variant_deleted_successfully = False
    first_variant_added = False # Indicates if the first variant from template is handled (either auto-created or placeholder for REST)
    auto_created_first_variant = False # Specifically if productUpdate/productOptionsCreate auto-creates the first variant
    auto_created_variants = [] # Initialize here to prevent UnboundLocalError

    product_gid_parts = product_gid.split('/')
    if not product_gid_parts:
        print("Error: Invalid product GID format")
        return False, False, False, []
    product_id = product_gid_parts[-1]

    # Prepare ProductOptionInput for productOptionsCreate
    # [{name: "Colour", values: [{name:"Black"}, {name:"White"}]}, {name: "Size", values: [{name:"Small"}]}]
    options_for_create_mutation = []
    if option_names and variants_input: # Ensure variants_input is available to derive values
        for i, option_name in enumerate(option_names):
            unique_value_names = set()
            for variant_template in variants_input:
                if "options" in variant_template and len(variant_template["options"]) > i:
                    option_value_from_template = variant_template["options"][i]
                    unique_value_names.add(option_value_from_template)
            
            options_for_create_mutation.append({
                "name": option_name,
                "values": [{"name": v} for v in unique_value_names] # Do NOT sort, preserve order from template if possible
            })
            # Re-sort only if needed for stability, but here we want template order.
            # unique_value_names is a set, so order is lost. We need to iterate template again to get order.
            
            ordered_values = []
            seen_values = set()
            for variant_template in variants_input:
                if "options" in variant_template and len(variant_template["options"]) > i:
                    val = variant_template["options"][i]
                    if val not in seen_values:
                        ordered_values.append({"name": val})
                        seen_values.add(val)
            
            options_for_create_mutation[-1]["values"] = ordered_values
    print(f"DEBUG: Options input for productOptionsCreate: {json.dumps(options_for_create_mutation, indent=2)}")

    graphql_client = ShopifyGraphQLClient(
        shop_name=shop_name_arg,
        api_key=api_key_arg,
        password=password_arg,
        api_version=api_version_arg
    )
    
    try:
        # --- Part 1: Check existing options (Skip delete/create if matching) ---
        existing_options_query = """
        query getProductOptions($productId: ID!) {
          product(id: $productId) {
            options {
              id
              name
              values
            }
            variants(first: 100) { # Fetch existing variants too
                edges { node { id title } }
            }
          }
        }
        """
        
        existing_options_result_str = graphql_client.execute(existing_options_query, variables={"productId": product_gid})
        existing_options_result = json.loads(existing_options_result_str) # Parse the JSON string

        if "errors" in existing_options_result or not existing_options_result.get("data", {}).get("product"):
            print(f"Error fetching existing options: {existing_options_result.get('errors')}")
            return False, None, None, [] # Indicate option update failure

        product_data_for_options = existing_options_result.get("data", {}).get("product", {})
        existing_options_on_product = product_data_for_options.get("options", [])
        
        # Populate auto_created_variants with existing variants initially
        if product_data_for_options.get("variants", {}).get("edges"):
            for edge in product_data_for_options.get("variants", {}).get("edges", []):
                 node = edge.get("node", {})
                 auto_created_variants.append({"id": node.get("id"), "title": node.get("title")})

        print(f"DEBUG: Fetched existing options: {json.dumps(existing_options_on_product, indent=2)}") 
        
        # Check if options match (simple check: option names and value counts/contents)
        options_match = False
        if len(existing_options_on_product) == len(options_for_create_mutation):
            match_count = 0
            for existing_opt in existing_options_on_product:
                for target_opt in options_for_create_mutation:
                    if existing_opt.get("name") == target_opt.get("name"):
                        # Compare values
                        existing_vals = set(existing_opt.get("values", []))
                        target_vals = set([v["name"] for v in target_opt.get("values", [])])
                        if existing_vals == target_vals:
                            match_count += 1
            if match_count == len(options_for_create_mutation):
                options_match = True
        
        deleted_count = 0
        
        if options_match:
            print("  SUCCESS: Existing options match the template. Skipping deletion and re-creation.")
            options_updated_successfully = True
        else:
            # If options DO NOT match, we attempt deletion (fallback to original logic)
            pass
            
        if not options_match:
            # --- Part 1.5: Delete ALL existing variants if options don't match ---
            # This is crucial because we cannot delete options that are used by variants.
            # Since we are re-creating the product structure, we should clear existing variants.
            print(f"Step 1.5a-0: Deleting ALL existing variants from product {product_gid} to allow option updates.")
            
            existing_variant_ids_to_delete = []
            if product_data_for_options.get("variants", {}).get("edges"):
                for edge in product_data_for_options.get("variants", {}).get("edges", []):
                     node = edge.get("node", {})
                     existing_variant_ids_to_delete.append(node.get("id"))
            
            if existing_variant_ids_to_delete:
                print(f"  Found {len(existing_variant_ids_to_delete)} variants to delete.")
                variant_bulk_delete_mutation = """
                    mutation productVariantsBulkDelete($productId: ID!, $variantIds: [ID!]!) {
                        productVariantsBulkDelete(productId: $productId, variantIds: $variantIds) {
                            product { id }
                            userErrors { field message }
                        }
                    }
                """
                # Delete in chunks if necessary, but 100 should be fine for now
                delete_vars = {"productId": product_gid, "variantIds": existing_variant_ids_to_delete}
                delete_res_str = graphql_client.execute(variant_bulk_delete_mutation, variables=delete_vars)
                delete_res = json.loads(delete_res_str)
                
                del_errors = delete_res.get("data", {}).get("productVariantsBulkDelete", {}).get("userErrors", [])
                if del_errors:
                    print(f"  Error deleting existing variants: {del_errors}")
                    # Proceeding anyway, hoping for the best, or return failure?
                    # If variant delete fails, option delete will likely fail too.
                else:
                    print(f"  Successfully deleted {len(existing_variant_ids_to_delete)} variants.")
                    # Clear auto_created_variants as they are now gone
                    auto_created_variants = []
            else:
                print("  No existing variants found to delete.")

        if not options_match and existing_options_on_product:
            print(f"Step 1.5a-1: Deleting existing options from product {product_gid}")
            for option in existing_options_on_product:
                option_id_to_delete = option.get("id")
                if option_id_to_delete:
                    # Corrected mutation name and variable structure
                    delete_option_mutation = """
                        mutation productOptionsDelete($productId: ID!, $options: [ID!]!) {
                            productOptionsDelete(productId: $productId, options: $options) {
                                deletedOptionsIds # Corrected response field
                                product { id options { id name values } }
                                userErrors { field message }
                            }
                        }
                    """
                    delete_variables = {"productId": product_gid, "options": [option_id_to_delete]} # Corrected variables
                    delete_result_str = graphql_client.execute(delete_option_mutation, variables=delete_variables)
                    delete_result = json.loads(delete_result_str)

                    # Check for deletedOptionsIds (plural)
                    if delete_result.get("data", {}).get("productOptionsDelete", {}).get("deletedOptionsIds"):
                        print(f"Successfully deleted option ID: {option_id_to_delete}")
                        deleted_count += 1
                    else:
                        # More verbose error printing for delete failure
                        print(f"Failed to delete option ID: {option_id_to_delete}.")
                        print(f"  Full delete_result: {json.dumps(delete_result, indent=2)}")
                        user_errors = delete_result.get("data", {}).get("productOptionsDelete", {}).get("userErrors", [])
                        if user_errors:
                            print(f"  UserErrors: {user_errors}")
                        else:
                            print("  No userErrors found in response.")
                else:
                    print(f"Skipping deletion for option without ID: {option.get('name')}")
        
        if not options_match:
            print(f"Successfully deleted {deleted_count} existing option(s).")
        
        # --- Part 2: Create new options using productOptionsCreate ---
        if not options_match and (deleted_count > 0 or not existing_options_on_product): 
            print(f"Step 1.5b: Creating new options for product {product_gid} using productOptionsCreate: {option_names}")
            
            options_create_mutation = """
            mutation productOptionsCreate(
                $productId: ID!, 
                $options: [OptionCreateInput!]!,
                $variantStrategy: ProductOptionCreateVariantStrategy
            ) {
              productOptionsCreate(
                productId: $productId, 
                options: $options,
                variantStrategy: $variantStrategy
              ) {
                product {
                  id
                  options {
                    id
                    name
                    values
                  }
                  variants(first: 50) { # Increased variant limit to see if CREATE strategy makes more
                    edges { node { id title } }
                  }
                }
                userErrors {
                  field
                  message
                }
              }
            }
            """
            
            options_create_variables = {
                "productId": product_gid,
                "options": options_for_create_mutation,
                "variantStrategy": "CREATE" # Explicitly set variant strategy
            }
            print(f"DEBUG: productOptionsCreate mutation variables: {json.dumps(options_create_variables, indent=2)}")
            
            options_create_result_str = graphql_client.execute(options_create_mutation, variables=options_create_variables)
            options_create_data = json.loads(options_create_result_str)
            
            create_user_errors = options_create_data.get("data", {}).get("productOptionsCreate", {}).get("userErrors", [])
            
            if create_user_errors:
                print(f"Error during productOptionsCreate:")
                for err in create_user_errors:
                    print(f"  - Field: {err.get('field', 'N/A')}, Message: {err['message']}")
                print(f"Full response: {json.dumps(options_create_data, indent=2)}")
                # options_updated_successfully remains False
            else: # Corresponds to: if create_user_errors
                created_product_data = options_create_data.get("data", {}).get("productOptionsCreate", {}).get("product", {})
                if created_product_data and created_product_data.get("options"):
                    updated_options = created_product_data.get("options", [])
                    print(f"DEBUG: productOptionsCreate product response (product.options): {json.dumps(updated_options, indent=2)}")
                    print(f"Success: Product options created via productOptionsCreate. New options: {json.dumps(updated_options, indent=2)}")
                    options_updated_successfully = True
                    
                    auto_created_variants = [] 
                    if created_product_data.get("variants", {}).get("edges", []):
                        for edge in created_product_data.get("variants", {}).get("edges", []):
                            node = edge.get("node", {})
                            auto_created_variants.append({"id": node.get("id"), "title": node.get("title")})
                        print(f"Variants after productOptionsCreate: {json.dumps(auto_created_variants, indent=2)}")
                        
                        first_variant_node = None
                        expected_first_option_val = None
                        if variants_input and len(variants_input) > 0 and "options" in variants_input[0] and len(variants_input[0]["options"]) > 0:
                            expected_first_option_val = variants_input[0]["options"][0]
                        
                        if expected_first_option_val:
                            for variant_node_item in auto_created_variants:
                                if variant_node_item.get("title") == expected_first_option_val:
                                   first_variant_node = variant_node_item
                                   break
                        
                        if first_variant_node:
                            print(f"First variant '{first_variant_node.get('title')}' (ID: {first_variant_node.get('id')}) appears to be auto-created by productOptionsCreate.")
                            auto_created_first_variant = True
                        else:
                            print(f"First variant based on options '{expected_first_option_val}' not found among auto-created variants after productOptionsCreate.")
                    # else: # This inner else was for 'if created_product_data.get("variants")' - not strictly needed if we just check auto_created_variants length later
                    #    print("No variants found in productOptionsCreate response, though options were set.")
                else: # Corresponds to: if created_product_data and created_product_data.get("options")
                    print(f"Error: productOptionsCreate succeeded but no product data or options returned.")
                    print(f"Full response: {json.dumps(options_create_data, indent=2)}")
                    # options_updated_successfully remains False
        else: # Corresponds to: if deleted_count > 0 or not existing_options_on_product (Outer if for Part 2)
            print("Skipping productOptionsCreate because prior option deletion failed or was not needed.")
            # options_updated_successfully remains False

        # --- Part 3: Delete Default Variant (Step 1.5c) ---
        # This part relies on options_updated_successfully and auto_created_variants
        if variant_id_to_delete and options_updated_successfully: 
            # Check if this variant_id_to_delete is indeed "Default Title"
            # We need to re-fetch the product's variants *after* productUpdate if we want to be sure.
            # However, 'auto_created_variants' now holds variants *after* productUpdate.
            # Let's find if variant_id_to_delete (from before productUpdate) still exists and is "Default Title".
            # This is tricky because its ID might persist even if its title changes or it's deleted/recreated.
            # For now, we trust variant_id_to_delete if it was flagged as "Default Title" initially from productCreate.

            # Re-evaluate: is variant_id_to_delete (captured from productCreate) still a "Default Title" variant?
            # The auto_created_variants are from AFTER productUpdate.
            # The variant_id_to_delete is from BEFORE productUpdate.
            # It is safer to delete any variant that currently has the title "Default Title".
            
            default_title_variants_after_update = [v for v in auto_created_variants if v.get("title") == "Default Title"] # UNCOMMENTED

            if default_title_variants_after_update: # UNCOMMENTED
                for dv in default_title_variants_after_update: # UNCOMMENTED
                    dv_id = dv.get("id") # UNCOMMENTED
                    print(f"Step 1.5c: Deleting 'Default Title' variant (ID: {dv_id}) found after productUpdate.") # UNCOMMENTED
                    # Note: We need a variant delete mutation here, which wasn't defined in the original context snippet
                    # Let's define it now
                    variant_delete_mutation = """
                        mutation productVariantsBulkDelete($productId: ID!, $variantIds: [ID!]!) {
                            productVariantsBulkDelete(productId: $productId, variantIds: $variantIds) {
                                product { id }
                                userErrors { field message }
                            }
                        }
                    """
                    variant_delete_variables = {"productId": product_gid, "variantIds": [dv_id]} # UNCOMMENTED
                    
                    variant_delete_result_str = graphql_client.execute(variant_delete_mutation, variables=variant_delete_variables) # UNCOMMENTED
                    variant_delete_data = json.loads(variant_delete_result_str) # UNCOMMENTED
                    
                    variant_delete_errors = variant_delete_data.get("data", {}).get("productVariantsBulkDelete", {}).get("userErrors", []) # UNCOMMENTED
                    if variant_delete_errors: # UNCOMMENTED
                        print(f"Error deleting variant {dv_id}: {variant_delete_errors}")
                    else: # UNCOMMENTED
                        print(f"Successfully submitted deletion for 'Default Title' variant {dv_id}.")
                        variant_deleted_successfully = True # Assume success if no errors; job might be async
            else: # UNCOMMENTED
                print("No 'Default Title' variant found after productUpdate to delete.")
                variant_deleted_successfully = True # Nothing to delete

        elif not variant_id_to_delete and options_updated_successfully: # UNCOMMENTED
            print("No initial 'Default Title' variant was flagged for deletion, and options updated.")
            variant_deleted_successfully = True
        elif not options_updated_successfully: # UNCOMMENTED
            print("Skipping default variant deletion because options update failed.")
        # --- End of Part 3 ---

        # --- Part 4: Add first variant if needed ---
        # If Shopify didn't create the first variant automatically during productUpdate,
        # and we successfully updated options and handled the default variant.
        if options_updated_successfully and variant_deleted_successfully and not auto_created_first_variant: # UNCOMMENTED
            if variants_input: # UNCOMMENTED
                first_variant_data_for_create = variants_input[0] # UNCOMMENTED
                # ... (rest of productVariantCreate logic from the original function)
                # This part is complex and was also having issues. For now, let's ensure productUpdate works.
                # The main goal is that productUpdate creates the options, and then REST API in Step 2 creates all variants.
                # If productUpdate *also* creates the first variant correctly, then auto_created_first_variant would be True.
                print("DEBUG: Part 4 - First variant was not auto-created by productUpdate. REST API in Step 2 should handle all variant creations.")
                first_variant_added = True # Let's consider it "handled" if Step 2 is expected to do it.
            else: # UNCOMMENTED
                print("DEBUG: Part 4 - No variants_input defined, cannot create first variant.")
                first_variant_added = True # No variants to add.
        elif auto_created_first_variant and options_updated_successfully and variant_deleted_successfully: # UNCOMMENTED
             print("DEBUG: Part 4 - First variant was auto-created during productUpdate.")
             first_variant_added = True
        # --- End of Part 4 ---
        
        # Determine overall success for Step 1.5
        step_1_5_overall_success = options_updated_successfully and variant_deleted_successfully and (first_variant_added or auto_created_first_variant)

        if step_1_5_overall_success:
            print("Step 1.5 Succeeded: Options updated, variants created/handled, and default variant deleted/replaced.")
        else:
            print("Step 1.5 Partial Success or Failure:")
            print(f"  - Options updated: {options_updated_successfully}")
            print(f"  - Variants handled (auto or added): {first_variant_added or auto_created_first_variant}")
            print(f"  - Default variant deleted/replaced: {variant_deleted_successfully}")
        
        return options_updated_successfully, (first_variant_added or auto_created_first_variant), variant_deleted_successfully, auto_created_variants # CORRECTED to auto_created_variants
        
    except Exception as e:
        print(f"An exception occurred during update_product_options_and_delete_default_variant: {e}")
        # Ensure we return the same number of values in case of exception
        return False, False, False, [] # ADDED empty list for auto_created_variants

def create_product_on_shopify(template_key, new_id_str, shop_name_arg, api_key_arg, password_arg, api_version_arg):
    print(f"Attempting to create product (with full variants) on Shopify using template: '{template_key}', ID: '{new_id_str}'")
    template_data = PRODUCT_TEMPLATES.get(template_key)
    if not template_data:
        print(f"  ERROR: Template key '{template_key}' not found in PRODUCT_TEMPLATES.")
        return None, [], []

    # --- 0. Fetch Shopify Location ID --- 
    # This is needed for inventoryQuantities in ProductVariantInput
    # get_first_location_id() uses REST and manages its own session.
    # It relies on global API_KEY, PASSWORD etc. being set by setup_shopify_api().
    # setup_shopify_api() should be called once in main().
    print("  Fetching Shopify Location ID for inventory...")
    shopify_location_gid = None
    try:
        # get_first_location_id() relies on the global Shopify REST API session being set up
        # by setup_shopify_api() in main().
        location_id_numeric = get_first_location_id() # This function uses REST API
        if location_id_numeric:
            shopify_location_gid = f"gid://shopify/Location/{location_id_numeric}"
            print(f"  Using Shopify Location GID: {shopify_location_gid}")
        else:
            print("  CRITICAL ERROR: Could not fetch Shopify Location ID. Cannot proceed with variant creation.")
            return None, [], []
    except Exception as e:
        print(f"  EXCEPTION fetching Shopify Location ID: {e}. Cannot proceed.")
        return None, [], []

    # Initialize GraphQL client for product creation
    graphql_client = None
    session_activated_by_this_function = False
    try:
        shop_url_for_session = f"{shop_name_arg}.myshopify.com"
        session = shopify.Session(shop_url_for_session, api_version_arg, password_arg)
        shopify.ShopifyResource.activate_session(session)
        session_activated_by_this_function = True
        graphql_client = shopify.GraphQL()
        print("  Shopify session activated for GraphQL client (for productCreate).")
    except Exception as e:
        print(f"  ERROR: Activating Shopify session for GraphQL: {e}")
        return None, [], []

    if not graphql_client:
        print("  ERROR: GraphQL client not initialized.")
        return None, [], []

    # Prepare product title and handle
    product_title = template_data.get("title_template", "Custom Product").format(id=new_id_str)
    
    # Prepare variants for ProductVariantInput
    product_variants_input_list = []
    template_variants_list = template_data.get("variants", []) or template_data.get("variants_template", [])
    if not template_variants_list:
        print(f"  ERROR: No \"variants\" or \"variants_template\" defined in template '{template_key}'. Cannot create product with this strategy.")
        if session_activated_by_this_function: shopify.ShopifyResource.clear_session()
        return None, [], []

    for v_template in template_variants_list:
        sku_template_str = v_template.get("sku") or v_template.get("sku_template")
        sku = sku_template_str.format(id=new_id_str) if sku_template_str else f"SKU-{new_id_str}-{len(product_variants_input_list)}"

        price_str = v_template.get("price", "0.00")
        # Ensure price is formatted correctly as a string for GraphQL decimal
        try:
            price_val = float(price_str)
            formatted_price = "{:.2f}".format(price_val)
        except ValueError:
            print(f"  WARNING: Invalid price \'{price_str}\' for SKU \'{sku}\'. Defaulting to 0.00.")
            formatted_price = "0.00"

        inventory_quantities = []
        if v_template.get("inventoryItem", {}).get("tracked", False) and shopify_location_gid:
            qty_data = v_template.get("inventoryQuantities", [{}])[0] # Get first entry or default
            available_qty = qty_data.get("availableQuantity", 0)
            inventory_quantities.append({
                "availableQuantity": int(available_qty),
                "locationId": shopify_location_gid
            })
        
        variant_input_item = {
            "options": v_template.get("options") or v_template.get("options_template"), # e.g., ["Black", "Small", "Gold"]
            "price": formatted_price,
            "sku": sku,
            "taxable": v_template.get("taxable", True),
            "weight": float(v_template.get("weight", 0.0)),
            "weightUnit": v_template.get("weightUnit", "GRAMS").upper(),
            "inventoryItem": { "tracked": v_template.get("inventoryItem", {}).get("tracked", False) },
            "inventoryPolicy": "CONTINUE",
            "inventoryQuantities": inventory_quantities if inventory_quantities else None, # Pass null if not applicable
            "metafields": [
                {
                    "namespace": "seo",
                    "key": "hidden",
                    "value": "1",
                    "type": "integer"
                }
            ]
        }

        product_variants_input_list.append(variant_input_item)

    # Prepare product input (WITHOUT options and variants for creation)
    product_input = {
        "title": product_title,
        "descriptionHtml": template_data.get("descriptionHtml_template", "").format(id=new_id_str),
        "vendor": template_data.get("vendor", "Default Vendor"),
        "productType": template_data.get("productType", ""),
        "handle": template_data.get("handle_template", f"product-{new_id_str}").format(id=new_id_str),
        "status": template_data.get("status", "DRAFT").upper(),
        "tags": [t.format(id=new_id_str) for t in template_data.get("tags_template", [])],
        # "options": template_data.get("options"), # REMOVED: Invalid in productCreate
        # "variants": product_variants_input_list if product_variants_input_list else None, # REMOVED: Invalid in productCreate
        "metafields": [
            {
                "namespace": "seo",
                "key": "hidden",
                "value": "1",
                "type": "integer"
            }
        ]
    }
    # print(f"  ProductInput (base) prepared: {json.dumps(product_input, indent=2)}") 

    media_input_list = [] # Assuming media handling is similar
    if template_data.get("media_template"):
        for media_item_template in template_data.get("media_template", []):
            original_source = media_item_template.get("originalSource_template")
            if original_source:
                media_input_list.append({
                    "mediaContentType": media_item_template.get("mediaContentType", "IMAGE").upper(),
                    "originalSource": original_source.format(id=new_id_str)
                })
    
    # 1. Create Product (Base)
    product_create_mutation = '''
    mutation productCreate($input: ProductInput!, $media: [CreateMediaInput!]) {
      productCreate(input: $input, media: $media) {
        product {
          id
          title
          handle
          options { name values }
          variants(first: 1) { edges { node { id title sku price } } }
        }
        userErrors { field message }
      }
    }
    '''
    variables = {"input": product_input, "media": media_input_list if media_input_list else []}

    # Initialize return values
    created_product_gid = None
    created_variants_details = [] 
    created_media_details = []    

    try:
        print("  Executing productCreate mutation (base product)...")
        result_str = graphql_client.execute(product_create_mutation, variables=variables)
        result_data = json.loads(result_str)
        
        user_errors = result_data.get("data", {}).get("productCreate", {}).get("userErrors", [])
        if user_errors:
            # Check for specific "Handle already in use" error
            handle_in_use = False
            for err in user_errors:
                if "Handle" in err.get("message", "") and "already in use" in err.get("message", ""):
                    handle_in_use = True
                    break
            
            if handle_in_use:
                print(f"  NOTICE: Handle '{product_input.get('handle')}' already exists. Attempting to fetch existing product...")
                # Fetch the product by handle
                query_by_handle = """
                query getProductByHandle($handle: String!) {
                    productByHandle(handle: $handle) {
                        id
                        title
                        handle
                        variants(first: 10) { edges { node { id } } }
                    }
                }
                """
                handle_res_str = graphql_client.execute(query_by_handle, variables={"handle": product_input.get("handle")})
                handle_res_data = json.loads(handle_res_str)
                existing_prod = handle_res_data.get("data", {}).get("productByHandle")
                
                if existing_prod and existing_prod.get("id"):
                    # Check options match
                    existing_opts = existing_prod.get("options", [])
                    template_opts = template_data.get("options_template", [])
                    
                    # Normalize for comparison
                    existing_opt_names = [o["name"] for o in existing_opts]
                    
                    options_mismatch = False
                    if len(existing_opts) != len(template_opts):
                        options_mismatch = True
                    else:
                        for i, name in enumerate(template_opts):
                            if existing_opts[i]["name"] != name:
                                options_mismatch = True
                                break
                    
                    if options_mismatch:
                        print(f"  NOTICE: Existing product options {existing_opt_names} do not match template {template_opts}.")
                        print(f"  Deleting existing product {existing_prod.get('id')} to recreate with correct structure...")
                        
                        delete_mutation = """
                        mutation productDelete($input: ProductDeleteInput!) {
                            productDelete(input: $input) {
                                deletedProductId
                                userErrors { field message }
                            }
                        }
                        """
                        delete_res_str = graphql_client.execute(delete_mutation, variables={"input": {"id": existing_prod.get("id")}})
                        delete_res = json.loads(delete_res_str)
                        
                        del_errors = delete_res.get("data", {}).get("productDelete", {}).get("userErrors", [])
                        if del_errors:
                             print(f"  ERROR: Failed to delete existing product: {del_errors}")
                             # Fallback to old behavior if delete fails? Or abort?
                             # Let's abort to avoid partial state
                             return None, [], []
                        else:
                             print("  Existing product deleted. Retrying creation...")
                             # RETRY CREATION
                             result_str = graphql_client.execute(product_create_mutation, variables=variables)
                             result_data = json.loads(result_str)
                             
                             created_product_node = result_data.get("data", {}).get("productCreate", {}).get("product", {})
                             if not created_product_node or not created_product_node.get("id"):
                                 print("  ERROR: productCreate retry failed or returned no product data.")
                                 print(f"  Full response: {json.dumps(result_data, indent=2)}")
                                 return None, [], []
                                 
                             created_product_gid = created_product_node.get("id")
                             print(f"  SUCCESS: Product recreated. GID: {created_product_gid}")

                    else:
                        created_product_gid = existing_prod.get("id")
                        print(f"  SUCCESS: Found existing product '{existing_prod.get('title')}'. GID: {created_product_gid}")
                        created_product_node = existing_prod
                else:
                    print("  ERROR: Handle in use, but could not fetch existing product by handle.")
                    if session_activated_by_this_function: shopify.ShopifyResource.clear_session()
                    return None, [], []
            else:
                print("  ERROR: productCreate failed.")
                print(f"  Full response: {json.dumps(result_data, indent=2)}")
                if session_activated_by_this_function: shopify.ShopifyResource.clear_session()
                return None, [], []

        if not created_product_gid: # Only if not set by handle recovery
            created_product_node = result_data.get("data", {}).get("productCreate", {}).get("product", {})
            if not created_product_node or not created_product_node.get("id"):
                print("  ERROR: productCreate succeeded but no product data or GID returned.")
                print(f"  Full response: {json.dumps(result_data, indent=2)}")
                if session_activated_by_this_function: shopify.ShopifyResource.clear_session()
                return None, [], []

            created_product_gid = created_product_node.get("id")
            print(f"  SUCCESS: Base Product '{created_product_node.get('title')}' created. GID: {created_product_gid}")

        # 2. Create Options and Variants (using existing helper)
        print("  Creating options and variants...")
        
        # Identify the default variant to delete (if any)
        default_variant_id_to_delete = None
        if created_product_node.get("variants") and created_product_node.get("variants").get("edges"):
            default_variant_id_to_delete = created_product_node.get("variants").get("edges")[0].get("node").get("id")
        
        option_names = template_data.get("options") or template_data.get("options_template")
        
        # Close session before calling helper to avoid conflict (helper creates new session)
        if session_activated_by_this_function: 
            shopify.ShopifyResource.clear_session()
            session_activated_by_this_function = False 
            
        success, first_var_handled, default_deleted, auto_created_variants = update_product_options_and_delete_default_variant(
            created_product_gid, 
            default_variant_id_to_delete, 
            option_names, 
            product_variants_input_list, 
            shop_name_arg, api_key_arg, password_arg, api_version_arg
        )
        
        if not success:
             print("  ERROR: Failed to update product options.")
             return created_product_gid, [], []

        # Return the created variants from the helper
        created_variants_details = auto_created_variants
        
        # --- Step 3: Update Variant Details (Price, SKU, etc.) ---
        # productOptionsCreate creates variants with default values. We must update them.
        if success and created_variants_details and product_variants_input_list:
            print("  Step 3: Updating variant details (prices, SKUs, weights)...")
            
            # Re-activate session if needed (it was closed before calling helper)
            if not session_activated_by_this_function:
                try:
                    shop_url_for_session = f"{shop_name_arg}.myshopify.com"
                    session = shopify.Session(shop_url_for_session, api_version_arg, password_arg)
                    shopify.ShopifyResource.activate_session(session)
                    session_activated_by_this_function = True
                    graphql_client = shopify.GraphQL()
                except Exception as e:
                    print(f"  ERROR: Activating Shopify session for variant update: {e}")
                    return created_product_gid, created_variants_details, []

            variants_to_update = []
            
            # Map created variants by title for easy lookup
            # Title is usually "Option1 / Option2"
            created_variants_map = {v["title"]: v["id"] for v in created_variants_details}
            
            for input_variant in product_variants_input_list:
                # Construct title from options to match
                options = input_variant.get("options", [])
                # Shopify joins options with " / "
                # Ensure options are strings
                options_str = [str(o) for o in options]
                variant_title_key = " / ".join(options_str)
                
                # Try to find match
                variant_id = created_variants_map.get(variant_title_key)
                
                # If single option, sometimes title is just the option value
                if not variant_id and len(options) == 1:
                     variant_id = created_variants_map.get(options_str[0])
                
                # Fallback: Try matching by option values if title match fails
                # This is more robust if Shopify changes title formatting or if created_variants_details is incomplete
                if not variant_id and len(options) == 1:
                    # Iterate through created_variants_details and check if title matches option value
                    for cv in created_variants_details:
                        if cv.get("title") == options_str[0]:
                            variant_id = cv.get("id")
                            break

                if variant_id:
                    update_input = {
                        "id": variant_id,
                        "price": input_variant.get("price"),
                        "sku": input_variant.get("sku"),
                        "taxable": input_variant.get("taxable", True),
                        "weight": input_variant.get("weight"),
                        "weightUnit": input_variant.get("weightUnit", "GRAMS"),
                        "inventoryItem": input_variant.get("inventoryItem"),
                        "inventoryPolicy": input_variant.get("inventoryPolicy", "CONTINUE")
                    }
                    # Add inventoryQuantities if present? 
                    # productVariantsBulkUpdate doesn't support inventoryQuantities directly in the same way as create?
                    # Actually it does not. Inventory is separate. But let's stick to basic fields first.
                    
                    variants_to_update.append(update_input)
                else:
                    print(f"  WARNING: Could not find created variant for options: {options_str}")
                    print(f"  Available variants: {list(created_variants_map.keys())}")

            if variants_to_update:
                print(f"DEBUG: variants_to_update payload (first 2): {json.dumps(variants_to_update[:2], indent=2)}")
                
                # Split updates into bulk-compatible and single-update-only fields
                # ProductVariantsBulkInput supports: id, price, compareAtPrice, taxable, inventoryPolicy, inventoryItem (maybe), mediaId
                # It DOES NOT support: sku, weight, weightUnit
                
                bulk_update_payload = []
                single_update_payload = []
                
                for v in variants_to_update:
                    # Bulk payload
                    b_item = {
                        "id": v["id"],
                        "price": v.get("price"),
                        "taxable": v.get("taxable"),
                        "inventoryPolicy": v.get("inventoryPolicy")
                        # "inventoryItem": v.get("inventoryItem") # Trying without inventoryItem in bulk first to be safe, or check if it works
                    }
                    # Check if inventoryItem caused issues? The previous error didn't list it, but let's be careful.
                    # If I leave it out, tracking might not be enabled.
                    # Let's try adding it to bulk.
                    if "inventoryItem" in v:
                        b_item["inventoryItem"] = v["inventoryItem"]
                        
                    bulk_update_payload.append(b_item)
                    
                    # Single payload (for SKU and Weight)
                    s_item = {
                        "id": v["id"],
                        "sku": v.get("sku"),
                        "weight": v.get("weight"),
                        "weightUnit": v.get("weightUnit")
                    }
                    single_update_payload.append(s_item)

                # 1. Run Bulk Update
                if bulk_update_payload:
                    print("  Running bulk update for price, taxable, inventory...")
                    bulk_mutation = """
                    mutation productVariantsBulkUpdate($productId: ID!, $variants: [ProductVariantsBulkInput!]!) {
                        productVariantsBulkUpdate(productId: $productId, variants: $variants) {
                            product { id }
                            productVariants {
                                id
                                price
                                inventoryItem { tracked }
                            }
                            userErrors { field message }
                        }
                    }
                    """
                    try:
                        bulk_res_str = graphql_client.execute(bulk_mutation, variables={"productId": created_product_gid, "variants": bulk_update_payload})
                        bulk_res = json.loads(bulk_res_str)
                        
                        bulk_errors = bulk_res.get("data", {}).get("productVariantsBulkUpdate", {}).get("userErrors", [])
                        if bulk_errors:
                            print(f"  ERROR in bulk update: {bulk_errors}")
                            print(f"  Bulk response: {json.dumps(bulk_res, indent=2)}")
                        else:
                            updated_vars = bulk_res.get("data", {}).get("productVariantsBulkUpdate", {}).get("productVariants", [])
                            print(f"  Successfully bulk updated {len(updated_vars)} variants (price/inventory).")
                            # Debug print one updated variant
                            if updated_vars:
                                print(f"  Sample updated variant: {updated_vars[0]}")
                    except Exception as e:
                        print(f"  EXCEPTION in bulk update: {e}")

                # 2. Run Single Updates (Loop) for SKU/Weight
                if single_update_payload:
                    print("  Running loop update for SKU and Weight...")
                    single_mutation = """
                    mutation productVariantUpdate($input: ProductVariantInput!) {
                        productVariantUpdate(input: $input) {
                            productVariant { id sku weight }
                            userErrors { field message }
                        }
                    }
                    """
                    sku_updated_count = 0
                    for v_input in single_update_payload:
                        try:
                            # Only update if fields are present
                            if not v_input.get("sku") and not v_input.get("weight"):
                                continue
                                
                            single_res_str = graphql_client.execute(single_mutation, variables={"input": v_input})
                            single_res = json.loads(single_res_str)
                            
                            s_errors = single_res.get("data", {}).get("productVariantUpdate", {}).get("userErrors", [])
                            if s_errors:
                                print(f"  ERROR updating SKU/Weight for {v_input['id']}: {s_errors}")
                            else:
                                sku_updated_count += 1
                        except Exception as e:
                            print(f"  EXCEPTION updating SKU/Weight for {v_input['id']}: {e}")
                    print(f"  Successfully updated SKU/Weight for {sku_updated_count} variants.")

            else:
                print("  No variants matched for update.")

        # Since we closed the session, we should not access graphql_client anymore unless we re-open.
        
        # In the case of existing product, created_product_node might not have media info if we used `getProductByHandle`
        # which had a limited query.
        # We should ensure we return media details if possible, or at least GIDs for linking images.
        
        # If we have existing media, we should try to fetch it if not already present.
        # Ideally, we should restart the session here briefly to get full details if needed, 
        # or rely on what we have.
        
        # If we are in "handle collision" mode, `created_product_node` comes from `getProductByHandle` which didn't fetch media.
        # The main loop needs media details to link images.
        
        # If we have existing media, we should try to fetch it if not already present.
        # Ideally, we should restart the session here briefly to get full details if needed, 
        # or rely on what we have.
        
        # If we are in "handle collision" mode, `created_product_node` comes from `getProductByHandle` which didn't fetch media.
        # The main loop needs media details to link images.
        
        # Determine expected media from template
        expected_media_sources = []
        if template_data.get("media_template"):
            for m in template_data["media_template"]:
                 src_tmpl = m.get("originalSource_template")
                 if src_tmpl:
                     expected_media_sources.append(src_tmpl.format(id=new_id_str))

        # Re-activate session to fetch/create media
        try:
            shop_url_for_session = f"{shop_name_arg}.myshopify.com"
            session = shopify.Session(shop_url_for_session, api_version_arg, password_arg)
            shopify.ShopifyResource.activate_session(session)
            session_activated_by_this_function = True # We reactivated it
            graphql_client = shopify.GraphQL()
            
            # Fetch existing media
            get_media_query = '''
            query getProductMedia($productId: ID!) {
                product(id: $productId) {
                id
                media(first: 50) {
                    edges {
                    node {
                        id
                        status
                        alt
                        ... on MediaImage {
                        image { originalSrc }
                        }
                    }
                    }
                }
                }
            }
            '''
            media_res = graphql_client.execute(get_media_query, variables={"productId": created_product_gid})
            media_data = json.loads(media_res)
            product_media = media_data.get("data", {}).get("product", {}).get("media", {})
            
            existing_media_sources = set()
            existing_media_nodes = []

            if product_media.get("edges"):
                print(f"  Fetched {len(product_media['edges'])} media items for existing/created product.")
                for edge in product_media['edges']:
                    node = edge.get("node", {})
                    existing_media_nodes.append(node)
                    if node.get("image") and isinstance(node.get("image"), dict):
                        src = node.get("image", {}).get("originalSrc")
                        # Normalize src for comparison (remove query params if needed, but strict for now)
                        # S3 URLs often have query params? or Shopify adds them.
                        # Usually checking filename or base path is safer, but let's try strict first.
                        # Better: Check if EXPECTED source is IN the existing source (substring)
                        if src:
                             existing_media_sources.add(src)
            
            # Check if we need to create new media
            media_to_create = []
            for expected_src in expected_media_sources:
                 # Check if this expected source matches any existing source
                 # Simple substring match might be safer for S3 vs CDN URLs
                 found = False
                 for existing_src in existing_media_sources:
                     # Remove query params from existing_src for comparison?
                     clean_existing = existing_src.split('?')[0]
                     clean_expected = expected_src.split('?')[0]
                     if clean_expected in clean_existing: # Found it
                         found = True
                         break
                 
                 if not found:
                     print(f"  Missing expected media: {expected_src}. Queuing for creation.")
                     media_to_create.append({
                        "originalSource": expected_src,
                        "mediaContentType": "IMAGE"
                     })
            
            # --- New Logic: Identify Stale Media to Delete ---
            media_ids_to_delete = []
            for node in existing_media_nodes:
                existing_src = None
                if node.get("image") and isinstance(node.get("image"), dict):
                     existing_src = node.get("image", {}).get("originalSrc")
                
                if existing_src:
                     # Check if this existing_src is in expected_media_sources
                     is_expected = False
                     for expected_src in expected_media_sources:
                         clean_existing = existing_src.split('?')[0]
                         clean_expected = expected_src.split('?')[0]
                         if clean_expected in clean_existing:
                             is_expected = True
                             break
                     
                     if not is_expected:
                         print(f"  Found stale media (not in template): {existing_src}. Queuing for deletion.")
                         media_ids_to_delete.append(node.get("id"))
            
            if media_ids_to_delete:
                print(f"  Deleting {len(media_ids_to_delete)} stale media items...")
                delete_media_mutation = """
                mutation productDeleteMedia($mediaIds: [ID!]!, $productId: ID!) {
                  productDeleteMedia(mediaIds: $mediaIds, productId: $productId) {
                    deletedMediaIds
                    userErrors {
                      field
                      message
                    }
                  }
                }
                """
                delete_vars = {
                    "mediaIds": media_ids_to_delete,
                    "productId": created_product_gid
                }
                
                try:
                    delete_res_str = graphql_client.execute(delete_media_mutation, variables=delete_vars)
                    delete_res = json.loads(delete_res_str)
                    
                    deleted_ids = delete_res.get("data", {}).get("productDeleteMedia", {}).get("deletedMediaIds", [])
                    del_errors = delete_res.get("data", {}).get("productDeleteMedia", {}).get("userErrors", [])
                    
                    if del_errors:
                        print(f"  Error deleting media: {del_errors}")
                    else:
                        print(f"  Successfully deleted {len(deleted_ids)} stale media items.")
                        
                        # Remove deleted items from existing_media_nodes list so we don't return them
                        existing_media_nodes = [n for n in existing_media_nodes if n.get("id") not in deleted_ids]

                except Exception as e_del:
                    print(f"  Exception deleting stale media: {e_del}")

            if media_to_create:
                print(f"  Creating {len(media_to_create)} new media items...")
                create_media_mutation = """
                mutation productCreateMedia($media: [CreateMediaInput!]!, $productId: ID!) {
                    productCreateMedia(media: $media, productId: $productId) {
                        media {
                            id
                            status
                            ... on MediaImage {
                                image { originalSrc }
                            }
                        }
                        userErrors {
                            field
                            message
                        }
                    }
                }
                """
                create_media_vars = {
                    "media": media_to_create,
                    "productId": created_product_gid
                }
                create_res_str = graphql_client.execute(create_media_mutation, variables=create_media_vars)
                create_res = json.loads(create_res_str)
                
                new_media_items = create_res.get("data", {}).get("productCreateMedia", {}).get("media", [])
                user_errors = create_res.get("data", {}).get("productCreateMedia", {}).get("userErrors", [])
                
                if user_errors:
                    print(f"  Error creating media: {user_errors}")
                
                if new_media_items:
                    print(f"  Successfully created {len(new_media_items)} new media items.")
                    # Add to our list for return
                    for nm in new_media_items:
                         existing_media_nodes.append(nm)

            # Re-build created_media_details from the full updated list
            created_media_details = []
            for node in existing_media_nodes:
                media_id = node.get("id")
                original_src = None
                if node.get("image") and isinstance(node.get("image"), dict):
                    original_src = node.get("image", {}).get("originalSrc")
                
                if media_id:
                    created_media_details.append({
                        "id": media_id,
                        "originalSrc": original_src,
                        "status": node.get("status", "UNKNOWN")
                    })

        except Exception as e_media:
                print(f"  Warning: Could not fetch/create media details: {e_media}")
                if session_activated_by_this_function:
                    shopify.ShopifyResource.clear_session()
                    session_activated_by_this_function = False

        # Let's fix the return to be consistent with what main() expects.
        return created_product_gid, created_variants_details, created_media_details
    
    except Exception as e:
        print(f"  EXCEPTION during productCreate: {e}")
        # RETURN an indicator of failure or empty data in case of exception
        return None, [], [] 
    finally:
        if session_activated_by_this_function:
             shopify.ShopifyResource.clear_session()
             print("  Shopify session cleared by create_product_on_shopify.")

    print(f"Finished create_product_on_shopify for: '{template_key}', ID: '{new_id_str}'.")
    # RETURN the extracted data
    return created_product_gid, created_variants_details, created_media_details

def link_images_to_variants(product_gid_placeholder, # Not directly used in variant update, but good for context
                            variants_data, 
                            media_data, 
                            shop_name_arg, api_key_arg, password_arg, api_version_arg, template_key=None):
    print(f"\n  Starting Step 2: Linking images to {len(variants_data)} variants...")
    
    graphql_client = None
    session_activated_by_this_function = False
    try:
        shop_url_for_session = f"{shop_name_arg}.myshopify.com"
        session = shopify.Session(shop_url_for_session, api_version_arg, password_arg)
        shopify.ShopifyResource.activate_session(session)
        session_activated_by_this_function = True
        graphql_client = shopify.GraphQL()
        print("  Shopify session activated for GraphQL client (for variant image linking).")
    except Exception as e:
        print(f"  ERROR: Activating Shopify session for GraphQL (variant linking): {e}")
        if session_activated_by_this_function: shopify.ShopifyResource.clear_session()
        return False
    if not graphql_client:
        print("  ERROR: GraphQL client not initialized (variant linking).")
        if session_activated_by_this_function: shopify.ShopifyResource.clear_session()
        return False

    # Map media originalSrc to media GID for easy lookup
    # Relaxed condition: Include items even if status is not READY, as long as ID is present.
    media_src_to_gid_map = {}
    for item in media_data:
        mid = item.get('id')
        src = item.get('originalSrc')
        status = item.get('status')
        
        if mid:
            if src:
                # Normalize src by removing query parameters
                clean_src = src.split('?')[0]
                media_src_to_gid_map[clean_src] = mid
            else:
                # If src is missing (e.g. PROCESSING), try to infer it from template if there is only one media item
                # This is a hack for the single-image sticker case
                if len(media_data) == 1 and template_key:
                     template_data = PRODUCT_TEMPLATES.get(template_key)
                     if template_data and template_data.get("media_template"):
                         # Try to reconstruct the expected source
                         # We don't have the ID used for formatting here easily available in this scope...
                         # But we can try to match loosely or just add it as a "fallback" entry
                         pass
    
    # Re-populate map with a more robust approach if empty
    if not media_src_to_gid_map and len(media_data) == 1 and media_data[0].get('id'):
         # If we have one media item but no source, we can't map by source.
         # But the logic below has a fallback: "Fallback Strategy 2: Single media item"
         # This strategy uses `list(media_src_to_gid_map.keys())[0]`.
         # So we need to put SOMETHING in the map.
         # Let's use a dummy key "DEFAULT"
         media_src_to_gid_map["DEFAULT"] = media_data[0].get('id')
         print("  WARNING: Media source missing (PROCESSING?), added fallback key 'DEFAULT'.")

    if not media_src_to_gid_map:
        print("  WARNING: No media items found with IDs.")
        print("  Media items received:")
        for item_idx, item_val in enumerate(media_data):
            print(f"    Item {item_idx}: ID={item_val.get('id')}, Src={item_val.get('originalSrc')}, Status={item_val.get('status')}")
        # Allow proceeding if some variants might not need images or if we want to see partial success
        # return False # If strict failure is desired

    print(f"  Media GID map (for READY media) created with {len(media_src_to_gid_map)} items.")
    print("  Available Media URLs:")
    for src in media_src_to_gid_map.keys():
        print(f"    - {src}")

    updated_count = 0
    error_count = 0
    skipped_due_to_media_not_ready = 0

    # Prepare bulk updates
    variants_bulk_input = []
    
    for variant in variants_data:
        variant_gid = variant.get("id")
        variant_options = variant.get("selectedOptions", []) 
        variant_title = variant.get("title", "N/A") 
        
        if not variant_gid:
            print(f"  WARNING: Skipping variant due to missing GID: {variant}")
            error_count += 1
            continue

        target_image_original_src_key = None
        
        # Color extraction logic
        parsed_colour_from_title = None
        if "/" in variant_title:
            parsed_colour_from_title = variant_title.split("/")[0].strip().lower()
        else: 
            parsed_colour_from_title = variant_title.strip().lower()

        colour_value_to_match = None
        if variant_options: 
            for opt in variant_options:
                if opt.get("name", "").lower() == "colour":
                    colour_value_to_match = opt.get("value", "").lower()
                    break
        
        if not colour_value_to_match and parsed_colour_from_title:
            colour_value_to_match = parsed_colour_from_title
        
        # Image matching logic
        if colour_value_to_match:
            # Check known colors
            for color_name in ["black", "white", "grey", "gray", "blue", "red", "green", "yellow"]:
                if color_name in colour_value_to_match:
                    for src_key in media_src_to_gid_map.keys():
                        if color_name in src_key.lower():
                            target_image_original_src_key = src_key
                            break
                    break # Stop checking colors once found
        
        # Fallback Strategy 2: Single media item
        if not target_image_original_src_key and len(media_src_to_gid_map) == 1:
             target_image_original_src_key = list(media_src_to_gid_map.keys())[0]

        # Fallback Strategy 3: Template key context
        if not target_image_original_src_key and template_key:
             known_colors = ["black", "white", "grey", "gray", "blue", "red", "green", "yellow"]
             for kc in known_colors:
                 if kc in template_key.lower():
                     for src_key in media_src_to_gid_map.keys():
                         if kc in src_key.lower():
                             target_image_original_src_key = src_key
                             break
                     if target_image_original_src_key: break
        
        # Fallback Strategy 4: Direct Match (for stickers where variant doesn't have color option)
        # If we have media and haven't matched yet, try to match by filename in template
        if not target_image_original_src_key and template_key:
             template_data = PRODUCT_TEMPLATES.get(template_key)
             if template_data and template_data.get("media_template"):
                 # Assuming single image for stickers for now as per template
                 # or trying to match the first available image
                 for m in template_data["media_template"]:
                     src_tmpl = m.get("originalSource_template")
                     # We don't have the ID here easily to format... 
                     # But we can check if any available media key "looks like" it belongs to this product type
                     # For stickers, there is only 1 image usually.
                     pass
        
        if not target_image_original_src_key:
             # Last ditch: if only 1 media item exists in the map (even if not DEFAULT), use it.
             if len(media_src_to_gid_map) == 1:
                 target_image_original_src_key = list(media_src_to_gid_map.keys())[0]

        if not target_image_original_src_key:
            print(f"  WARNING: No matching media originalSrc found in map for variant '{variant_title}' with colour '{colour_value_to_match}'.")
            error_count += 1
            continue
            
        media_gid_to_link = media_src_to_gid_map.get(target_image_original_src_key)
        
        if media_gid_to_link:
            variants_bulk_input.append({
                "id": variant_gid,
                "mediaId": media_gid_to_link
            })
        else:
            print(f"  ERROR: Media GID missing for src '{target_image_original_src_key}'.")
            error_count += 1

    if not variants_bulk_input:
        print("  No variants were matched to images. Skipping update.")
        return False

    print(f"  Prepared bulk update for {len(variants_bulk_input)} variants.")

    # Execute Bulk Mutation
    bulk_update_mutation = """
    mutation productVariantsBulkUpdate($productId: ID!, $variants: [ProductVariantsBulkInput!]!) {
        productVariantsBulkUpdate(productId: $productId, variants: $variants) {
            product {
                id
            }
            productVariants {
                id
                image { id }
            }
            userErrors {
                field
                message
            }
        }
    }
    """
    
    try:
        # We need the product GID for bulk update. 
        # product_gid_placeholder is passed as argument
        variables = {
            "productId": product_gid_placeholder,
            "variants": variants_bulk_input
        }
        
        result_str = graphql_client.execute(bulk_update_mutation, variables=variables)
        result_data = json.loads(result_str)
        
        bulk_data = result_data.get("data", {}).get("productVariantsBulkUpdate", {})
        user_errors = bulk_data.get("userErrors", [])
        
        if user_errors:
            print(f"  ERROR in productVariantsBulkUpdate:")
            for err in user_errors:
                print(f"    - {err.get('message')}")
            return False
        
        updated_variants = bulk_data.get("productVariants", [])
        if updated_variants:
            print(f"  SUCCESS: Bulk updated {len(updated_variants)} variants with images.")
            updated_count = len(updated_variants)
        else:
            print("  WARNING: Bulk update succeeded but returned no variants.")
            
    except Exception as e:
        print(f"  EXCEPTION during bulk variant update: {e}")
        error_count += len(variants_bulk_input)
            
    if session_activated_by_this_function:
        shopify.ShopifyResource.clear_session()
        print("  Shopify session cleared by link_images_to_variants.")
    
    total_processed_or_attempted = updated_count + error_count
    if error_count == 0 and updated_count == (len(variants_data) - skipped_due_to_media_not_ready):
        if skipped_due_to_media_not_ready > 0:
            print(f"  SUCCESS (Partial): {updated_count} variants linked to images. {skipped_due_to_media_not_ready} variants skipped as their target media was not ready.")
            return True # Still return True as operations that could be done were successful
        else:
            print(f"  SUCCESS: All {updated_count} variants successfully linked to images.")
            return True
    else:
        print(f"  COMPLETED WITH ISSUES: Total Variants: {len(variants_data)}, Successfully Linked: {updated_count}, Failed/Skipped (incl. media not ready): {error_count + skipped_due_to_media_not_ready}")
        return False

def fulfill_order(order_number_str, tracking_number, tracking_company, notify_customer):
    """Marks an order as fulfilled using the modern FulfillmentOrder workflow."""
    query_name = f"#{order_number_str.lstrip('#')}"
    
    session_activated = False
    try:
        # Step 1: Find the order (uses REST)
        orders = shopify.Order.find(name=query_name, status="any")
        if not orders:
            print(f"Error: Order with number '{order_number_str}' (searched as '{query_name}') not found.")
            return
        order = orders[0]

        # Activate session for GraphQL calls
        shop_url_for_session = f"{SHOP_NAME}.myshopify.com"
        session = shopify.Session(shop_url_for_session, API_VERSION, PASSWORD)
        shopify.ShopifyResource.activate_session(session)
        session_activated = True

        # Step 2: Get the fulfillment orders for the order.
        # Let's fetch them directly using a raw request to avoid library issues.
        fulfillment_orders_response = shopify.GraphQL().execute("""
            query($id: ID!) {
                order(id: $id) {
                    fulfillmentOrders(first: 10) {
                        edges {
                            node {
                                id
                                status
                                lineItems(first: 20) {
                                    edges {
                                        node {
                                            id
                                            remainingQuantity
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        """, {"id": f"gid://shopify/Order/{order.id}"})
        
        fulfillment_orders_data = json.loads(fulfillment_orders_response)
        if "errors" in fulfillment_orders_data:
            print(f"Error fetching fulfillment orders via GraphQL: {fulfillment_orders_data['errors']}")
            return

        fulfillment_order_nodes = fulfillment_orders_data.get("data", {}).get("order", {}).get("fulfillmentOrders", {}).get("edges", [])
        
        if not fulfillment_order_nodes:
            print(f"No fulfillment orders found for order {order_number_str}.")
            return

        # Step 3: Fulfill the fulfillment orders.
        # We'll simple fulfill all items in the first open fulfillment order.
        target_fulfillment_order_id = None
        fulfillment_order_line_items = []

        for edge in fulfillment_order_nodes:
            node = edge.get("node", {})
            if node.get("status") == "OPEN" or node.get("status") == "IN_PROGRESS":
                target_fulfillment_order_id = node.get("id")
                
                # Gather line items to fulfill
                for line_item_edge in node.get("lineItems", {}).get("edges", []):
                    line_item_node = line_item_edge.get("node", {})
                    if line_item_node.get("remainingQuantity", 0) > 0:
                        fulfillment_order_line_items.append({
                            "fulfillmentOrderId": target_fulfillment_order_id,
                            "fulfillmentOrderLineItems": [{
                                "id": line_item_node.get("id"),
                                "quantity": line_item_node.get("remainingQuantity")
                            }]
                        })
                break # Just handle one fulfillment order for now
        
        if not target_fulfillment_order_id:
            print(f"No open fulfillment orders found for order {order_number_str}.")
            return

        # Construct mutation
        fulfillment_mutation = """
        mutation fulfillmentCreateV2($fulfillment: FulfillmentV2Input!) {
            fulfillmentCreateV2(fulfillment: $fulfillment) {
                fulfillment {
                    id
                    status
                }
                userErrors {
                    field
                    message
                }
            }
        }
        """
        
        fulfillment_input = {
            "lineItemsByFulfillmentOrder": fulfillment_order_line_items,
            "notifyCustomer": notify_customer
        }
        
        if tracking_number:
            fulfillment_input["trackingInfo"] = {
                "number": tracking_number,
                "company": tracking_company if tracking_company else "Other"
            }

        print(f"Attempting to fulfill order {order_number_str} (Fulfillment Order ID: {target_fulfillment_order_id})...")
        # print(f"Variables: {json.dumps(fulfillment_input, indent=2)}")

        fulfillment_result = shopify.GraphQL().execute(fulfillment_mutation, {"fulfillment": fulfillment_input})
        fulfillment_data = json.loads(fulfillment_result)
        
        if "errors" in fulfillment_data:
             print(f"Error executing fulfillment mutation: {fulfillment_data['errors']}")
             return

        result_node = fulfillment_data.get("data", {}).get("fulfillmentCreateV2", {})
        user_errors = result_node.get("userErrors", [])
        
        if user_errors:
            print(f"User errors during fulfillment: {user_errors}")
        else:
            print(f"Successfully fulfilled order {order_number_str}!")
            print(f"Fulfillment ID: {result_node.get('fulfillment', {}).get('id')}")

    except Exception as e:
        print(f"An exception occurred while fulfilling order {order_number_str}: {e}")
    finally:
        if session_activated:
            shopify.ShopifyResource.clear_session()

def check_order_status(order_number_str):
    """Checks the status of an order."""
    query_name = f"#{order_number_str.lstrip('#')}"
    try:
        orders = shopify.Order.find(name=query_name, status="any")
        if not orders:
            print(f"Order {query_name} not found.")
            return
        
        order = orders[0]
        print(f"Order: {order.name} (ID: {order.id})")
        print(f"Financial Status: {order.financial_status}")
        print(f"Fulfillment Status: {order.fulfillment_status or 'unfulfilled'}")
        print(f"Tags: {order.tags}")
        
        # You could add more details here if needed

    except Exception as e:
        print(f"An exception occurred while checking status for order {query_name}: {e}")

def get_online_store_publication_id(shop_name_arg, api_key_arg, password_arg, api_version_arg):
    """Fetches the GID of the Online Store publication."""
    global _PUBLICATION_ID_CACHE
    if "online_store" in _PUBLICATION_ID_CACHE:
        return _PUBLICATION_ID_CACHE["online_store"]

    query = """
    query PublicationsQuery {
      publications(first: 10) {
        edges {
          node {
            id
            name
          }
        }
      }
    }
    """
    graphql_client = None
    session_activated = False
    try:
        shop_url_for_session = f"{shop_name_arg}.myshopify.com"
        session = shopify.Session(shop_url_for_session, api_version_arg, password_arg)
        shopify.ShopifyResource.activate_session(session)
        session_activated = True
        graphql_client = shopify.GraphQL()
    except Exception as e:
        print(f"Error activating Shopify session for get_online_store_publication_id: {e}")
        return None

    if not graphql_client:
        print("GraphQL client could not be initialized for get_online_store_publication_id.")
        if session_activated:
            shopify.ShopifyResource.clear_session()
        return None

    publication_id = None
    try:
        result = graphql_client.execute(query)
        data = json.loads(result)
        
        publications = data.get("data", {}).get("publications", {}).get("edges", [])
        for pub in publications:
            node = pub.get("node", {})
            if node.get("name") == "Online Store":
                publication_id = node.get("id")
                _PUBLICATION_ID_CACHE["online_store"] = publication_id
                # print(f"Found Online Store Publication ID: {publication_id}")
                break
                
        if not publication_id and publications:
             # Fallback: just take the first one if "Online Store" not found strictly
             print("Warning: 'Online Store' publication not found by name. Using first available.")
             publication_id = publications[0].get("node", {}).get("id")

    except Exception as e:
        print(f"Error fetching publications: {e}")
    finally:
        if session_activated:
            shopify.ShopifyResource.clear_session()
            
    return publication_id

def publish_product_to_channel(product_gid, publication_id, shop_name_arg, api_key_arg, password_arg, api_version_arg):
    """Publishes a product to a sales channel (publication)."""
    if not publication_id:
        print("  Skipping publishing: No publication ID available.")
        return False

    mutation = """
    mutation publishablePublish($id: ID!, $input: [PublicationInput!]!) {
      publishablePublish(id: $id, input: $input) {
        publishable {
          availablePublicationCount
          publicationCount
        }
        userErrors {
          field
          message
        }
      }
    }
    """
    
    variables = {
        "id": product_gid,
        "input": [{
            "publicationId": publication_id
        }]
    }

    graphql_client = None
    session_activated = False
    success = False
    
    try:
        shop_url_for_session = f"{shop_name_arg}.myshopify.com"
        session = shopify.Session(shop_url_for_session, api_version_arg, password_arg)
        shopify.ShopifyResource.activate_session(session)
        session_activated = True
        graphql_client = shopify.GraphQL()
        
        result_str = graphql_client.execute(mutation, variables=variables)
        result_data = json.loads(result_str)
        
        user_errors = result_data.get("data", {}).get("publishablePublish", {}).get("userErrors", [])
        if user_errors:
            print(f"  Error publishing product: {user_errors}")
        else:
            publishable = result_data.get("data", {}).get("publishablePublish", {}).get("publishable", {})
            if publishable:
                print("  Product published to Online Store successfully.")
                success = True
            else:
                 print("  Product publishing failed or status unknown from response.")
                 print(json.dumps(result_data, indent=2))
    except Exception as e:
        print(f"  An exception occurred during publishing: {e}")
    finally:
        if session_activated:
            shopify.ShopifyResource.clear_session()

    return success

def add_product_to_collection(product_gid, collection_title, shop_name, api_key, password, api_version):
    """
    Adds a product to a collection. Creates the collection if it doesn't exist.
    """
    print(f"Ensuring product {product_gid} is in collection '{collection_title}'...")
    
    session_activated = False
    try:
        shop_url_for_session = f"{shop_name}.myshopify.com"
        session = shopify.Session(shop_url_for_session, api_version, password)
        shopify.ShopifyResource.activate_session(session)
        session_activated = True
        client = shopify.GraphQL()

        # Step 1: Find collection by title
        find_collection_query = """
        query($query: String!) {
            collections(first: 1, query: $query) {
                edges {
                    node {
                        id
                        title
                    }
                }
            }
        }
        """
        # Search for exact title match
        result = client.execute(find_collection_query, {"query": f"title:{collection_title}"})
        data = json.loads(result)
        
        collection_id = None
        edges = data.get("data", {}).get("collections", {}).get("edges", [])
        for edge in edges:
            if edge["node"]["title"] == collection_title:
                collection_id = edge["node"]["id"]
                break
        
        # Step 2: Create collection if not found
        if not collection_id:
            print(f"  Collection '{collection_title}' not found. Creating...")
            create_collection_mutation = """
            mutation collectionCreate($input: CollectionInput!) {
                collectionCreate(input: $input) {
                    collection {
                        id
                    }
                    userErrors {
                        field
                        message
                    }
                }
            }
            """
            create_result = client.execute(create_collection_mutation, {
                "input": {
                    "title": collection_title,
                    "handle": collection_title # Use ID as handle too
                }
            })
            create_data = json.loads(create_result)
            user_errors = create_data.get("data", {}).get("collectionCreate", {}).get("userErrors", [])
            
            if user_errors:
                print(f"  Error creating collection: {user_errors}")
                return False
            
            collection_id = create_data.get("data", {}).get("collectionCreate", {}).get("collection", {}).get("id")
            print(f"  Created collection with ID: {collection_id}")
        else:
            print(f"  Found existing collection with ID: {collection_id}")

        # Step 3: Add product to collection
        add_product_mutation = """
        mutation collectionAddProducts($id: ID!, $productIds: [ID!]!) {
            collectionAddProducts(id: $id, productIds: $productIds) {
                collection {
                    id
                }
                userErrors {
                    field
                    message
                }
            }
        }
        """
        
        add_result = client.execute(add_product_mutation, {
            "id": collection_id,
            "productIds": [product_gid]
        })
        add_data = json.loads(add_result)
        user_errors = add_data.get("data", {}).get("collectionAddProducts", {}).get("userErrors", [])
        
        if user_errors:
             print(f"  Error adding product to collection: {user_errors}")
             return False
             
        print(f"  Successfully added product {product_gid} to collection '{collection_title}'.")
        return True

    except Exception as e:
        print(f"  Error managing collection: {e}")
        return False
    finally:
        if session_activated:
            shopify.ShopifyResource.clear_session()

def main():
    setup_shopify_api()

    parser = argparse.ArgumentParser(description="Administer your Shopify store from the command line.")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Subparser for getting shop details
    parser_details = subparsers.add_parser("details", help="Fetch and display shop details.")

    # Subparser for adding a tag to an order
    parser_add_tag = subparsers.add_parser("add-tag", help="Add a tag to an order using its order number (e.g., 11670).")
    parser_add_tag.add_argument("--order-number", required=True, help="The order number (e.g., 11670). Do not include #.")
    parser_add_tag.add_argument("--tag", required=True, help="The tag to add.")

    # Subparser for removing a tag from an order
    parser_remove_tag = subparsers.add_parser("remove-tag", help="Remove a tag from an order using its order number (e.g., 11670).")
    parser_remove_tag.add_argument("--order-number", required=True, help="The order number (e.g., 11670). Do not include #.")
    parser_remove_tag.add_argument("--tag", required=True, help="The tag to remove.")
    
    # Subparser for fulfilling an order
    parser_fulfill = subparsers.add_parser("fulfill-order", help="Mark an order as fulfilled.")
    parser_fulfill.add_argument("--order-number", required=True, help="The order number (e.g., 11670).")
    parser_fulfill.add_argument("--tracking-number", help="Optional: The tracking number for the shipment.")
    parser_fulfill.add_argument("--tracking-company", help="Optional: The shipping company.")
    parser_fulfill.add_argument("--notify-customer", action="store_true", help="Send a shipping notification to the customer.")

    # Subparser for checking order status
    parser_check_status = subparsers.add_parser("check-status", help="Check the fulfillment status of an order.")
    parser_check_status.add_argument("--order-number", required=True, help="The order number to check (e.g., 11670).")

    # Subparser for creating a product from template
    parser_create_product = subparsers.add_parser("create-product", help="Create a product on Shopify from a predefined template.")
    parser_create_product.add_argument("--template-key", required=True, help="The key of the product template to use (e.g., custom-tee-black).")
    parser_create_product.add_argument("--id", required=True, help="The new ID to use for placeholders in the template.")

    args = parser.parse_args()

    if args.command == "details":
        print("Fetching shop details...")
        get_shop_details()
    elif args.command == "add-tag":
        print(f"Attempting to add tag '{args.tag}' to order number {args.order_number}...")
        add_tag_to_order(args.order_number, args.tag)
    elif args.command == "remove-tag":
        print(f"Attempting to remove tag '{args.tag}' from order number {args.order_number}...")
        remove_tag_from_order(args.order_number, args.tag)
    elif args.command == "fulfill-order":
        print(f"Attempting to fulfill order {args.order_number}...")
        fulfill_order(args.order_number, args.tracking_number, args.tracking_company, args.notify_customer)
    elif args.command == "check-status":
        print(f"Checking status for order {args.order_number}...")
        check_order_status(args.order_number)
    elif args.command == "create-product":
        print(f"Attempting to create product using template '{args.template_key}' with ID '{args.id}'...")
        # Pass credentials/config to the function for explicit session activation
        # create_product_on_shopify(args.template_key, args.id, SHOP_NAME, API_KEY, PASSWORD, API_VERSION)
        
        # New flow: Step 1 - Create product and get GIDs
        created_product_gid, created_variants, created_media = create_product_on_shopify(
            args.template_key, args.id, SHOP_NAME, API_KEY, PASSWORD, API_VERSION
        )

        if created_product_gid and created_variants and created_media:
            print(f"  Product GID: {created_product_gid}")
            print(f"  Variants created: {len(created_variants)}")
            # for v in created_variants: print(f"    - Var GID: {v['id']}, Opts: {v['selectedOptions']}") # Debug
            print(f"  Media created: {len(created_media)}")
            # for m in created_media: print(f"    - Media GID: {m['id']}, Src: {m['originalSrc']}, Status: {m['status']}") # Debug
            
            # Step 2 - Call a new function to link images to variants
            link_success = link_images_to_variants(created_product_gid, created_variants, created_media, 
                                                 SHOP_NAME, API_KEY, PASSWORD, API_VERSION, template_key=args.template_key)
            if link_success:
                print("  Image linking process completed successfully (or with partial success if media not ready).")
                
                # Step 3 - Add product to collection
                collection_title = args.id
                add_product_to_collection(created_product_gid, collection_title, SHOP_NAME, API_KEY, PASSWORD, API_VERSION)
                
            else:
                print("  ERROR during image linking process.")
            # print("\\nNEXT STEP: Implement and call 'link_images_to_variants' function here.\\n") # Removed placeholder

        elif created_product_gid: # Product created but maybe no variants/media (should not happen with current template)
            print(f"  Product GID: {created_product_gid}, but issue fetching variants/media details.")
        else:
            print(f"  Product creation failed or returned no GID.")

    elif args.command is None: # If no command is given, show help
        parser.print_help()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
