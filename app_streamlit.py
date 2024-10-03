import streamlit as st
import replicate
import requests
import time
import os
import re
from dotenv import load_dotenv
from io import BytesIO
from PIL import Image
import base64

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
    # Initialize session state for prompt history
    if 'prompt_history' not in st.session_state:
        st.session_state.prompt_history = []

    def wait_for_image(url, max_attempts=10, delay=2):
        for attempt in range(max_attempts):
            response = requests.head(url)
            if response.status_code == 200:
                return True
            time.sleep(delay)
        return False

    def display_image(url):
        response = requests.get(url)
        if response.status_code == 200:
            image = Image.open(BytesIO(response.content))
            st.image(image, caption="Generated Image")
            return image
        else:
            st.error(f"Failed to download image. Status code: {response.status_code}")
            return None

    def get_image_download_link(img, filename, text):
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        href = f'<a href="data:file/png;base64,{img_str}" download="{filename}">**{text}**</a>'
        return href

    # Streamlit app
    st.title("Flux.1.X - Streamlit GUI")

    # Create three columns
    left_column, margin_col, right_column = st.columns([6, 1, 5])

    # Left column contents
    with left_column:
        input_prompt = st.text_area("Enter your prompt:", height=100)

        model_version = st.selectbox(
            "Model Version (schnell: fast and cheap, dev: quick and inexpensive, pro: moderate render time, most expensive)",
            options=["schnell", "dev", "pro","1.1-pro"],
            index=0
        )
        
        aspect_ratio = st.selectbox(
            "Aspect Ratio",
            options=["1:1", "16:9", "21:9", "2:3", "3:2", "4:5", "5:4", "9:16", "9:21"],
            index=0
        )

        # some default values since different versions of the model require different params
        guidance = None
        steps = None
        safety_checker = None
        interval = None
        safety_tolerance = None
        
        if model_version == "dev":
            guidance = st.slider(
                "Guidance - How closely the model follows your prompt, 1-10, default 3.5",
                min_value=0.0,
                max_value=10.0,
                value=3.5,
                step=0.01,
                format="%.2f"
            )
        
        if model_version.startswith("pro"):
            guidance = st.slider(
                "Guidance - How closely the model follows your prompt, 2-5, default is 3",
                min_value=2.0,
                max_value=5.0,
                value=3.0,
                step=0.01,
                format="%.2f"
            )
            
            steps = st.slider(
                "Steps - Quality/Detail of render, 1-100, default 25.",
                min_value=1,
                max_value=100,
                value=25,
                step=1
            )    

            interval = st.slider(
                "Interval - Variance of the image, 4 being the most varied, default is 1",
                min_value=1.0,
                max_value=4.0,
                value=1.0,
                step=0.01,
                format="%.2f"
            )  

            safety_tolerance = st.slider(
                "Safety Tolerance - 1 to 5, 5 being least restrictive, 1 default (3 on default on here)",
                min_value=1,
                max_value=5,
                value=3,
                step=1
            )     

            if not model_version.startswith("pro"):
                safety_checker = "On"
        #     safety_checker = st.radio(
        #         "Safety Checker - Turn on model NSFW checking",
        #         options=["Off", "On"],
        #         index=1,
        #         format_func=lambda x: "Disabled" if x == "On" else "Enabled"
        #     )
        
        seed = st.number_input("Seed (optional)", min_value=0, max_value=2**32-1, step=1, value=None, key="seed")

        replicate_key = st.text_input("Replicate Key - Required", key="rep_key", type="password")
        if replicate_key is None:
            st.warning("You must provide a replicate auth token key for this to work.")
            st.stop()
        else:
            os.environ["REPLICATE_API_TOKEN"] = replicate_key
        
        col1, col2, col3 = st.columns([2,2,4])
        with col1:
            generate_button = st.button("Generate Image")
            
        if generate_button:
            if replicate_key is None or replicate_key == "":
                st.warning("You must provide a replicate auth token key for this to work.")
                st.stop()

            
            
            
            if input_prompt:
                st.session_state.prompt_history.insert(0, input_prompt)
                with st.spinner():

                    input_dict = {
                        "prompt": input_prompt,
                        "aspect_ratio": aspect_ratio,
                        "output_format": "png",
                        "output_quality": 100 # output_quality, note this is ignored if output is .png
                       
                    }
               
                    if seed is not None:
                        input_dict["seed"] = seed
                    
                    if guidance is not None:
                        input_dict["guidance"] = guidance
                    
                    if steps is not None:
                        input_dict["steps"] = steps

                    if safety_checker is not None:
                        input_dict["disable_safety_checker"] = safety_checker == "On"
                        
                    if safety_tolerance is not None:    
                        input_dict["safety_tolerance"] = safety_tolerance

                    # Run the model with the prepared input
                    try:
                        
                        client = replicate.Client(api_token=replicate_key)
                        
                        output = client.run(
                            f"black-forest-labs/flux-{model_version}",
                            input=input_dict
                        )
                        
                        if isinstance(output, list) and len(output) > 0:
                            output = output[0]

                        if not isinstance(output, str):
                            st.error(f"Unexpected output format: {output}")
                        else:
                            with st.spinner('Waiting for image to be ready...'):
                                if wait_for_image(output):
                                    image = display_image(output)
                                    if image:
                                        timestamp = int(time.time())
                                        clean_prompt = re.sub(r'[^a-zA-Z0-9 ]', '', input_prompt)
                                        clean_prompt = clean_prompt.strip()[:30]
                                        clean_prompt = clean_prompt.replace(' ', '_')
                                        filename = f"{timestamp}_{clean_prompt}.png"
                                        
                                        st.markdown(get_image_download_link(image, filename, 'Download Image'), unsafe_allow_html=True)
                                else:
                                    st.error("Timed out waiting for image to be ready.")

                    except Exception as e:
                        st.error(f"Error generating image: {str(e)}")

            else:
                st.warning("Please enter a prompt.")

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