import streamlit as st
import replicate
import requests
import time
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize session state for prompt history
if 'prompt_history' not in st.session_state:
    st.session_state.prompt_history = []

def download_image(url):
    timestamp = int(time.time())
    filename = f"{timestamp}.png"
    response = requests.get(url)
    
    if response.status_code == 200:
        with open(filename, 'wb') as file:
            file.write(response.content)
        st.success(f"Image downloaded and saved as {filename}")
        return filename
    else:
        st.error(f"Failed to download image. Status code: {response.status_code}")
        return None

# Streamlit app
st.title("Flux Schnell")

# Create two columns
left_column, margin_col, right_column = st.columns([7, 1, 4])

# Left column contents
with left_column:
    input_prompt = st.text_area("Enter your prompt:", height=100)

    aspect_ratio = st.selectbox(
        "Aspect Ratio",
        options=["1:1", "16:9", "21:9", "2:3", "3:2", "4:5", "5:4", "9:16", "9:21"],
        index=0
    )

    output_quality = st.slider("Output Quality", min_value=1, max_value=100, value=90, step=5)

    # safety_checker = st.radio(
    #     "Disable Safety Checker",
    #     options=["Off", "On"],
    #     index=1,
    #     format_func=lambda x: "Disabled" if x == "On" else "Enabled"
    # )

    if st.button("Generate Image"):
        if input_prompt:
            # Add the new prompt to the history
            st.session_state.prompt_history.insert(0, input_prompt)
            
            with st.spinner("Generating image..."):
                output = replicate.run(
                    "black-forest-labs/flux-schnell",
                    input={
                        "prompt": input_prompt,
                        "aspect_ratio": aspect_ratio,
                        "output_format": "png",
                        "output_quality": output_quality,
                        "disable_safety_checker": False #safety_checker == "On",
                    }
                )
                
                filename = download_image(output)
                
                if filename:
                    st.image(filename, caption="Generated Image")
        else:
            st.warning("Please enter a prompt.")

# Right column contents
with right_column:
    st.subheader("Prompt History")
    
    # Create a container for the prompt history
    prompt_history_container = st.container()
    
    # Display prompt history in a scrollable area
    with prompt_history_container:
        for i, prompt in enumerate(st.session_state.prompt_history):
            st.text(f"{i+1}. {prompt}")
    
    # Add some CSS to make the container scrollable
    st.markdown("""
        <style>
            .stContainer {
                max-height: 400px;
                overflow-y: auto;
            }
        </style>
    """, unsafe_allow_html=True)