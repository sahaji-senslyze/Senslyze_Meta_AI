
import json
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

# Load environment variables
load_dotenv(dotenv_path='../.env.local')
groq_api_key = os.getenv('GROQ_API_KEY')

# Initialize the ChatGroq model


# Example product price ID mapping
product_price_id_mapping = {
    "ai-consulting-services": "price_1Ow8ofB795AYY8p1goWGZi6m",
    "Luxury Cloud-Comfort Memory Foam Mattress": "price_1Owv99B795AYY8p1mjtbKyxP",
    "Classic Harmony Spring Mattress": "price_1Owv9qB795AYY8p1tPcxCM6T",
    "EcoGreen Hybrid Latex Mattress": "price_1OwvLDB795AYY8p1YBAMBcbi",
    "Plush Serenity Bamboo Mattress": "price_1OwvMQB795AYY8p1hJN2uS3S",
}

# Save the product price ID mapping to a JSON file
with open("example_product_price_id_mapping.json", "w") as f:
    json.dump(product_price_id_mapping, f)

def get_product_id_from_query(query, product_price_id_mapping_path):
    # Load the product price ID mapping from the JSON file
    with open(product_price_id_mapping_path, "r") as f:
        product_price_id_mapping = json.load(f)

    # Serialize the product_price_id_mapping to a JSON string for inclusion in the prompt
    product_price_id_mapping_json_str = json.dumps(product_price_id_mapping)

    # Dynamically create the enum list from product_price_id_mapping keys
    enum_list = list(product_price_id_mapping.values()) + [
        "No relevant product id found"
    ]
    enum_list_str = json.dumps(enum_list)

    # Build the prompt
    prompt = f"""
    You are an expert data scientist and you are working on a project to recommend products to customers based on their needs.
    Given the following query:
    {query}
    and the following product price id mapping:
    {product_price_id_mapping_json_str}
    return the price id that is most relevant to the query.
    ONLY return the price id, no other text. If no relevant price id is found, return 'No relevant price id found'.
    Your output will follow this schema:
    {{
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Price ID Response",
    "type": "object",
    "properties": {{
        "price_id": {{
        "type": "string",
        "enum": {enum_list_str}
        }}
    }},
    "required": ["price_id"]
    }}
    Return a valid directly parsable json, do not return it within a code snippet or add any kind of explanation!!
    """
    llm = ChatGroq(groq_api_key=groq_api_key, model_name="llama-3.1-70b-versatile")
    # Send the prompt to the Groq LLaMA model
    response = llm.invoke(prompt)

    # Extract the product ID from the response (assuming JSON structure)
    product_id = response.content  # Assuming response is directly the product_id

    return product_id

# # Example query
# query = "I want to buy a memory foam mattress."
# product_price_id_mapping_path = "example_product_price_id_mapping.json"
# product_id = get_product_id_from_query(query, product_price_id_mapping_path)
# print(product_id)
