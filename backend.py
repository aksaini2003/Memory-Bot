#here we are going to write the backend code for our chatbot and we will use it in the frontend 

#importing all necessary libraries 

from langgraph.graph import StateGraph ,START,END 

from langchain_groq import ChatGroq
from dotenv import load_dotenv 
load_dotenv() 
from typing import TypedDict,Annotated 
from langchain_core.messages import HumanMessage,BaseMessage

from langgraph.checkpoint.memory import MemorySaver  

llm=ChatGroq(model='Llama-3.3-70b-Versatile') 

from langgraph.graph.message import add_messages
#here BaseMessage is abstract it can be any kind of message human,system,ai,etc 
# add_messages is a reducer by which we append the messages 

class ChatState(TypedDict):

    messages: Annotated[list[BaseMessage], add_messages]


#lets make a obejct for the persistence memory 
checkpointer=MemorySaver() 

#lets make our graph 
graph=StateGraph(ChatState) 


#logic for the chatting 
def Chat_with_LLM(state: ChatState)-> ChatState: 
    response=llm.invoke(state['messages']) 
    return {'messages':[response]}


#lets add node thier is only 1 node in it 
#by which user can communicate with the llm 
graph.add_node('Chat_Node',Chat_with_LLM) 




#lets add edges 
graph.add_edge(START,'Chat_Node') 
graph.add_edge('Chat_Node',END)


chat_bot=graph.compile(checkpointer=checkpointer) 

#now the above code is the part of the backend and we have to use it in the frontend 
