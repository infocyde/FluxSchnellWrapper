# Flux.1 Schnell Replicate API Wrapper (Also supports Develop Model)
Just a simple streamlit wrapper around Flux.1 Schnell and Develop API calls to Replicate
This is written in Python and Streamlit.  You must have a python 3.1x interpreter installed on your system.

# Note, ideally you put your replicate_api_token in your .env file (google or chatGPT for how to do that).  But there is a spot now above the generate image button to paste your replicate_api_token if you don't have it in your .env file
To get a replicate auth token key, create a replicate account at replicate.com, and then follow the instruction on getting a key.

1) Create your virtual enviornment 

Navigate to where you pulled this code, then in a terminal window in visual studio type 
python -m venv .venv

When that is done, type 

.venv\scripts\activate

If you have Conda or another way to manage python virtual enviornments, I'm sure you are knowledgable enough to figure the above out in your enviornment.

2) Install the requirements

pip install -r requirements.txt  

3) run streamlit

streamlit run app.py    

Hopefully it works!

This is pretty basic code.  You should be able to hack it better, I just wanted something fast, this works.  I will probably add support for calls to the other models as well down the road.

Have fun!

