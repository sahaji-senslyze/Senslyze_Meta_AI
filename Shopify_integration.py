import os
import json
import requests
from typing import Annotated, List, Optional, TypedDict
from langchain.schema import SystemMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, END, START
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from langchain_groq import ChatGroq
from langchain.tools import tool
from langgraph.prebuilt import ToolNode, tools_condition
from dotenv import load_dotenv
from Store.userinfo import get_userinfo, set_userinfo
from StateManager.GlobalState import GlobalStateManager, State, get_chat_history

# Load environment variables
load_dotenv(dotenv_path='.env.local')

# Shopify API setup
SHOP_NAME = os.getenv('SHOPIFY_SHOP_NAME')
ACCESS_TOKEN = os.getenv('SHOPIFY_ACCESS_TOKEN')
API_VERSION = '2024-04'
BASE_URL = f"https://{SHOP_NAME}.myshopify.com/admin/api/{API_VERSION}"

# Groq LLM setup
groq_api_key = os.getenv('GROQ_API_KEY')
llm = ChatGroq(groq_api_key=groq_api_key, model_name="llama-3.1-70b-versatile")

# Initialize memory saver and StateGraph
memory = MemorySaver()
graph_builder = StateGraph(State)

# Debug mode
DEBUG = False

def debug_print(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)

# Shopify API functions
def make_shopify_api_request(endpoint):
    headers = {"X-Shopify-Access-Token": ACCESS_TOKEN}
    response = requests.get(f"{BASE_URL}/{endpoint}", headers=headers)
    return response.json()

def fetch_shopify_data(data_type: str, limit: int = 5) -> dict:
    """Fetch data from Shopify store based on the data type"""
    if data_type == "products":
        response = make_shopify_api_request(f"products.json?limit={limit}")
        return {"products": response.get("products", [])[:limit]}
    elif data_type == "collections":
        return make_shopify_api_request(f"custom_collections.json?limit={limit}")
    elif data_type == "orders":
        return make_shopify_api_request(f"orders.json?limit={limit}")
    elif data_type == "customers":
        return make_shopify_api_request(f"customers.json?limit={limit}")
    else:
        return {"error": "Invalid data type"}

def get_gemini_response(query):
    prompt = f"""
    You are an AI assistant for a Shopify store. Analyze the following user query and determine the appropriate action:

    User Query: "{query}"

    If the query is asking for specific Shopify data (products, collections, orders, or customers), return a JSON object with the following structure:
    {{
        "action": "fetch_data",
        "data_type": "products|collections|orders|customers"
    }}

    If the query is a general question or doesn't require fetching Shopify data, return a JSON object with the following structure:
    {{
        "action": "chat_response",
        "response": "Your helpful response here"
    }}

    Ensure your entire response is a valid JSON object. Don't add any extra strings or characters.

     MAKE SURE THE RESPONSE IS A VALID JSON OBJECT, IT IS VERY IMPORTANT TO KEEP IT JSON. IF YOU GIVE A JSON OBJECT
    THEN YOU WILL GET A CHOCOLATE FOR BEING A GOOD AI ASSISTANT OTHERWISE YOU WILL FACE PUNISHMENT.
    """
    return json.loads(response.text)

@tool
def classification_agent_tool(user_query: str, state: Optional[State] = None) -> str:
    """Classification agent to understand user intent"""
    state = GlobalStateManager.get_global_state()
    chat_history = get_chat_history(state)
    combined_message = f"System: {classification_prompt}\n\nChat History: {chat_history}\n\nuser query: {user_query}"
    response = llm.invoke([SystemMessage(content=combined_message)])
    debug_print(f"Classification output: {response.content}")
    return response.content

@tool
def clarification_agent_tool(classification_response: str, user_query: str, state: Optional[State] = None) -> str:
    """Clarification agent to gather additional information"""
    state = GlobalStateManager.get_global_state()
    chat_history = get_chat_history(state)
    combined_message = f"System: {clarification_prompt}\n\nChat History: {chat_history}\n\nClassification Agent Response:{classification_response}\n\nuser query: {user_query}\n\n"
    response = llm.invoke([SystemMessage(content=combined_message)])
    debug_print(f"Clarification output: {response.content}")
    return response.content

@tool
def templateselection_agent_tool(user_query: str, classification_output: str, clarification_output: str, state: Optional[State] = None) -> str:
    """Template Selection agent to determine response format"""
    state = GlobalStateManager.get_global_state()
    chat_history = get_chat_history(state)
    combined_message = f"System: {template_prompt}\n\nclassification agent response: {classification_output}\n\nclarification agent response: {clarification_output}\n\nuser query: {user_query}"
    response = llm.invoke([SystemMessage(content=combined_message)])
    debug_print(f"Template selection output: {response.content}")
    return response.content

@tool
def datamodeling_agent_tool(user_query: str, product_specifications: str, template_selected: str, state: Optional[State] = None) -> str:
    """Data modeling tool to process Shopify data and generate a response"""
    debug_print(f"Datamodeling input - Query: {user_query}, Specs: {product_specifications}, Template: {template_selected}")
    
    gemini_response = get_gemini_response(user_query)
    debug_print(f"Gemini response: {gemini_response}")
    
    if gemini_response['action'] == 'fetch_data':
        shopify_data = fetch_shopify_data(gemini_response['data_type'], limit=5)
        debug_print(f"Fetched Shopify data: {shopify_data}")
        
        processed_data = process_shopify_data(shopify_data, template_selected)
        debug_print(f"Processed data: {processed_data}")
        
        # TODO: PREPARE A DATA TO SEND TO MASTER BOT
        temp_data = ""
        # Get the chatroom for the current session
        session_id = GlobalStateManager.get_session_details()
        chatroom = get_userinfo().get(session_id, {}).get('chatRoom')
        
        # Directly send the message based on the template
        if template_selected == "CAROUSEL":
            send_message_to_tubulu_carousel(
                message="Here are some products for you:",
                items=processed_data,
                TUBULU_CHATROOM=chatroom
            )
            return "Carousel data sent directly to Tubulu."
        elif template_selected == "BUTTONS":
            button_titles = [item.get("title", "") for item in processed_data]
            send_message_to_tubulu_button(
                message="Here are some options:",
                buttons_title=button_titles,
                TUBULU_CHATROOM=chatroom
            )
            return "Button data sent directly to Tubulu."
        elif template_selected == "FORM":
            form_title = "Product Information"
            form_attributes = processed_data.get("form_attributes", [])
            send_message_to_tubulu_form(
                message="Please provide the following information:",
                form_title=form_title,
                form_attributes_title=form_attributes,
                TUBULU_CHATROOM=chatroom
            )
            return "Form data sent directly to Tubulu."
        else:
            # For TEXT template or any other, return the data to be processed by the main flow
            return json.dumps({"template": template_selected, "data": processed_data, "message": "A list of proudcts has been sent."})
    else:
        return json.dumps({"template": "TEXT", "data": gemini_response['response']})



def process_shopify_data(data, template):
    if template == "CAROUSEL":
        return [
            {
                "url": f"/products/{item['handle']}",
                "actionText": f"View {item['title']}",
                "image": item["image"]["src"] if item.get("image") else "",
                "title": item["title"],
                "description": item.get("body_html", "")[:100] + "..." if item.get("body_html") else ""
            } 
            for item in data.get("products", [])[:5]
        ]
    elif template == "BUTTONS":
        return [{"title": item["title"]} for item in data.get("products", [])[:5]]
    elif template == "FORM":
        return {"form_attributes": ["Name", "Email", "Product Interest"]}
    else:
        return str(data)  # Default to string representation for TEXT template

def Masterbot(state: State):
    GlobalStateManager.set_global_state(state)
    state["messages"].insert(0, SystemMessage(content=Masterbot_prompt))
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

# Set up tool nodes and graph
tools = [classification_agent_tool, clarification_agent_tool, templateselection_agent_tool, datamodeling_agent_tool]
llm_with_tools = llm.bind_tools(tools)

graph_builder.add_node("Masterbot", Masterbot)
graph_builder.add_node("tools", ToolNode(tools=tools))
graph_builder.add_conditional_edges("Masterbot", tools_condition)
graph_builder.add_edge("tools", "Masterbot")
graph_builder.add_edge(START, "Masterbot")

graph = graph_builder.compile(checkpointer=memory)

def shopify_integrated_chat(session_id, user_input):
    config = {"configurable": {"thread_id": session_id}}
    GlobalStateManager.set_session_details(session_id)
    UserInfo = get_userinfo()
    
    debug_print(f"Processing input for session {session_id}: {user_input}")
    
    if user_input:
        events = graph.stream({"messages": [HumanMessage(content=user_input)]}, config, stream_mode="values")
        
        for event in events:
            debug_print("Event:", event)
            event["messages"][-1].pretty_print()
            final_result = event

        debug_print("Final result:", final_result)
        processed_result = process_final_result(final_result, UserInfo.get(session_id, {}).get('chatRoom'))
        return processed_result
    else:
        return "No input from user"

def process_final_result(result, chatroom):
    content = result["messages"][-1].content
    debug_print(f"Processing final result: {content}")
    
    print("-----------------------_*_-------------------------")
    print(f"Raw content: {content}")

    # Check if the content is a direct message indicating the data was sent to Tubulu
    if "sent directly to Tubulu" in content:
        return content  # This message comes from datamodeling_agent_tool

    try:
        # Try to parse the entire content as JSON
        data = json.loads(content)
        template = data.get("template", "TEXT")
        message_data = data.get("data", "")
    except json.JSONDecodeError:
        # If parsing fails, treat as TEXT
        template = "TEXT"
        message_data = content

    print(f"Template: {template}, Data: {message_data}")

    # Handle TEXT template (other templates are handled in datamodeling_agent_tool)
    if template == "TEXT":
        send_message_to_tubulu_text(message=str(message_data), TUBULU_CHATROOM=chatroom)
    
    return f"Message processed using {template} template"

if __name__ == "__main__":
    session_id = "1"
    set_userinfo(session_id=session_id, chatRoom=os.getenv("TUBULU_CHAT_ROOM"), username="John")
    
    while True:
        user_input = input("User: ")
        if user_input.lower() == 'exit':
            break
        response = shopify_integrated_chat(session_id, user_input)
        print("Assistant:", response)