import streamlit as st
from streamlit_multipage import MultiPage


def input_page(st, **state):
    st.title("Body Mass Index")
    st.write("Your BMI is:")

def compute_page(st, **state):
    st.title("Body Mass Index")
    st.write("Your BMI is:")

 


app = MultiPage()
app.st = st

app.add_app("Input Page", input_page)
app.add_app("BMI Result", compute_page)

app.run()