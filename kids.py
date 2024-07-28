from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import streamlit as st

# Custom CSS for styling with a background image
st.markdown("""
    <style>
    .main {
        background-image: url('https://images.pexels.com/photos/1612351/pexels-photo-1612351.jpeg?auto=compress&cs=tinysrgb&w=600');
        background-size: cover;
        background-position: center;
        padding: 20px;
        padding: 20px;
    }
    .title {
        color: #ffffff;
        font-family: 'Comic Sans MS', cursive, sans-serif;
        text-shadow: 2px 2px 4px #000000;
    }
    .header {
        color: #f0e68c;
    }
    .text-input, .text-area {
        border-radius: 10px;
        border: 2px solid #ffffff;
        background-color: rgba(255, 255, 255, 0.8);
    }
    .stButton button {
        background-color: #4CAF50;
        color: white;
        border-radius: 12px;
        padding: 10px 24px;
    }
    </style>
    """, unsafe_allow_html=True)

# Streamlit framework
st.markdown('<h1 class="title">Interactive Storyteller for Kids</h1>', unsafe_allow_html=True)
st.markdown('<h3 class="header">Create Your Own Story</h3>', unsafe_allow_html=True)

# Input for OpenAI API key from user
openai_api_key = st.text_input("Enter your OpenAI API key:", key="apikey", placeholder="Your OpenAI API key here...", type="password")

# Input fields for story elements
character = st.text_input("Enter the main character's name:", key="character", placeholder="E.g., Max the Explorer")
setting = st.text_input("Enter the setting of the story:", key="setting", placeholder="E.g., A mystical forest")
plot = st.text_area("Enter a brief plot description:", key="plot", placeholder="E.g., Finds a magical artifact")

# Initialize the OpenAI LLM only if the API key is provided
if openai_api_key:
    try:
        # Initialize the OpenAI LLM with the provided API key
        llm = ChatOpenAI(model="gpt-3.5-turbo", api_key=openai_api_key)
        output_parser = StrOutputParser()
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "You are a creative storyteller. Please generate a short story based on the following details."),
                ("user", "Main Character: {character}\nSetting: {setting}\nPlot: {plot}")
            ]
        )
        chain = prompt | llm | output_parser

        # Generate story button
        if st.button("Generate Story"):
            if character and setting and plot:
                st.write("Generating your story, please wait...")

                # Generate the story using LangChain and OpenAI
                response = chain.invoke({'character': character, 'setting': setting, 'plot': plot})

                # Display the generated story
                st.subheader("Your Story")
                st.write(response)
            else:
                st.warning("Please fill in all the fields.")
    except Exception as e:
        st.error(f"An error occurred: {e}")
else:
    st.warning("Please enter your OpenAI API key.")
