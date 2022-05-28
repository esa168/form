
import streamlit as st
import random

@st.cache
def get_pwd ():
    password = random.randint(1,100)
    return str(password)

def first ():
    st.sidebar.header('Header')
    
    with st.sidebar.form('my form'):
        x = st.sidebar.text_input('Enter your personal password : ')
        button = st.sidebar.button('Submit')
    
    if button:
        return x
    

def run_app():
    st.write ('This is the app')
    st.write (str(random.randint(1,100)))

def main ():
    
    pwd = get_pwd ()
    x = first()
    
    print (pwd)

    if x == pwd:
        #st.subheader('Welcome to the app')
        #st.write('This is the app')
        run_app()


main()