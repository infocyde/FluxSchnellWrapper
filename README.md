# Flux.1 Streamlit  API Wrapper 
Just a simple streamlit wrapper around Flux.1 Schnell, Develop, and Pro API calls to Replicate
This is written in Python and Streamlit.  You must have a python 3.1x interpreter installed on your system.

This pretty much assumes some knowledge of python, and a development enviornment like Visual Studio Code

Note, ideally you put your replicate_api_token in your .env file (google or chatGPT for how to do that).  But there is a spot now above the generate image button to paste your replicate_api_token if you don't have it in your .env file
To get a replicate auth token key, create a replicate account at replicate.com, and then follow the instruction on getting a key.

1) In a terminal window, navigate to the folder where you are going to install this code, and then type (assumes GIT is installed)

Git clone https://github.com/infocyde/FluxSchnellWrapper.git

Note the above command might be slightly different if using Sudo but you can figure that out.


2) Create your virtual enviornment 

Navigate to where you downloaded this code / repo, then in a terminal window in visual studio type 

python -m venv .venv

When that is done, type in the termainal to activate your virtual environment

.venv\scripts\activate

If you have Conda or another way to manage python virtual enviornments, I'm sure you are knowledgable enough to figure the above out in your enviornment.

What is a virtual environment?

[ChatGPT] 
A virtual environment in Python is an isolated environment that allows you to install and manage dependencies separately from the system-wide Python installation. It is used to avoid conflicts between project-specific dependencies and to ensure that each project has its own specific package versions.

2) Install the requirements

In the terminal type

pip install -r requirements.txt  

3) run streamlit

streamlit run app.py    

Hopefully it works!

This is pretty basic code.  You should be able to hack it better, I just wanted something fast, this works.  I will probably add support for calls to the other models as well down the road.

Have fun!

