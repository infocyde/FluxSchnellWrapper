# click file to startup streamlit example, edit line three 
@echo off
cd /d c:\somepath\somefolder
call .venv\Scripts\activate.bat
start "" http://localhost:8501
streamlit run app.py --server.port 8501