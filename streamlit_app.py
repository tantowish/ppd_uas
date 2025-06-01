import streamlit as st
import requests

st.title('Streamlit and Flask Integration')

response = requests.get('http://localhost:5000/api')
data = response.json()

st.write(data['message'])
