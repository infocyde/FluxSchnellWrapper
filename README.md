# FluxSchnellWrapper
Just a simple streamlit wrapper around Flux Schnell calls to Replicate

Cooked it up in about an hour using Claude.  It isn't perfect (like if you change the prompt) you need to click somewhere outside the input window to update the page 
before hitting the Image Generate button.

# Note, this assumes you have a replicate key in an .env file a directory or more up from this project, so dotenv can load your key, else this will not work.
To get a key, create a replicate account at replicate.com, and then follow the instruction on getting a key and use chatGPT to figure out how to create a .env file for python if you don't know how (that is where you want to put the key)

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

