import pandas as pd
import boto3
import json
from botocore.exceptions import ClientError
from PIL import Image
import io

# Load credentials from CSV
creds = pd.read_csv('./hackathon_accessKeys.csv')  # Update with your CSV path
access_key = creds['Access key ID'][0]
secret_key = creds['Secret access key'][0]

# Initialize a session using your credentials
session = boto3.Session(
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key,
)

# Create a Bedrock client
bedrock_runtime = session.client('bedrock-runtime', region_name="us-east-1")
MODEL_ID = "us.meta.llama3-2-90b-instruct-v1:0"
IMAGE_NAME = "./1.jpeg"

def resize_image(image_path, max_size=(1120, 1120)):
    ext = image_path.split('.')[-1]
    with Image.open(image_path) as img:
        img.thumbnail(max_size)
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format=ext)
        return img_byte_arr.getvalue()

def is_jpeg(image_path):
    return image_path.lower().endswith(('.jpg'))

try:
    if is_jpeg(IMAGE_NAME):
        # For JPEG images, we'll skip the image analysis and return an empty entity list
        response_text = json.dumps({"entities": [""]})
    else:
        # Resize the image if necessary
        image = resize_image(IMAGE_NAME)
        
        user_message = """You are a sales expert, for a shopify store. You are responsible for identifying what product the image provided contains and output an entity.:
        ## Steps
        1. Identify the product in the image.
        2. Output the entity array in the following format:
        {
            entities: [entity1, entity2, ...]
        }
        ## Example
        {
            entities: ['sweater', 'full shirt', 'red t-shirt']
        }
        
        Make sure the response is a formatted response in JSON format and does not contain any extra text or characters like ```json or anything.
        """

        ext = IMAGE_NAME.split('.')[-1]
        
        messages = [
            {
                "role": "user",
                "content": [
                    {"image": {"format": ext, "source": {"bytes": image}}},
                    {"text": user_message},
                ],
            }
        ]
        
        response = bedrock_runtime.converse(
            modelId=MODEL_ID,
            messages=messages,
        )
        
        if 'output' in response and 'message' in response['output'] and 'content' in response['output']['message']:
            response_text = response["output"]["message"]["content"][0]["text"]
        else:
            response_text = json.dumps({"entities": []})
    
    print("Model response:\n--------\n")
    print(response_text)
        
except Exception as e:
    print(f"An error occurred: {str(e)}")




url = f"https://partnersv1.pinbot.ai/v3/{PHONE_NUMBER_ID}/messages"

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