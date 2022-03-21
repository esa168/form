from argon2 import hash_password
import streamlit as st
import streamlit_authenticator as stauth
import numpy as np
import pandas as pd

# https://towardsdatascience.com/how-to-add-a-user-authentication-service-in-streamlit-a8b93bf02031


# use name and passwords
names = ['John Smith','Rebecca Briggs']
usernames = ['jsmith','rbriggs']
#passwords = ['123','456']
passwords = [
    ['$2b$12$v/JwtgTZejC50b/b9S6zhuZpybSeG.xUzwHxY21FcjcWH69bc/0oO', 
     '$2b$12$4iT9nNOARBC.3j13HsJ0NOi/XKjPlBjgofTZ6vjHqK3iAswdEpRvy', 
     '$2b$12$XLocTIhMMhmNJS8VQSDpq.3HgZGg8iafKpsgqDoC0sqsT7aemPNnS'], 
    
    ['$2b$12$o1os2aVTxo.0NfPLxAJTc.n48KpwzQKgRqcLPNLLJH9K8iYcyatsm', 
     '$2b$12$NNJitnSt2wO0MzQw/kT03ubiELqUetwju9M10Y3GDucB.FiWdLTai', 
     '$2b$12$qZNDLEwi5hoNa/r3l5tul.onYqzB5B.oTgpS6ZwLY4u.vDs2JHZKG']
    ]


def generate_hash_list(password):
    hash_list =[]
    for pwd in password:
        hashed_passwords = stauth.Hasher(pwd).generate()
        hash_list.append(hashed_passwords)
    return hash_list

def generate_hash(pwd):
        return stauth.Hasher(pwd).generate()

def log_in (names,usernames,hashed_passwords):

    authenticator = stauth.Authenticate(names,usernames,hashed_passwords,'some_cookie_name','some_signature_key',cookie_expiry_days=0)
    #authenticator = stauth.Authenticate(names,usernames,hashed_passwords, cookie_expiry_days=0)
    
    name, authentication_status, username = authenticator.login('Login','main')
    if authentication_status:
        st.write('Welcome *%s*' % (name))
        st.title('Some content')
    elif authentication_status == False:
        st.error('Username/password is incorrect')
    elif authentication_status == None:
        st.warning('Please enter your username and password')
    
    
        

def streamlit ():
    st.sidebar.header ('Main Data')
    date = st.sidebar.date_input ("Date")
    cust= st.sidebar.text_input ("Customer Name")
    prod_code = st.sidebar.text_input ('Product Code')
    dosage = st.sidebar.number_input ("dosage")
    resin = st.sidebar.text_input ("Resin")
    color = st.sidebar.color_picker ("Color")
    

def main ():
    #print (generate_hash(passwords))
    #hash_password = generate_hash(passwords)
    
    log_in (names,usernames,hash_password)
    
    







if __name__ == '__main__':
    main()


