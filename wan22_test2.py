import streamlit as st
import replicate
import requests
import os
from PIL import Image
import tempfile
import time, datetime

from dotenv import load_dotenv
load_dotenv()


# Configure the page
st.set_page_config(
    page_title="WAN Video Generator",
    page_icon="🎬",
    layout="wide"
)

# Title and description
st.title("🎬 WAN Video Generator")
st.markdown("""
Generate videos from images using the WAN 2.2 I2V Fast model on Replicate.
Upload an image or provide a URL, add a descriptive prompt, and create your video!
""")

# API Key input

replicate_key = st.text_input("Replicate Key - If not provided, will try to use the key in .env file", key="rep_key", type="password")
    
if replicate_key != None and replicate_key != "":
    os.environ["REPLICATE_API_TOKEN"] = replicate_key

temp_path = None

# Create output directory if it doesn't exist
OUTPUT_DIR = "output"
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# Main interface
col1, col2 = st.columns([1, 1])

if 1 ==1:
    st.header("📸 Input Image")
    
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

if 1 ==1:
    st.header("✍️ Video Prompt")
    
    # Prompt input
    prompt = st.text_area(
        "Describe the video you want to generate:",
        value="Close-up shot of an elderly sailor wearing a yellow raincoat, seated on the deck of a catamaran, slowly puffing on a pipe. His cat lies quietly beside him with eyes closed, enjoying the calm. The warm glow of the setting sun bathes the scene, with gentle waves lapping against the hull and a few seabirds circling slowly above. The camera slowly pushes in, capturing this peaceful and harmonious moment.",
        height=150,
        help="Provide a detailed description of the video motion and scene you want to create"
    )
    
    # Advanced options
    with st.expander("🔧 Advanced Options"):
        st.info("The WAN 2.2 I2V Fast model uses default parameters. Future versions may include additional controls.")
    
    # Generate button
    generate_button = st.button(
        "🎬 Generate Video", 
        type="primary", 
        #disabled=not (replicate_key and image_url and prompt),
        use_container_width=True
    )

# Generation section
if generate_button:
    if not temp_path:
        st.error("❌ Please provide an image (upload or URL).")
    elif not prompt.strip():
        st.error("❌ Please provide a video prompt.")
    else:
        try:
            # Show progress
            progress_placeholder = st.empty()
            status_placeholder = st.empty()
            
            with status_placeholder.container():
                st.info("🚀 Starting video generation...")
            
            # Keep file open during the entire operation
            with open(temp_path, "rb") as image_file:
                # Prepare input for Replicate
                replicate_input = {
                    "image": image_file,
                    "prompt": prompt,
                    "disable_safety_checker": True
                }
                
                # Show input details (create display version)
                display_input = {
                    "image": f"File: {temp_path}",
                    "prompt": prompt,
                    "disable_safety_checker": True
                }
                with st.expander("📋 Generation Details", expanded=True):
                    st.json(display_input)
                
                # Show generation status
                with status_placeholder.container():
                    st.info("⏳ Generating video... This may take a few minutes.")
                
                progress_bar = progress_placeholder.progress(0)
                
                client = None
                if replicate_key is None:
                    client = replicate.Client()
                else:
                    client = replicate.Client(api_token=replicate_key)
                
                # Start prediction - file stays open during this call
                output = client.run(
                    "wan-video/wan-2.2-i2v-fast",
                    input=replicate_input,
                )
            
            # File is automatically closed here
            progress_bar.progress(100)
            
            # Clear status messages
            progress_placeholder.empty()
            status_placeholder.empty()
            
            # Display results
            st.success("✅ Video generated successfully!")
            
            # Get video URL - Fixed handling
            if isinstance(output, str):
                # Output is already a URL string
                video_url = output
            elif hasattr(output, 'url') and callable(getattr(output, 'url')):
                # Output has a callable url method
                video_url = output.url()
            elif hasattr(output, 'url'):
                # Output has url as a property, not a method
                video_url = output.url
            else:
                # Fallback - convert to string
                video_url = str(output)

            # Optional debug (remove these lines once working):
            # st.write(f"Debug - Output type: {type(output)}")
            # st.write(f"Debug - Video URL: {video_url}")
            
            # Display video
            st.header("🎥 Generated Video")
            st.video(video_url)
            
            # Download section
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.markdown(f"**Video URL:** [Open in new tab]({video_url})")
            
            with col2:
                # Download button - Fixed handling
                try:
                    if hasattr(output, 'read') and callable(getattr(output, 'read')):
                        video_data = output.read()
                    else:
                        # Download from URL
                        response = requests.get(video_url)
                        response.raise_for_status()
                        video_data = response.content
                    
                    st.download_button(
                        label="⬇️ Download Video",
                        data=video_data,
                        file_name="generated_video.mp4",
                        mime="video/mp4"
                    )
                except Exception as e:
                    st.warning(f"Download unavailable: {str(e)}")
                    st.markdown(f"You can download directly from: {video_url}")
                    
        except Exception as e:
            st.error(f"❌ Error generating video: {str(e)}")
            
            # Show helpful error messages
            if "authentication" in str(e).lower():
                st.info("💡 Make sure your Replicate API token is valid and has sufficient credits.")
            elif "rate limit" in str(e).lower():
                st.info("💡 You may have hit rate limits. Please wait a moment and try again.")
            elif "invalid input" in str(e).lower():
                st.info("💡 Please check that your image URL is accessible and your prompt is appropriate.")

# Footer with information
st.markdown("---")
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    st.markdown("**Model:** WAN 2.2 I2V Fast")

with col2:
    st.markdown("**Provider:** Replicate")

with col3:
    st.markdown("**API Docs:** [replicate.com](https://replicate.com)")

# Cleanup temporary files
if uploaded_file and 'tmp_file' in locals():
    try:
        os.unlink(tmp_file.name)
    except:
        pass

# Usage instructions
with st.expander("📖 How to Use"):
    st.markdown("""
    1. **Get API Token**: Sign up at [Replicate](https://replicate.com) and get your API token
    2. **Add Image**: Upload an image or provide an image URL
    3. **Write Prompt**: Describe the video motion and scene you want
    4. **Generate**: Click the generate button and wait for processing
    5. **Auto-Save**: Videos are automatically saved to the `output/` directory
    6. **Download**: Optional manual download is still available
    
    **Output Directory:**
    - All generated videos are saved to: `output/`
    - Files are named with timestamps: `generated_video_YYYYMMDD_HHMMSS.mp4`
    - Directory is created automatically if it doesn't exist
    
    **Tips:**
    - Use clear, detailed prompts for better results
    - Higher resolution images generally work better
    - Processing time varies but typically takes 2-5 minutes
    - Make sure you have sufficient Replicate credits
    """)


OUTPUT_DIR = 'output'
# File management section
with st.expander("📁 File Management"):
    if os.path.exists(OUTPUT_DIR):
        output_files = [f for f in os.listdir(OUTPUT_DIR) if f.endswith('.mp4')]
        if output_files:
            st.markdown(f"**Generated Videos in `{OUTPUT_DIR}/`:**")
            for file in sorted(output_files, reverse=True):  # Most recent first
                filepath = os.path.join(OUTPUT_DIR, file)
                file_size = os.path.getsize(filepath) / (1024*1024)
                file_time = datetime.datetime.fromtimestamp(os.path.getctime(filepath)).strftime("%Y-%m-%d %H:%M:%S")
                
                col1, col2, col3 = st.columns([2, 1, 1])
                with col1:
                    st.text(f"📹 {file}")
                with col2:
                    st.text(f"{file_size:.1f} MB")
                with col3:
                    st.text(file_time)
        else:
            st.info("No videos generated yet.")
    else:
        st.info("Output directory will be created when first video is generated.")

# Error handling info
with st.expander("🔧 Troubleshooting"):
    st.markdown("""
    **Common Issues:**
    - **Authentication Error**: Check your API token
    - **Rate Limiting**: Wait a few minutes between requests
    - **Image Loading**: Ensure image URLs are publicly accessible
    - **Long Processing**: Video generation can take several minutes
    - **Credits**: Make sure you have sufficient Replicate credits
    
    **Supported Image Formats:** JPG, PNG, WebP
    """)