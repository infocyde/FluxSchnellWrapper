# Flux.1.1 + SD 3.5 Streamlit GUI for Replicate Flux API
Just a simple streamlit wrapper GUI around Flux.1 Schnell, Develop, Pro and Stability.ai's Stable Diffusion 3.5 API calls to Replicate.
This is written in Python and Streamlit.  You must have a python 3.1x interpreter installed on your system.

You can test a live version if you have a replicate auth token key here-

https://huggingface.co/spaces/infocyde/FluxGUI

To get a replicate auth token key, create a replicate account at replicate.com, and then follow the instruction on getting a key.

Also note, could I capture your key?  Yes.  Am I?  No.  I got 99 problems and grabbing keys for short term gain for long term consequences
ain't another one I want!

----------------------------------------------------------
To run locally: 

This pretty much assumes some knowledge of python, and a development enviornment like Visual Studio Code

1) In a terminal window, navigate to the folder where you are going to install this code, and then type (assumes GIT is installed)

Git clone https://github.com/infocyde/FluxSchnellWrapper.git

Note the above command might be slightly different if using Sudo but you can figure that out.

2) Create your virtual enviornment 

Navigate to where you downloaded this code / repo, then in a terminal window in visual studio type 

python -m venv .venv

When that is done, type in the terminal to activate your virtual environment

.venv\scripts\activate

If you have Conda or another way to manage python virtual enviornments, I'm sure you are knowledgable enough to figure the above out in your enviornment.

What is a virtual environment?

[ChatGPT] 
A virtual environment in Python is an isolated environment that allows you to install and manage dependencies separately from the system-wide Python installation. It is used to avoid conflicts between project-specific dependencies and to ensure that each project has its own specific package versions.

3) Install the requirements

In the terminal type

pip install -r requirements.txt  

4) run streamlit

In the terminal type (assuming you are in the directory of the project)

streamlit run app.py    

Hopefully it works!

This is pretty basic code.  You should be able to hack it better, I just wanted something fast, this works.  

Why is this better than using replicate's web interface?
- It isn't, just different
- It saves the images locally, so you don't have to hassle with that
- You can save prompts
- You can switch between models quickly without having to reinput a prompt

Have fun!

