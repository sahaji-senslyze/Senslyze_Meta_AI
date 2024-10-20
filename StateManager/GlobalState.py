from typing import Annotated,List,Optional
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, END, START

class State(TypedDict):
    messages: Annotated[list, add_messages]
    # agent_call_history: Annotated[list, add_messages]

graph_builder = StateGraph(State)

class GlobalStateManager:
    _global_state: Optional[State] = None
    _session_id: Optional[str] = None  # Should define a type for session_id

    @classmethod
    def set_global_state(cls, state: State):
        cls._global_state = state

    @classmethod
    def get_global_state(cls) -> State:
        if cls._global_state is None:
            raise ValueError("Global state is not initialized.")
        return cls._global_state
    @classmethod 
    def set_session_details(cls, session):
        cls._session_id = session

    @classmethod
    def get_session_details(cls) -> str:
        if cls._session_id is None:
            raise ValueError("Session id is not initialized.")
        return cls._session_id
        


def get_chat_history(state: State) -> str:
    messages = state['messages']
    num_messages = len(messages)

    if num_messages >= 5:
        chat_history = '\n'.join([m.content for m in messages[-5:]])
    else:
        chat_history = '\n'.join([m.content for m in messages])

    return chat_history