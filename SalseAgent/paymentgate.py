import json
import os
import requests
from dotenv import load_dotenv
from langchain_groq import ChatGroq

# Load environment variables
load_dotenv(dotenv_path='../.env.local')
groq_api_key = os.getenv('GROQ_API_KEY')
stripe_key = os.getenv('STRIPE_KEY')
from SalseAgent.productprice_mapping import get_product_id_from_query

def generate_stripe_payment_link(query: str) -> str:
    """Generate a stripe payment link for a customer based on a single query string."""

    # example testing payment gateway url
    PAYMENT_GATEWAY_URL = os.getenv(
        "PAYMENT_GATEWAY_URL", "https://agent-payments-gateway.vercel.app/payment"
    )
    PRODUCT_PRICE_MAPPING = "example_product_price_id_mapping.json"

    # use LLM to get the price_id from query
    price_id = get_product_id_from_query(query, PRODUCT_PRICE_MAPPING)
    price_id = json.loads(price_id)
    payload = json.dumps(
        {"prompt": query, **price_id, "stripe_key": stripe_key}
    )
    headers = {
        "Content-Type": "application/json",
    }

    response = requests.request(
        "POST", PAYMENT_GATEWAY_URL, headers=headers, data=payload
    )
    return response.text

# generate_stripe_payment_link(
#     query="Please generate a payment link for John Doe to buy two mattresses - the Classic Harmony Spring Mattress"
# )
