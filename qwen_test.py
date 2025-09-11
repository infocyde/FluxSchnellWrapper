import streamlit as st
import replicate
import os
from PIL import Image
import tempfile
import requests
from datetime import datetime


from dotenv import load_dotenv
load_dotenv()

# Create output directory if it doesn't exist
OUTPUT_DIR = "output"
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

st.title("🎨 AI Image Editor")
st.write("Upload an image and describe how you want it changed!")

# Sidebar for settings
st.sidebar.header("Settings")
output_quality = st.sidebar.slider("Output Quality", 1, 100, 80, help="Higher quality = larger file size")

# File uploader
uploaded_file = st.file_uploader(
    "Choose an image file", 
    type=['png', 'jpg', 'jpeg', 'webp'],
    help="Upload the image you want to edit"
)

# Display uploaded image
if uploaded_file is not None:
    # Display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)
    
    # Save uploaded file temporarily to get a URL (for local testing)
    # In production, you'd want to upload to a cloud service
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        temp_path = tmp_file.name
    
    st.success("✅ Image uploaded successfully!")
    
replicate_key = st.text_input("Replicate Key - If not provided, will try to use the key in .env file", key="rep_key", type="password")
    
if replicate_key != None and replicate_key != "":
    os.environ["REPLICATE_API_TOKEN"] = replicate_key



    # Prompt input
    prompt = st.text_area(
        "What changes would you like to make?",
        placeholder="e.g., Change the sweater to be blue with white text",
        help="Describe how you want the image to be modified"
    )
    
    # Process button
    if st.button("🔄 Edit Image", type="primary"):
        if prompt.strip():
            try:
                with st.spinner("Processing your image... This may take a minute."):
                    # For this example, we'll use the temp file path
                    # In production, you'd upload to a cloud service and use that URL
                    with open(temp_path, "rb") as f:
                        input_data = {
                            "image": f,  # For local files
                            "prompt": prompt,
                            "output_quality": output_quality,
                            "disable_safety_checker": True

                        }


                        client = None
                        if replicate_key is None:
                            client =   replicate.Client()
                        else:
                            client = replicate.Client(api_token=replicate_key)
                        
                        # Run the Replicate model
                        output = client.run(
                            "qwen/qwen-image-edit",
                            input=input_data
                        )
                    
                    # Process and save outputs
                    if output:
                        st.success("🎉 Image editing complete!")
                        
                        # Create timestamp for unique filenames
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        
                        # Display and save each output
                        for index, item in enumerate(output):
                            # Get the image data
                            if hasattr(item, 'read'):
                                image_data = item.read()
                            else:
                                # If it's a URL, download it
                                response = requests.get(str(item))
                                image_data = response.content
                            
                            # Save to output folder
                            filename = f"edited_{timestamp}_{index}.webp"
                            filepath = os.path.join(OUTPUT_DIR, filename)
                            
                            with open(filepath, "wb") as file:
                                file.write(image_data)
                            
                            # Display the result
                            st.image(image_data, caption=f"Edited Image {index + 1}")
                            st.success(f"💾 Saved as: {filepath}")
                            
                            # Download button
                            st.download_button(
                                label=f"📥 Download Image {index + 1}",
                                data=image_data,
                                file_name=filename,
                                mime="image/webp"
                            )
                    else:
                        st.error("❌ No output received from the model")
                        
            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")
                st.info("💡 Make sure you have set up your Replicate API token and have credits available")
                
            finally:
                # Clean up temporary file
                if os.path.exists(temp_path):
                    os.unlink(temp_path)
        else:
            st.warning("⚠️ Please enter a prompt describing the changes you want to make")

else:
    st.info("👆 Please upload an image to get started")

# Display recent outputs
st.header("📁 Recent Outputs")
if os.path.exists(OUTPUT_DIR) and os.listdir(OUTPUT_DIR):
    output_files = [f for f in os.listdir(OUTPUT_DIR) if f.endswith(('.webp', '.png', '.jpg', '.jpeg'))]
    output_files.sort(reverse=True)  # Most recent first
    
    if output_files:
        st.write(f"Found {len(output_files)} saved images:")
        
        # Show thumbnails of recent outputs
        cols = st.columns(3)
        for i, filename in enumerate(output_files[:6]):  # Show only last 6
            with cols[i % 3]:
                filepath = os.path.join(OUTPUT_DIR, filename)
                try:
                    image = Image.open(filepath)
                    st.image(image, caption=filename, use_column_width=True)
                except Exception as e:
                    st.error(f"Could not load {filename}")
    else:
        st.write("No output files found yet.")
else:
    st.write("No output folder found yet. Process an image to create it!")

# Instructions
with st.expander("ℹ️ Setup Instructions"):
    st.markdown("""
    **Before using this app, make sure to:**
    
    1. Install required packages:
    ```bash
    pip install streamlit replicate pillow requests
    ```
    
    2. Set up your Replicate API token:
    ```bash
    export REPLICATE_API_TOKEN="your_token_here"
    ```
    Or set it in your environment variables.
    
    3. Run this app:
    ```bash
    streamlit run app.py
    ```
    
    **Note:** This app saves edited images to a local `output` folder and provides download buttons for easy access.
    """)

# Footer
st.markdown("---")
st.markdown("*Built with Streamlit and Replicate AI* 🚀")