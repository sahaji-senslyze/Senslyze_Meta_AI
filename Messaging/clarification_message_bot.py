# from typing import TypedDict, Annotated
# import os
# import requests
# from typing import Annotated,List,Optional
# from typing_extensions import TypedDict
# from langchain.schema import SystemMessage, HumanMessage, AIMessage
# from langchain.llms.base import BaseLLM
# from langgraph.graph import StateGraph, END, START
# from langgraph.graph.message import add_messages
# from langchain_core.messages import BaseMessage
# from langgraph.prebuilt import ToolNode, tools_condition
# from langchain_groq import ChatGroq
# from pydantic import BaseModel, Field
# from langchain.tools import BaseTool, StructuredTool, tool
# from langgraph.checkpoint.memory import MemorySaver
# from Store.userinfo import get_userinfo
# from StateManager.GlobalState import GlobalStateManager, graph_builder, State, get_chat_history
# from Prompt.SystemPrompts import Masterbot_prompt,clarification_prompt,classification_prompt,template_prompt
# from Tools.search_tool import websearch_tool
# from Tublu.tublu_functions import send_message_to_tubulu_text, send_message_to_tubulu_button, send_message_to_tubulu_form
# from dotenv import load_dotenv
# from langgraph.checkpoint.memory import MemorySaver
# from Store.userinfo import get_userinfo


# load_dotenv(dotenv_path='.env.local')

# groq_api_key = os.getenv('GROQ_API_KEY')

# llm=ChatGroq(groq_api_key=groq_api_key,model_name="llama-3.1-70b-versatile")

# memory = MemorySaver()


# UserInfo = get_userinfo
# # Define State
# class State(TypedDict):
#     messages: Annotated[list, add_messages]

# # Initialize StateGraph
# graph_message_builder = StateGraph(State)

# # Define tools
# @tool
# def Text_message_tool(text: str) -> str:
#     """
#     Will take the message and display it to the user in plain text format.
#     """
#     session_id = GlobalStateManager.get_session_details()
#     tubulu_chatroom = UserInfo.get(session_id, {}).get('chatRoom')
#     send_message_to_tubulu_text(message=text,TUBULU_CHATROOM=tubulu_chatroom)
#     return "Message sent successfully"

# @tool
# def Button_message_tool(message: str, buttons_title: list[str]) -> str:
#     """
#     Will take the message and button titles as a list of strings and display them to the user.
#     """
#     session_id = GlobalStateManager.get_session_details()
#     tubulu_chatroom = UserInfo.get(session_id, {}).get('chatRoom')
#     send_message_to_tubulu_button(message, buttons_title, tubulu_chatroom)
#     return "Message sent successfully"

# @tool
# def Form_message_tool(message: str, form_title: str, form_attributes_title: list[str]) -> str:
#     """
#     Will take the message, form title, and form attributes title as a list and send the form to the user.
#     """
#     session_id = GlobalStateManager.get_session_details()
#     tubulu_chatroom = UserInfo.get(session_id, {}).get('chatRoom')
#     send_message_to_tubulu_form(message, form_title, form_attributes_title, tubulu_chatroom)
#     return "Message sent successfully"

# # Create the tool nodes for the graph
# tools_message = [Text_message_tool, Button_message_tool, Form_message_tool]
# llm_with_message_tools = llm.bind_tools(tools_message)

# # Clarification template bot
# def clarification_template_bot(state:State):
#     clarification_template = """
#     You are a template selection agent. You will get a response from the masterbot, which is responding to the user. Your task is to
#     pass that message in the proper template to the user.
#     You have these templates to choose from:
#     1. **TEXT**: Simple text response.
#     2. **FORM**
#     3. **BUTTONS**

#     Based on the template you selected, use the appropriate tool to send the message to the user.
#     Do not make any changes to the message provided by the masterbot. Only the masterbot can send you messages, not the user.
#     Important dont call tool multiple times only once if it returns message sent succesfully then stop
#     """

#     # Create system message
#     system_message = SystemMessage(content=clarification_template)

#     # Invoke LLM with the current state of messages, including the system message
#     response = llm_with_message_tools.invoke(state["messages"] + [system_message])

#     # Return the response
#     return {"messages": response}

# # Add nodes and edges to the graph
# graph_message_builder.add_node("clarification_template_bot", clarification_template_bot)

# # ToolNode containing the tools
# tool_node_message = ToolNode(tools=tools_message)
# graph_message_builder.add_node("tools", tool_node_message)

# # Add conditional edges between nodes
# graph_message_builder.add_conditional_edges(
#     "clarification_template_bot",
#     tools_condition
# )
# graph_message_builder.add_edge("tools", "clarification_template_bot")
# graph_message_builder.add_edge(START, "clarification_template_bot")

# # Compile the graph with a checkpointer
# graph_message = graph_message_builder.compile(checkpointer=memory)



# def clar_chat(session_id, masterbot_input):
#     config = {"configurable": {"thread_id": session_id}}
#     UserInfo = get_userinfo()
#     GlobalStateManager.set_session_details(session_id)
#     print(GlobalStateManager.get_session_details())
# # The config is the **second positional argument** to stream() or invoke()!
    
#     if masterbot_input:
#         events = graph_message.stream(
#               {"messages": [("ai", masterbot_input)]}, config, stream_mode="values"
#         )
#         for event in events:
#             event["messages"][-1].pretty_print()
#             final_result = event
#         return masterbot_input, final_result
#     else:
#         return "no input from user"
    

from typing import TypedDict, Annotated, List
import os
from langchain.schema import SystemMessage
from langgraph.graph import StateGraph, END, START
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_groq import ChatGroq
from langchain.tools import tool
from langgraph.checkpoint.memory import MemorySaver
from Store.userinfo import get_userinfo
from StateManager.GlobalState import GlobalStateManager
from dotenv import load_dotenv
from SalseAgent.product_info import fetch_product_by_name
from Whatsapp.whatsapp_message import send_whatsapp_text_message, send_memory_consent, send_button_message, send_product_image_template, send_whatsapp_ask_user_location, send_whatsapp_template

# Load environment variables
load_dotenv(dotenv_path='.env.local')

groq_api_key = os.getenv('GROQ_API_KEY')

# Initialize the ChatGroq model
llm = ChatGroq(groq_api_key=groq_api_key, model_name="llama-3.1-70b-versatile")

# Initialize memory saver
memory = MemorySaver()

# Define State TypedDict
class State(TypedDict):
    messages: Annotated[list, add_messages]

# Initialize StateGraph
graph_message_builder = StateGraph(State)

# Define tools
@tool
def Text_message_tool(text: str) -> str:
    """
    Will take the message and display it to the user in text format it could take emoji also.
    """
    # session_id = GlobalStateManager.get_session_details()
    # tubulu_chatroom = get_userinfo().get(session_id, {}).get('chatRoom')
    # send_message_to_tubulu_text(message=text, TUBULU_CHATROOM=tubulu_chatroom)
    send_whatsapp_text_message(message=text)
    return "Message sent successfully Don't send the message again"

@tool
def Button_message_tool(message: str, buttons_title: list[str]) -> str:
    """
    Will take the message and button titles as a list of strings and display them to the user.
    """
    # session_id = GlobalStateManager.get_session_details()
    # tubulu_chatroom = get_userinfo().get(session_id, {}).get('chatRoom')
    # send_message_to_tubulu_button(message, buttons_title, tubulu_chatroom)
    send_button_message(message, buttons_title)
    return "Message sent successfully Don't send any message again"

# @tool
# def Form_message_tool(message: str, form_title: str, form_attributes_title: list[str]) -> str:
#     """
#     Will take the message, form title, and form attributes title as a list and send the form to the user.
#     """
#     session_id = GlobalStateManager.get_session_details()
#     tubulu_chatroom = get_userinfo().get(session_id, {}).get('chatRoom')
#     send_message_to_tubulu_form(message, form_title, form_attributes_title, tubulu_chatroom)
#     return "Message sent successfully"
@tool
def location_get_tool(query:str)->str:
    """
    Only use when user wants to buy or purchase the product/srvices. use this to ask user about their location.
    """
    send_whatsapp_ask_user_location()
    return ("Message sent succesfull : asked user for the location Don't ask any other question")

@tool
def contact_us_form(query:str)-> str:
    """
    It sends user the contact us form where user can resolve any of its query if master bot is unable to resolve it.
    """
    send_whatsapp_template(template_type='contact')
    return("Contact Us form send to the user Kindly ask user to fill it in a polite manner")

@tool
def Image_message_tool(productname: str) ->str:
    """
    It will take the actual product name and display the Image of the product and discription and display it to the user. Don't send any message after sending image .
    """
    product = fetch_product_by_name(productname)

# Check if product is found (it might return a "No similar product" message otherwise)
    if isinstance(product, dict):  # Ensure 'product' is a dictionary and not an error message
       product_name = product.get('name')
       product_description = product.get('description')
       product_image = product.get('image_url')
       product_buy = product.get('buy_url')
       print(product_image,product_name, product_buy)
       
       send_product_image_template(product_name=product_name, product_description=product_description, product_image_url=product_image, buy_url=product_buy)
       return "Message sent succesfull "


# Create the tool nodes for the graph
tools_message = [Text_message_tool,Button_message_tool, location_get_tool, contact_us_form]
llm_with_message_tools = llm.bind_tools(tools_message)

# Clarification template bot
def clarification_template_bot(state: State):
    clarification_template = """
    You are a template selection agent. You will get a response from the masterbot, which is responding to the user. Your task is to
    pass that message in the proper template to the user.
    You Will also get the user query so based on user query intent and master bot response use the proper template tool to send message to the user.
    You have these templates to choose from:
    1. **TEXT**: Simple text response.
    3. **BUTTONS**: To show quick actions and categories and etc.


    **Also conserve the emoji's that are passed by the masterbot pass the emojes also to the tools to send the message** and also try to use the buttons more times.
    Based on the template you selected,  use the appropriate tool to send the message to the user.
    Do not make any changes to the message provided by the masterbot. Only the masterbot can send you messages, not the user.
    You can send emoji's also in the message to the tools to make user experience more better.
    Important: don't call the tool multiple times; only call once if it returns "Message sent successfully", then stop.
    **Most Important** Don't remove the emoji and also dont change the message recived from master bot just pass it to the tool as it is.
    Note: Dont send multiple messages repatedly. Only send once. Only use once the tool to send message to user.
    """

    # Create system message
    system_message = SystemMessage(content=clarification_template)
    
    # Invoke LLM with the current state of messages, including the system message
    response = llm_with_message_tools.invoke(state["messages"] + [system_message])

    # Return the response
    return {"messages": response}

# Add nodes and edges to the graph
graph_message_builder.add_node("clarification_template_bot", clarification_template_bot)
tool_node_message = ToolNode(tools=tools_message)
graph_message_builder.add_node("tools", tool_node_message)

# Add conditional edges between nodes
graph_message_builder.add_conditional_edges(
    "clarification_template_bot",
    tools_condition
)
graph_message_builder.add_edge("tools", "clarification_template_bot")
graph_message_builder.add_edge(START, "clarification_template_bot")

# Compile the graph with a checkpointer
graph_message = graph_message_builder.compile(checkpointer=memory)

# Function to handle chat session
def clar_chat(session_id, masterbot_input, user_query):
    config = {"configurable": {"thread_id": session_id}}
    GlobalStateManager.set_session_details(session_id)
    
    if masterbot_input:
        events = graph_message.stream(
            {"messages": [("user",user_query),("ai", masterbot_input)]}, config, stream_mode="values"
        )
        for event in events:
            event["messages"][-1].pretty_print()
            final_result = event
        return masterbot_input, final_result["messages"][-1].content
    else:
        return "no input from user"
