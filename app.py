import os
from PIL import Image
import streamlit as st
from lyzr_automata.ai_models.openai import OpenAIModel
from lyzr_automata import Agent, Task
from lyzr_automata.tasks.task_literals import InputType, OutputType
from lyzr_automata.pipelines.linear_sync_pipeline  import  LinearSyncPipeline
from lyzr_automata import Logger
from dotenv import load_dotenv; load_dotenv()

# Setup your config
st.set_page_config(
    page_title="Book Writing Assistant",
    layout="centered",   
    initial_sidebar_state="auto",
    page_icon="./logo/lyzr-logo-cut.png"
)

# Load and display the logo
image = Image.open("./logo/lyzr-logo.png")
st.image(image, width=150)

# App title and introduction
st.title("Book Writing Assistant by Lyzr")
st.markdown("### Welcome to the Book Writing Assistant!")
st.markdown("Book Writing Assistant your AI muse, offering writing assistance, and even image generation to fuel your creativity.!!!")

# Custom function to style the app
def style_app():
    # You can put your CSS styles here
    st.markdown("""
    <style>
    .app-header { visibility: hidden; }
    .css-18e3th9 { padding-top: 0; padding-bottom: 0; }
    .css-1d391kg { padding-top: 1rem; padding-right: 1rem; padding-bottom: 1rem; padding-left: 1rem; }
    </style>
    """, unsafe_allow_html=True)

# Book Writing Assistant Application

# replace this with your openai api key or create an environment variable for storing the key.
API_KEY = os.getenv('OPENAI_API_KEY')

 
open_ai_model_image = OpenAIModel(
    api_key=API_KEY,
    parameters={
        "n": 1,
        "model": "dall-e-3",
    },
)


open_ai_model_text = OpenAIModel(
    api_key= API_KEY,
    parameters={
        "model": "gpt-4-turbo-preview",
        "temperature": 0.5,
        "max_tokens": 1500,
    },
)

def book_writing_assistant(genre):
    
    writer_agent = Agent(
        prompt_persona="You are an expert book writer and a graphic designer, good at writing books on a single keyword as well making the attractive cover pages for your books, you can also provide the chapter's regrading the any topic",
        role="book writer", 
    )

    title_generation = Task(
        name="Book Title Creator",
        agent=writer_agent,
        output_type=OutputType.TEXT,
        input_type=InputType.TEXT,
        model=open_ai_model_text,
        instructions="Use the description provided and write some set of titles for the book. Use your creativity. [IMPORTANT!] Setup the events in a detailed manner",
        log_output=True,
        enhance_prompt=False,
        default_input=genre
    )

    chapter_generation = Task(
        name="Book Chapters Creator",
        agent=writer_agent,
        output_type=OutputType.TEXT,
        input_type=InputType.TEXT,
        model=open_ai_model_text,
        instructions="Use the description provided and write some set book chapter's and well give the blueprint of how to write the book on provided description. Use your creativity. [IMPORTANT!] Setup the events in a detailed manner",
        log_output=True,
        enhance_prompt=False,
        default_input=genre
    )

    book_writing_tips =  Task(
        name="Book Writing Tips",
        agent=writer_agent,
        output_type=OutputType.TEXT,
        input_type=InputType.TEXT,
        model=open_ai_model_text,
        instructions="Use the description provided and give the 4-5 bullet points in 20-30 words of book writing tips on provided description. Use your creativity. [IMPORTANT!] Setup the events in a detailed manner",
        log_output=True,
        enhance_prompt=False,
        default_input=genre
    )

    
    book_cover_image = Task(
        name="Book Cover Image Creation",
        output_type=OutputType.IMAGE,
        input_type=InputType.TEXT,
        model=open_ai_model_image,
        log_output=True,
        instructions="Generate an Image which is suitable to the given description. Capture every detail. Minimalistic style. [IMPORTANT!] Avoid any text or numbers in the image.",
    )

    logger = Logger()
    

    main_output = LinearSyncPipeline(
        logger=logger,
        name="Book Writing Assistant",
        completion_message="Book Writing Assistant Generated all things!",
        tasks=[
            title_generation,
            chapter_generation,
            book_writing_tips,
            book_cover_image,
        ],
    ).run()

    return main_output


if __name__ == "__main__":
    style_app() 
    book_brief = st.text_input("Enter about the book, a title or a genre")
    button=st.button('Submit')
    if (button==True):
        
        generated_output = book_writing_assistant(book_brief)

        # DISPLAY OUTPUT
        title_output = generated_output[0]['task_output']
        st.header('Suggested Titles')
        st.write(title_output)
        st.markdown('---')

        chapter_output = generated_output[1]['task_output']
        st.header("Suggested Chapter's")
        st.write(chapter_output)
        st.markdown('---')

        writing_tips = generated_output[2]['task_output']
        st.header('Writing Tips')
        st.write(writing_tips)
        st.markdown('---')

        image_file_name = generated_output[3]['task_output'].local_file_path
        st.header('Book Cover Page')
        st.image(image_file_name, caption='Book Writing Assistant - Lyzr') 
        
    with st.expander("ℹ️ - About this App"):
        st.markdown("""
        This app uses Lyzr Automata Agent to create the book title, chapters, cover image and also providing the writing tips. For any inquiries or issues, please contact Lyzr.
        
        """)
        st.link_button("Lyzr", url='https://www.lyzr.ai/', use_container_width = True)
        st.link_button("Book a Demo", url='https://www.lyzr.ai/book-demo/', use_container_width = True)
        st.link_button("Discord", url='https://discord.gg/nm7zSyEFA2', use_container_width = True)
        st.link_button("Slack", url='https://join.slack.com/t/genaiforenterprise/shared_invite/zt-2a7fr38f7-_QDOY1W1WSlSiYNAEncLGw', use_container_width = True)