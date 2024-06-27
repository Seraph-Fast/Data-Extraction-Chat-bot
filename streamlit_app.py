import streamlit as st
from streamlit_option_menu import option_menu
from Components import chatbot_page, report_generation_page
from Components import model


st.set_page_config(layout="wide")
if 'knowledge_model' not in st.session_state:
    st.session_state.knowledge_model = model.run_chatbot()

knowledge_model = st.session_state.knowledge_model


with st.sidebar:
    selected = option_menu("", ["Chatbot"],
                           icons=['chat', 'file-earmark-text'],
                           menu_icon="cast", default_index=0)

if selected == "Chatbot":
    chatbot_page.show_chatbot_page(knowledge_model)