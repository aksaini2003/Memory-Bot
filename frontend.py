import streamlit as st 
from langchain_core.messages import HumanMessage 


from backend import chat_bot
# with st.chat_message('user'):
#     st.text('Hello') 
# with st.chat_message('assistant'):
#     st.text('How can I help you?') 
# with st.chat_message('user'):
#     st.text('My name is Aashish') 
# with st.chat_message('assistant'):
#     st.text('Nice to meet you, Aashish!')
    
    
# #lets see how to take input 
# user_input=st.chat_input('Type here') 
# if user_input: 
#     with st.chat_message('user'): 
#         st.text(user_input)
    
#lets try to make a dummy chatbot that will return the given input as output 
# user_input=st.chat_input('Type here') 
# if user_input:
#     with st.chat_message('user'):
#         st.text(user_input) 
        
#     with st.chat_message('assistant'): 
#         st.text(user_input)
#here it is overwriting the messages every time we send a new message 



# 3lets see how to solve this problem 
#we have to maintain the history of the messages 


#lets load the messages from the history 
#NOTE:- AS WE KNOW THAT THE CODE OF STREAMLIT IS EXECUTED EVERY TIME WHEN USER DONE ANY ACTION 
#SO THIS HISTORY WILL BE LOST EVERY TIME 
#LETS SOLVE THIS PROBLEM BY USING SESSION STATE
import streamlit.components.v1 as components

# Inject HTML and CSS for sticky header
components.html("""
    <div style="position: fixed; top: 0; left: 0; width: 100%; 
                background-color: #ffffff; padding: 15px; 
                font-size: 28px; font-weight: bold; 
                text-align: center; z-index: 999; 
                border-bottom: 1px solid #ddd;">
        🤖 Chatbot with Memory
    </div>
    <div style="margin-top: 80px;">
""", height=100)

# Add spacer to avoid overlap
st.markdown("<br><br><br><br>", unsafe_allow_html=True)
try:
    if 'history_msg' not in st.session_state: 
        st.session_state['history_msg']=[]

    for msg in st.session_state['history_msg']: 
        with st.chat_message(msg['role']): 
            st.text(msg['content']) 
        
    user_input=st.chat_input('Type here') 
    if user_input: 
        st.session_state['history_msg'].append({'role':'user','content':user_input})
        with st.chat_message('user'): 
            st.text(user_input) 
            
            
        #we have to make changes in this part of code to add the actual ai response 
        
        config={'configurable':{'thread_id':'11'}}
        
        with st.chat_message('assistant'):
            ai_response=chat_bot.invoke({'messages':HumanMessage(content=user_input)},config=config)
            output_message=ai_response['messages'][-1].content 
            st.text(output_message)
        st.session_state['history_msg'].append({'role':'assistant','content':output_message})
except Exception as e: 
    st.error('Due to high traffic, the server is currently down. Please try again Later.') 
    