# Flask Webhook Route
from flask import Flask,request,jsonify
import requests
from langchain_groq import ChatGroq
from sales import sales_chat
from Store.userinfo import UserInfo,set_userinfo,get_userinfo
import os
from StateManager.GlobalState import GlobalStateManager
from sales import SalesGPT, llm
from SalseAgent.customize import config, conversation_stages
# import logging
# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger(__name__)

app = Flask(__name__)

sales_agent = SalesGPT.from_llm(llm, verbose=False, **config)    
# sales_agent.seed_agent()
@app.route("/", methods=["GET"])
def index(): 
    return "This is senslyze hacks!"


def reset(session_id):
    sales_agent.seed_agent(session_id)
    

@app.route("/health-check", methods=["GET"])
def health_check(): 
    return "OK"


@app.route('/chat', methods=['POST'])
def chat():
    # logger.info("Received chat request")
    data = request.get_json()
    print(data)
    # logger.debug("Request data: %s", data)

    # Extract relevant information from the new data structure
    entry = ""
    changes = ""
    value = ""
    message = ""
    contact = ""
    user_input = ""
    session_id = ""
    username = ""
    phone_number = ""

    try:
        entry = data['entry'][0]
        changes = entry['changes'][0]
        value = changes['value']
        message = value['messages'][0]
        contact = value['contacts'][0]
        session_id = message['from']
        user_input = message['text']['body'].strip()

        if(user_input == "/reset"):
            reset(session_id)

        
        username = contact['profile']['name']
        phone_number = value['metadata']['display_phone_number']

    except (KeyError, IndexError) as e:
        # logger.error(f"Error parsing incoming data: {e}")
        if(value) : 
            print("--------PRINT VALUE---------", message)
            if(message):
                try:
                    button = message["button"]
                    user_input = button['text']
                    payload = button['payload']
                    if(payload): 
                        user_input = payload 
                except:
                    interactive = message["interactive"]
                    if(interactive):
                        button_reply = interactive["button_reply"]["title"]
                        user_input = button_reply
            else: 
                statuses = value['statuses']
                if(statuses): 
                    return jsonify({ "error": "AI Response" }), 200
        # return jsonify({"error": "Invalid data format"}), 400

    GlobalStateManager.set_session_details(session_id)
    set_userinfo(session_id=session_id, chatRoom=phone_number, username=username)
    UserInfo = get_userinfo()
    # logger.debug("User info: %s", UserInfo)

    # Add message to database
    # message_id = db.add_message(session_id, user_input)

    # Get responses from all agents
    agent_responses = sales_chat(session_id, user_input, sales_agent)
    # logger.info("Chat responses: %s", agent_responses)

    # The agent_responses are already added to the database in the user_chat function

    return jsonify(agent_responses)
# Run the Flask app
if __name__ == '__main__':
    app.run(port=5000, debug=True)