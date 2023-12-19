import tiktoken
import os
import streamlit as st
from streamlit_chat import message
from langchain import OpenAI
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import (ConversationBufferMemory, ConversationSummaryMemory,ConversationBufferWindowMemory)
from langchain.memory import ConversationTokenBufferMemory

# Store a single conversation session
if 'conversation' not in st.session_state:
    st.session_state['conversation'] = None

# Store messages in a conversation session
if 'messages' not in st.session_state:
    st.session_state['messages'] = []

# Store api_key in session
if 'API_Key' not in st.session_state:
    st.session_state['API_Key'] = ''

#Setting page title and header
st.set_page_config(page_title="Chat GTP Clone", page_icon="robot_face:")
st.markdown("<h1 style='text-align: center;'> How can I assist you? </h1>", unsafe_allow_html=True)

# Setting side bar
st.sidebar.title('😎')
st.session_state['API_Key'] = st.sidebar.text_input("What's your API key?", type="password")

summarise_button = st.sidebar.button('Summarise the conversation', key='summarise')
if summarise_button:
    summarise_placeholder = st.sidebar.write("Nice chatting with you my friend ❤️ :\n\n" + "Hello Friend")

# Get response 
def getResponse(userInput, api_key):
    # Only initialise once if it's a new conversation.
    if  st.session_state['conversation'] is None:
        llm = OpenAI(temperature=0, openai_api_key=api_key, model_name='gpt-3.5-turbo-instruct')
        st.session_state['conversation'] = ConversationChain(llm=llm, verbose=True, memory=ConversationBufferMemory())

    response = st.session_state['conversation'].predict(input=userInput)
    print(st.session_state['conversation'].memory.buffer)

    return response

response_container = st.container()
container = st.container()

# Input & submit conversation on
with container:
    with st.form(key='my_form', clear_on_submit=True):
        user_input = st.text_area("Your question goes here:", key='input', height=100)
        submit_button = st.form_submit_button(label="Send")
        if submit_button:
            st.session_state['messages'].append(user_input)
            model_reponse = getResponse(user_input, st.session_state['API_Key'])
            st.session_state['messages'].append(model_reponse)

            with response_container:
                for i in range(len(st.session_state['messages'])):
                    if(i % 2) == 0:
                        message(st.session_state['messages'][i], is_user=True, key=str(i) + '_user')
                    else:
                        message(st.session_state['messages'][i], key=str(i) + '_AI')

