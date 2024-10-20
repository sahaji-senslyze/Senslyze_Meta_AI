import json
from difflib import get_close_matches

# Load the product data from a JSON file
with open("SalseAgent\example_product_info.json", "r") as file:
    product_data = json.load(file)

# Function to fetch product details by name
def fetch_product_by_name(name):
    # Extract product names from the JSON
    product_names = [product['name'] for product in product_data['products']]
    
    # Find close matches (with a cutoff for similarity)
    closest_matches = get_close_matches(name, product_names, n=1, cutoff=0.6)
    
    if closest_matches:
        # Find the matching product details
        for product in product_data['products']:
            if product['name'] == closest_matches[0]:
                return product
    else:
        return f"No similar product found for: {name}"

# # Test the function
# search_name = "Luxury Cloud Mattress"  # Misspelled or partial name
# product_info = fetch_product_by_name(search_name)

# print(product_info)
