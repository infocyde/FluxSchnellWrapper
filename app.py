import streamlit as st
import replicate
import requests
import time
import os
import re
from dotenv import load_dotenv

# ******* For More Info on Flux.1 on Replicate ********
#                                                     *
#      https://replicate.com/black-forest-labs        *
#                                                     *
# *****************************************************

st.set_page_config(layout="wide", page_title="Flux.1 in Streamlit with Replicate!", page_icon=":frame_with_picture:")


# Load environment variables
load_dotenv()


# Global error catch as I'm lazy
try:


    # Initialize session state for prompt history and last saved image
    if 'prompt_history' not in st.session_state:
        st.session_state.prompt_history = []
    if 'last_saved_image' not in st.session_state:
        st.session_state.last_saved_image = None

    def download_image(url, prompt):
        if not os.path.exists('output'):
            os.makedirs('output')
        
        timestamp = int(time.time())
        clean_prompt = re.sub(r'[^a-zA-Z0-9 ]', '', prompt)
        clean_prompt = clean_prompt.strip()[:30]
        clean_prompt = clean_prompt.replace(' ', '_')
        
        filename = f"{timestamp}_{clean_prompt}.png"
        filepath = os.path.join('output', filename)
        
        response = requests.get(url)
        
        if response.status_code == 200:
            with open(filepath, 'wb') as file:
                file.write(response.content)
            st.success(f"Image downloaded and saved as output\{filename}")
            st.session_state.last_saved_image = filepath
            return filepath
        else:
            st.error(f"Failed to download image. Status code: {response.status_code}")
            return None

    def delete_last_image():
        if st.session_state.last_saved_image and os.path.exists(st.session_state.last_saved_image):
            os.remove(st.session_state.last_saved_image)
            st.success(f"Deleted: {os.path.basename(st.session_state.last_saved_image)}")
            st.session_state.last_saved_image = None
        else:
            st.warning("No image to delete or file not found.")

    # Streamlit app
    st.title("Flux.1 - Schnell, Dev Streamlit GUI")

    # Create three columns
    left_column, margin_col, right_column = st.columns([6, 1, 5])

    # Left column contents
    with left_column:
        
        
        
        input_prompt = st.text_area("Enter your prompt:", height=100)

        model_version = st.selectbox(
            "Model Version (schnell: fast and cheap, dev: quick and inexpensive, pro: moderate render time, most expensive)",
            options=["schnell", "dev"],
            index=0
        )
        
        
        aspect_ratio = st.selectbox(
            "Aspect Ratio",
            options=["1:1", "16:9", "21:9", "2:3", "3:2", "4:5", "5:4", "9:16", "9:21"],
            index=0
        )

        output_quality = st.slider("Output Quality", min_value=1, max_value=100, value=90, step=1)

        guidance = None

        # Note Guidance doesn't work as I've opted for now to just save PNG formats, where guidance is ignored.  Also supported are webp and jpeg
        if model_version == "dev":
            guidance = st.slider(
            "Guidance",
            min_value=0.0,
            max_value=10.0,
            value=3.5,
            step=0.01,
            format="%.2f"
        )

        # safety_checker = st.radio(
        #     "Disable Safety Checker",
        #     options=["Off", "On"],
        #     index=1,
        #     format_func=lambda x: "Disabled" if x == "On" else "Enabled"
        # )

        seed = st.number_input("Seed (optional)", min_value=0, max_value=2**32-1, step=1, value=None, key="seed")

        replicate_key = st.text_input("Replicate Key - If not provided, will try to use the key in .env file", key="rep_key")
        
        if replicate_key != None and replicate_key != "":
            os.environ["REPLICATE_API_TOKEN"] = replicate_key

        col1, col2,col3 = st.columns([2,2,4])
        with col1:
            generate_button = st.button("Generate Image")
        with col2:
            delete_button = st.button("Delete Last Image")

        if generate_button:
            if input_prompt:
                st.session_state.prompt_history.insert(0, input_prompt)
                with st.spinner():
                    input_dict = {
                        "prompt": input_prompt,
                        "aspect_ratio": aspect_ratio,
                        "output_format": "png",
                        "output_quality": output_quality,
                        "disable_safety_checker": False #safety_checker == "On"
                    
                    }
                    
                    # Add seed to the input dictionary only if it's not None
                    if seed is not None:
                        input_dict["seed"] = seed
                    
                    # add guidance
                    if model_version=="dev":
                        input_dict["guidance"] = guidance

                    # Run the model with the prepared input
                    output = replicate.run(
                        f"black-forest-labs/flux-{model_version}",
                        input=input_dict
                    )

                    
                    
                    filepath = download_image(output, input_prompt)
                    
                    if filepath:
                        st.image(filepath, caption="Generated Image")
            else:
                st.warning("Please enter a prompt.")

        if delete_button:
            delete_last_image()

    # Margin column (empty for spacing)
    with margin_col:
        st.empty()

    # Right column contents
    with right_column:
        st.subheader("Prompt History")
        
        prompt_history_container = st.container()
        
        with prompt_history_container:
            for i, prompt in enumerate(st.session_state.prompt_history):
                st.text(f"{i+1}. {prompt}")
        
        st.markdown("""
            <style>
                .stContainer {
                    max-height: 400px;
                    overflow-y: auto;
                }
            </style>
        """, unsafe_allow_html=True)
except Exception as ex:
    st.error(f"Something errored out {ex}")