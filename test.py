
import streamlit as st
import random


def get_pwd ():
    password = random.randint(1,100)
    password ='123'
    return str(password)

#@st.cache (suppress_st_warning=True)
def enter_pwd ():
    
    '''
    st.sidebar.header('Header')
    with st.sidebar.form('my form'):
        x = st.sidebar.text_input('Enter your personal password : ')
        button = st.sidebar.button('Submit')  
    if button:
        return x
    '''
    
    if "pwd_correct" not in st.session_state:
        st.session_state['pwd_correct'] = False
    if  st.session_state ['pwd_correct'] == False:
        x = st.text_input('Enter your personal password : ')
        button = st.button('Submit') 
        if button :
            return x 
        
    
def run_app():
    st.write ('running the app and generate a random number')
    st.write (str(random.randint(1,100)))


def main ():
    file_pwd = get_pwd()
    if 'password' not in st.session_state:
        st.session_state['password'] = file_pwd
        #st.write ('password is : ')
        #st.write (st.session_state['password'])
        x = enter_pwd()
        if "usr_pwd" not in st.session_state:
            st.session_state['usr_pwd'] = x
    
    if st.session_state['pwd_correct'] == False:
        if st.session_state['usr_pwd'] == st.session_state['password'] :
            st.write ('correct password')
            run_app()
            st.subheader('Welcome to the app')
            st.session_state['pwd_correct'] = True

        else:
            st.write ('incorrect password')

        
    


main()


#!!

def main_1():
    x = st.text_input('Enter your password : ')
    
    if 'x' not in st.session_state:
        st.session_state['x'] = x

