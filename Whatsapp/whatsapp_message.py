import requests
import json
import os
from dotenv import load_dotenv
from Store.userinfo import get_userinfo
from SalseAgent.product_info import fetch_product_by_name
from StateManager.GlobalState import GlobalStateManager
load_dotenv(dotenv_path='.env.local')


API_KEY=os.getenv("API_KEY")
RECIPIENT_NUMBER=os.getenv("RECIPIENT_NUMBER")
PHONE_NUMBER_ID=os.getenv("PHONE_NUMBER_ID")

url = f"https://partnersv1.pinbot.ai/v3/{PHONE_NUMBER_ID}/messages"

def send_memory_consent(intent = "your preference") : 
    user = get_userinfo() 
    session_id = GlobalStateManager.get_session_details()
    

    payload = json.dumps({
    "to": session_id,
    "type": "template",
    "template": {
        "language": {
        "code": "en"
        },
        "name": "memory_update",
        "components": [
        {
            "type": "body",
            "parameters": [
            {
                "type": "text",
                "text": intent
            }
            ]
        },
        {
            "type": "button", # YES BUTTON
            "sub_type": "quick_reply",
            "index": "0",
            "parameters": [
            {
                "type": "payload",
                "payload": "Yes"  # CAN PASS DYNAMIC PAYLOAD
            }
            ]
        },
        {
            "type": "button", # NO BUTTON
            "sub_type": "quick_reply",
            "index": "1",
            "parameters": [
            {
                "type": "payload",
                "payload": "No" # CAN PASS DYNAMIC PAYLOAD
            }
            ]
        }
        ]
    },
    "messaging_product": "whatsapp"
    })
    headers = {
    'apikey': API_KEY,
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    if(response.status_code == 200) : 
        print("Memory consent successfully")
    return ""

def send_whatsapp_text_message(message):
    user = get_userinfo() 
    session_id = GlobalStateManager.get_session_details()
    to = session_id
    
    payload = json.dumps({
    "to": to,
    "type": "text",
    "text": {
        "body": message
    },
    "messaging_product": "whatsapp"
    })
    headers = {
    'Content-Type': 'application/json',
    'apikey': API_KEY
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    if (response.status_code == 200):
        print("Message sent successfully")
    else:
        print(f"Failed to send message. Status code: {response.status_code}")
        print(response.text)



def send_button_message(message: str, buttons: list[str]) -> str: 
    """Sends a message with buttons to the user."""
    user = get_userinfo() 
    session_id = GlobalStateManager.get_session_details()
    to = session_id


    finalButtonsArray = [
        {
            "type": "reply", 
            "reply": {
                "id": "unique-id-" + str(i), 
                "title": title[0:20]
            }
        } for i, title in enumerate(buttons[0:3])
    ]

    payload = json.dumps({
    "messaging_product": "whatsapp",
    "recipient_type": "individual",
    "to": to,
    "type": "interactive",
    "interactive": {
        "type": "button",
        "body": {
        "text": message
        },
        "action": {
        "buttons": finalButtonsArray
        }
    }
    })
    headers = {
    'Content-Type': 'application/json',
    'apikey': API_KEY 
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)



import json
import requests

def send_whatsapp_carousel_template():
    """
    Sends a WhatsApp carousel template with product cards.
    """
    session_id = GlobalStateManager.get_session_details()
    to = session_id
    products = ["Luxury Cloud-Comfort Memory Foam Mattress", "Classic Harmony Spring Mattress", "EcoGreen Hybrid Latex Mattress","Plush Serenity Bamboo Mattress","UltraPlush Euro-Top Mattress"]

    # Ensure 'products' is a list and contains valid data
    if not isinstance(products, list) or len(products) < 1:
        print("Invalid product list provided.")
        return

    # Prepare product cards
    allCards = []
    for i, product in enumerate(products):
        # Extract product data safely
        product = fetch_product_by_name(product)
        product_name = product.get('name', 'Luxery comfort')
        product_description = product.get('description', '')[:100]  # Truncate if necessary
        product_image = product.get('image_url', 'https://m.media-amazon.com/images/I/71SGVQVjGoL._SX569_.jpg')
        product_url = product.get('buy_url', 'Sleepwell-Impressions-Mattress-Airvent-Technology/dp/B0CJM7H24F/ref=sr_1_1_sspa?crid=3IHMV8HTUPBLA&dib=eyJ2IjoiMSJ9.f23zWd-SuioNBmSvmdkSMr9jwwOpINKK1pRa0GBUOQlz13JRnIScH5EGQPx5OmjYI_2IsFjAkssZfbOyaldZFHX3h3DaRUSit782d9gIDlHt5l89hmn7gVGB0yc0eCodgwBD1LvOuOQgyWkDrLfBI09dz80CgtgiJvJCyE-e5qLhjw_lKNZomUIvTHbVhXMu1ZUlMw4I9TImLEyHdkZphzks0Ot29DJvGGKoC24VvTWPxQfP76HSMonxX2MjY2ZskjP_MZXJynUeNczF1dv1jIwswbAnJlBF1trz6UTWW4E.adbOqU8YnPyn11AYyO2BKg-yYjA1Po9CTC_fbeZuYIs&dib_tag=se&keywords=Luxury%2BCloud-Comfort%2BMemory%2BFoam%2BMattress&qid=1729328597&sprefix=luxury%2Bcloud-comfort%2Bmemory%2Bfoam%2Bmattress%2Caps%2C220&sr=8-1-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&th=1')

        # Build product card structure for WhatsApp
        productCard = {
            "card_index": i,
            "components": [
                {
                    "type": "header",  # lowercase
                    "parameters": [
                        {
                            "type": "image",  # lowercase
                            "image": {
                                "link": product_image  # Image link
                            }
                        }
                    ]
                },
                {
                    "type": "body",  # lowercase
                    "parameters": [
                        {
                            "type": "text",
                            "text": f"{product_name}"
                        }
                    ]
                },
                {
                    "type": "button",  # lowercase
                    "sub_type": "url",  # lowercase
                    "index": "0",
                    "parameters": [
                        {
                            "type": "text",
                            "text": f"View {product_url}"  # Product handle
                        }
                    ]
                },
                {
                    "type": "button",  # lowercase
                    "sub_type": "quick_reply",  # lowercase
                    "index": "1",
                    "parameters": [
                        {
                            "type": "payload",
                            "payload": "add to cart"  # Payload for adding to cart
                        }
                    ]
                }
            ]
        }
        allCards.append(productCard)

    # Construct the payload
    payload = json.dumps({
        "messaging_product": "whatsapp",
        "recipient_type": "individual",  # lowercase
        "to": to,
        "type": "template",
        "template": {
            "name": "product_carousel_dynamic",
            "language": {
                "code": "en"
            },
            "components": [
                {
                    "type": "body",  # lowercase
                    "parameters": [
                        {
                            "type": "text",
                            "text": "Check out our products"
                        }
                    ]
                },
                {
                    "type": "carousel",  # lowercase
                    "cards": allCards
                }
            ]
        }
    })

    # Set headers
    headers = {
        'apikey': API_KEY,  # Assuming API_KEY is defined globally
        'Content-Type': 'application/json'
    }

    # Make the API request
    response = requests.post(f"https://partnersv1.pinbot.ai/v3/{PHONE_NUMBER_ID}/messages", headers=headers, data=payload)

    if response.status_code == 200:
        print("Message sent successfully")
    else:
        print(f"Failed to send message. Status code: {response.status_code}")



def send_whatsapp_ask_user_location(): 

    session_id = GlobalStateManager.get_session_details()
    to = session_id

    payload = json.dumps({
    "messaging_product": "whatsapp",
    "recipient_type": "individual",
    "type": "interactive",
    "to": to,
    "interactive": {
        "type": "location_request_message",
        "body": {
        "text": "Hey share me your location to deliever the product to your address."
        },
        "action": {
        "name": "send_location"
        }
    }
    })
    headers = {
    'apikey': API_KEY,
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    if(response.status_code == 200) : 
        print("Message sent successfully")
        return "Message sent successfully"
    
    else: 
        print(f"Failed to send message. Status code: {response.status_code}")
        return f"Failed to send message. Status code: {response.status_code}"




def send_product_image_template(product_name, product_description, product_image_url, buy_url):
    session_id = GlobalStateManager.get_session_details()

    payload = json.dumps({
    "to": session_id,
    "type": "template",
    "template": {
        "language": {
        "code": "en"
        },
        "name": "product_image_sales",
        "components": [
        {
            "type": "header",
            "parameters": [
                {
                    "type": "image",
                    "image": {
                    "link": product_image_url
                    }
                }
            ]
        },
        {
            "type": "body",
            "parameters": [
                {
                    "type": "text",
                    "text": product_name 
                }
            ]
        },
        {
            "type": "button",
            "sub_type": "url",
            "index": "2",
            "parameters": [
                {
                    "type": "payload",
                    "payload": buy_url
                }
            ]
        }
        ]
    },
    "messaging_product": "whatsapp"
    })
    headers = {
    'apikey': API_KEY,
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    if(response.status_code == 200) : 
        print("Message sent successfully")
        return 200
        # return ("Image of the product send succesfull to the user")
    else:
        print(f"Failed to send message. Status code: {response}")
        return 400


import requests
import json

PHONE_NUMBER_ID = "428728346998136"
API_KEY = "05c3febb-8bd0-11ef-bb5a-02c8a5e042bd"

def send_whatsapp_template(template_type):
    url = f"https://partnersV1.pinbot.ai/v3/{PHONE_NUMBER_ID}/messages"
    session_id = GlobalStateManager.get_session_details()
    template_data = {
        "winner": {
            "name": "winner_flow_final",
            "flow_token": "1343602839951623"
        },
        "contact": {
            "name": "contact_flow_v1",
            "flow_token": "3209030375951785"
        },
        "subscription": {
            "name": "subscription_flow_v1",
            "flow_token": "1083160976778834"
        }
    }

    if template_type not in template_data:
        raise ValueError("Invalid template type. Choose 'winner', 'contact', or 'subscription'.")

    payload = json.dumps({
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": session_id,
        "type": "template",
        "template": {
            "name": template_data[template_type]["name"],
            "language": {
                "code": "en_US"
            },
            "components": [
                {
                    "type": "button",
                    "sub_type": "flow",
                    "index": "0",
                    "parameters": [
                        {
                            "type": "action",
                            "action": {
                                "flow_token": template_data[template_type]["flow_token"]
                            }
                        }
                    ]
                }
            ]
        }
    })

    headers = {
        'apikey': API_KEY,
        'Content-Type': 'application/json'
    }

    response = requests.post(url, headers=headers, data=payload)
    return response.text

# # Example usage
# if __name__ == "__main__":
#     recipient_number = "918855886289"
    
#     # print("Winner flow response:")
#     # print(send_whatsapp_template("winner", recipient_number))
    
#     # print("\nContact flow response:")
#     # print(send_whatsapp_template("contact", recipient_number))
    
#     print("\nSubscription flow response:")
#     print(send_whatsapp_template("subscription", recipient_number))





# if __name__ == "__main__":
#     send_whatsapp_text_message("Hello, this is a test message sent using PinBot API")
#     send_memory_consent("would you like me to save your preference for future referneces")

# send_product_image_template(session="918421250272",product_name="Luxury Cloud-Comfort Memory Foam Mattress Sleepwell-Impressions-Mattress-Airvent",product_description="",product_image_url="https://m.media-amazon.com/images/I/615ElisimfL._SX569_.jpg", buy_url="Sleepwell-Impressions-Mattress-Airvent-Technology/dp/B0CJM7H24F/ref=sr_1_1_sspa?crid=3IHMV8HTUPBLA&dib=eyJ2IjoiMSJ9.f23zWd-SuioNBmSvmdkSMr9jwwOpINKK1pRa0GBUOQlz13JRnIScH5EGQPx5OmjYI_2IsFjAkssZfbOyaldZFHX3h3DaRUSit782d9gIDlHt5l89hmn7gVGB0yc0eCodgwBD1LvOuOQgyWkDrLfBI09dz80CgtgiJvJCyE-e5qLhjw_lKNZomUIvTHbVhXMu1ZUlMw4I9TImLEyHdkZphzks0Ot29DJvGGKoC24VvTWPxQfP76HSMonxX2MjY2ZskjP_MZXJynUeNczF1dv1jIwswbAnJlBF1trz6UTWW4E.adbOqU8YnPyn11AYyO2BKg-yYjA1Po9CTC_fbeZuYIs&dib_tag=se&keywords=Luxury%2BCloud-Comfort%2BMemory%2BFoam%2BMattress&qid=1729328597&sprefix=luxury%2Bcloud-comfort%2Bmemory%2Bfoam%2Bmattress%2Caps%2C220&sr=8-1-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&th=1") 
# 

# product_list = ["Luxury Cloud-Comfort Memory Foam Mattress", "Classic Harmony Spring Mattress", "EcoGreen Hybrid Latex Mattress","Plush Serenity Bamboo Mattress","UltraPlush Euro-Top Mattress"]

# send_whatsapp_carousel_template(products=product_list)

# # if __name__ == "_main_":
# # send_whatsapp_carousel_template(dummy_products)

