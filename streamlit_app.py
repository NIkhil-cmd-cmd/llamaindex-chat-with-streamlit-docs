import streamlit as st
import openai
from llama_index.llms.openai import OpenAI
from streamlit_option_menu import option_menu

try:
    from llama_index import VectorStoreIndex, ServiceContext, Document, SimpleDirectoryReader
except ImportError:
    from llama_index.core import VectorStoreIndex, ServiceContext, Document, SimpleDirectoryReader

# Initialize OpenAI API key
openai.api_key = st.secrets.openai_key

# Set page configuration
st.set_page_config(page_title="Share-On", page_icon="💬", layout="centered", initial_sidebar_state="auto", menu_items=None)

# Sidebar menu
with st.sidebar:
    selected = option_menu(
        "Menu",
        ["Home", "Chat", "Mental Health Resources", "Advocacy"],
        icons=["house", "chat", "book", "book"],
        menu_icon="cast",
        default_index=0,
    )

# Define pages
def home():
    st.title("Welcome to Share-On")
    st.info("From AI to advocacy, Share-On is a non-profit 501-3(C) organization dedicated to supporting teenage mental health with innovative software created by teens, for teens. The deterioration of students’ mental health is a highly overlooked, yet universal, issue caused by factors such as schoolwork, social life, and extracurricular activities. Share-On offers a platform for students to unwind and seek guidance. With our self-developed AI algorithm, users can input their current problems as “rants” into our platform, and receive an output with specialized resources and customized advice catered to their issues. Furthermore, our data collection helps us to identify common challenges among teens, enabling Share-On to work with the community to help find solutions. ", icon="📃")

def chat():
    st.title("Share what's on your mind with Share-On")
    if "messages" not in st.session_state.keys():  # Initialize the chat messages history
        st.session_state.messages = [
            {"role": "assistant", "content": "Hi! I'm here to provide you with mental health support. How can I assist you today?"}
        ]

    @st.cache_resource(show_spinner=False)
    def load_data():
        with st.spinner(text="Loading and indexing mental health resources – hang tight! This should take 1-2 minutes."):
            reader = SimpleDirectoryReader(input_dir="./data", recursive=True)
            docs = reader.load_data()
            service_context = ServiceContext.from_defaults(llm=OpenAI(model="gpt-3.5-turbo", temperature=0.5, system_prompt="You are a mental health assistant. Your job is to answer questions related to mental health, provide support, and offer factual information. Keep your answers supportive and based on facts – do not hallucinate features or give medical advice."))
            index = VectorStoreIndex.from_documents(docs, service_context=service_context)
            return index

    index = load_data()

    if "chat_engine" not in st.session_state.keys():  # Initialize the chat engine
        st.session_state.chat_engine = index.as_chat_engine(chat_mode="condense_question", verbose=True)

    if prompt := st.chat_input("Your question"):  # Prompt for user input and save to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

    for message in st.session_state.messages:  # Display the prior chat messages
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # If last message is not from assistant, generate a new response
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = st.session_state.chat_engine.chat(prompt)
                st.write(response.response)
                message = {"role": "assistant", "content": response.response}
                st.session_state.messages.append(message)  # Add response to message history

def Mental_Health_Resources():
    st.title("Mental Health Resources")
    st.info("Here you can find various resources related to mental health.")
    # Add your resource content here ("Call 911 if you or someone you know is in immediate danger or go to the nearest emergency room.



988 Suicide & Crisis Lifeline 

Call or text 988; Llame al 988 (para ayuda en español)
Use Lifeline Chat  on the web (English only)
The Lifeline provides 24-hour, confidential support to anyone in suicidal crisis or emotional distress. Call or text 988 to connect with a trained crisis counselor. 



Veterans Crisis Line 
Use Veterans Crisis Chat  on the web 
The Veterans Crisis Line is a free, confidential resource that connects veterans 24 hours a day, 7 days a week with a trained responder. The service is available to all veterans and those who support them, even if they are not registered with the VA or enrolled in VA healthcare.



Disaster Distress Helpline 
Call or text 1-800-985-5990
The disaster distress helpline provides immediate crisis counseling for people who are experiencing emotional distress related to any natural or human-caused disaster. The helpline is free, multilingual, confidential, and available 24 hours a day, 7 days a week.

View the 5 action steps for helping someone in emotional pain infographic to see how you can help those in distress.")

Source: https://www.nimh.nih.gov/health/find-help 



Nation sexual assault hotline

Call: 1-800-656-4673

For more visit: https://sakitta.org/survivors/



National Domestic Violence Hotline

Call: 800-799-7233 or text "START" to: 88788

​

Love is Respect – National Teen Dating Abuse Hotline

Hotline: 1 (866) 331 – 9474
Text: 22522
Available 24 hours a day, 7 days a week via phone, text, and online chat.

Love is Respect offers information, support, and advocacy to young people who have questions or concerns about their dating relationships.

​

StrongHearts Native Helpline

Hotline: 1 (844) 762 – 8483
Available Monday through Friday, 9:00am to 5:30pm CST via phone.

The StrongHearts Native Helpline is a safe, anonymous, and confidential service for Native Americans experiencing domestic violence and dating violence.

​

Pathways to Safety International

Hotline: 1 (833) 723 – 3833
Email: crisis@pathwaystosafety.org
Available 24 hours a day, 7 days a week via phone, email, and online chat.

Pathways to Safety International assists Americans experiencing interpersonal and gender based violence abroad.



Gay, Lesbian, Bisexual and Transgender National Hotline

Hotline: 1 (888) 843 – 4564
Youth Talkline: 1 (800) 246 – 7743
Senior Helpline: 1 (888) 234 – 7243
Email: help@LGBThotline.org
Hours vary, available via phone and online chat.

The LGBT National Help Center serves gay, lesbian, bisexual, transgender, and questioning people by providing free and confidential peer support and local resources.



Womens Law

Email hotline: https://hotline.womenslaw.org/

The WomensLaw online helpline provides basic legal information, referrals, and emotional support for victims of abuse.

​

For more visit: https://victimconnect.org/resources/national-hotlines/​

# Hide Streamlit style
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

def advocacy():
    st.title("Advocacy")
    st.info("At Share-On, we are dedicated to harnessing the power of user data to drive positive change. Through a careful and respectful approach, we utilize the insights gained from the stories shared within our organization to advocate for stronger mental health laws and bills. Our commitment to your privacy will always stand; every piece of information shared is treated with the utmost confidentiality. Your stories aren't just stories here; they're fuel for change. Our aim is to shape policies that truly help people dealing with mental health struggles.")
    # Add your resource content here

# Render selected page
if selected == "Home":
    home()
elif selected == "Chat":
    chat()
elif selected == "Resources":
    resources()
elif selected == "Advocacy":
    advocacy()

