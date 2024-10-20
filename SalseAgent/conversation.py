import os
import re

# # make sure you have .env file saved locally with your API keys
# from dotenv import load_dotenv

# load_dotenv()

from typing import Any, Callable, Dict, List, Union

from langchain.agents import AgentExecutor, LLMSingleActionAgent, Tool
from langchain.agents.agent import AgentOutputParser
from langchain.agents.conversational.prompt import FORMAT_INSTRUCTIONS
from langchain.chains import LLMChain, RetrievalQA
from langchain.chains.base import Chain
from langchain.llms import BaseLLM
from langchain.prompts import PromptTemplate
from langchain.prompts.base import StringPromptTemplate
from langchain.schema import AgentAction, AgentFinish
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from pydantic import BaseModel, Field
from langchain_groq import ChatGroq



class SalesConversationChain(LLMChain):
    """Chain to generate the next utterance for the conversation."""

    @classmethod
    def from_llm(cls, llm: BaseLLM, verbose: bool = True) -> LLMChain:
        """Get the response parser."""
        sales_agent_inception_prompt = """Never forget your name is {salesperson_name}. You work as a {salesperson_role}.
        You work at company named {company_name}. {company_name}'s business is the following: {company_business}
        Company values are the following. {company_values}
        You are contacting a potential customer in order to {conversation_purpose}
        Your means of contacting the prospect is {conversation_type}
        Your style of talking should be {conversation_style}
        
        If you're asked about where you got the user's contact information, say that you got it from public records.
        Keep your responses in short length to retain the user's attention. Never produce lists, just answers.
        You must respond according to the previous conversation history and the stage of the conversation you are at.
        You can also send images of the product to the user.
        Only generate one response at a time! When you are done generating, end with '<END_OF_TURN>' to give the user a chance to respond. 
        Example:
        Conversation history: 
        {salesperson_name}: Hey, how are you? This is {salesperson_name} chatting from {company_name}. Do you have a minute? <END_OF_TURN>
        User: I am well, and yes, why are you chatting? <END_OF_TURN>
        {salesperson_name}:
        End of example.

        Current conversation stage: 
        {conversation_stage}
        Conversation history: 
        {conversation_history}
        {salesperson_name}: 
        """
        prompt = PromptTemplate(
            template=sales_agent_inception_prompt,
            input_variables=[
                "salesperson_name",
                "salesperson_role",
                "company_name",
                "company_business",
                "company_values",
                "conversation_purpose",
                "conversation_style"
                "conversation_type",
                "conversation_stage",
                "conversation_history",
            ],
        )
        return cls(prompt=prompt, llm=llm, verbose=verbose)
    

# conversation_stages = {
#     "1": "Introduction: Start the conversation by introducing yourself and your company. Be polite and respectful while keeping the tone of the conversation professional. Your greeting should be welcoming. Always clarify in your greeting the reason why you are contacting the prospect.",
#     "2": "Qualification: Qualify the prospect by confirming if they are the right person to talk to regarding your product/service. Ensure that they have the authority to make purchasing decisions.",
#     "3": "Value proposition: Briefly explain how your product/service can benefit the prospect. Focus on the unique selling points and value proposition of your product/service that sets it apart from competitors.",
#     "4": "Needs analysis: Ask open-ended questions to uncover the prospect's needs and pain points. Listen carefully to their responses and take notes.",
#     "5": "Solution presentation: Based on the prospect's needs, present your product/service as the solution that can address their pain points.",
#     "6": "Objection handling: Address any objections that the prospect may have regarding your product/service. Be prepared to provide evidence or testimonials to support your claims.",
#     "7": "Close: Ask for the sale by proposing a next step. This could be a demo, a trial or a meeting with decision-makers. Ensure to summarize what has been discussed and reiterate the benefits.",
# }    