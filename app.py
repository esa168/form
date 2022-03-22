# streamlit_app.py

#from pyrsistent import v
#from tkinter import font
import streamlit as st
import pandas as pd 
#import numpy as np
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode, GridUpdateMode
import requests

# IP and MAC address
# ngrok
# new page for summary before sending 


def run_app_V0():

    dict = {
        'rm_code':[],
        'rm_conc':[]
        
    }
    
    # create a df from the dict
    df = pd.DataFrame(dict)
    
    #sidebar = st.sidebar
    st.sidebar.title("General Information")    

    date = st.sidebar.date_input ("Date")
    cust= st.sidebar.text_input ("Customer Name")
    prod_code = st.sidebar.text_input ('Product Code')
    dosage = st.sidebar.number_input ("dosage")
    resin = st.sidebar.text_input ("Resin")
    color = st.sidebar.color_picker ("Color")
    submit = st.sidebar.button ("Submit")
    if submit:
        st.sidebar.balloons()
        # save what needs to be save
    
    
    st.markdown("# Formula Section")
    with st.container():
        st.markdown ('### Enter Formula')
        rm_code= st.text_input ("Code")
        rm_conc = st.number_input (label="Concentration", min_value=0.000001, max_value=100.00, step=0.000001, format="%.7f")
     
        click_formula = st.button ("Save")
        if click_formula:
            st.balloons() 
            dict['rm_code'].append(rm_code)
            dict['rm_conc'].append(rm_conc)
            
            st.experimental_rerun() 
            
            
    with st.container ():
        st.markdown ('### Table')
  
 

        # And display the result!
        st.dataframe(df)

def run_app_v1():
    
    dict = {
        'rm_code':[],
        'rm_conc':[] 
    }
    
    # create a df from the dict
    df = pd.DataFrame(dict)
    

    st.markdown("### Formula Entry Form")
    
    
    #! SIDE BAR 
    st.sidebar.markdown("# General Information")
    #st.sidebar.title("General Information")

    date = st.sidebar.date_input ("Date", key= 'a')
    cust= st.sidebar.text_input ("Customer Name", key='b')
    prod_code = st.sidebar.text_input ('Product Code', key='c')
    dosage = st.sidebar.number_input ("dosage", key='d')
    resin = st.sidebar.text_input ("Resin",key='e')
    color = st.sidebar.color_picker ("Color", key='f')

        
    #! MAIN 
    with st.container():
        
        with st.form (key = 'formula', clear_on_submit=True):
            st.markdown ('##### Enter Formula')
            #st.subheader('Enter Formula')
            rm_code= st.text_input ("Code")
            rm_conc = st.number_input (label="Concentration", min_value=0.000001, max_value=100.00, step=0.000001, format="%.7f")
            submit_button = st.form_submit_button ("Submit")    
   
            #dict['rm_code'].append(rm_code)
            #dict['rm_conc'].append(rm_conc)
   
   
                
    with st.container ():
        st.markdown ('### Table')

        # And display the result!
        st.dataframe(df)
        
        #st.dataframe(df)
        
    with st.container():
        col1,col2 = st.columns (2)
        with col1:
            st.button ("Save This Code")
        with col2:
            var_list = ["b","c","d","e","f"]
            clear =  st.button (label="Next Code", on_click=clear_form)

def check_password():
    #https://docs.streamlit.io/knowledge-base/deploy/authentication-without-sso
    # not commit secrets to git hub
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 Password incorrect")
        return False
    else:
        # Password correct.
        return True

            
def clear_form ():
    # a is a datetime.date class
    # 2022-02-21 format 
    #st.session_state['a'] = 
 
    st.session_state['b'] = ""
    st.session_state['c'] = ""
    st.session_state['d'] = 0
    st.session_state['e'] = ""
    st.session_state['f'] = ""
    st.session_state['dict']={}
    st.session_state.pop('counter', None)
  
  
def clear_table (): 
    st.session_state['dict']={} 


def create_table(dict):
    # headername = col name
    # field where data is coming from 
    df = pd.DataFrame(dict) 
    grid_options = {
        "columnDefs": [ 
                        {"headerName": "Material Code", "field": "rm_code","editable": False,},
                        
                        {"headerName": "Material Conc","field": "rm_conc","editable": False,},
                        ]
                    }
    #new_df = grid_return["data"]    
    grid_return = AgGrid(df, grid_options)

  

     
    
def run_app_v2(dict):

    st.markdown("### Formula Entry Form")
    
    #! SIDE BAR 
    st.sidebar.markdown("# General Information")
    #st.sidebar.title("General Information")
    
    cmf_no =st.sidebar.text_input ("CMF No",key='j')

    #date = st.sidebar.date_input ("Date", key= 'a')
    cust= st.sidebar.text_input ("Customer Name", key='b')
    
    #!
  
    prod_kind = st.sidebar.selectbox("Product Kind", ("DC", "MB",'Others'),key='g')

    a_o = st.sidebar.text_input ("A/O",key='i')
        
    color = st.sidebar.color_picker ("Color", key='f')

    prod_code = st.sidebar.text_input ('Product Code', key='c')
    dosage = st.sidebar.number_input ("Dosage", key='d')
    resin = st.sidebar.text_input ("Resin",key='e')
    end_product = st.sidebar.text_area ("End Product",key='h')

 
    #remarks = st.sidebar.text_area ("Remarks",key='k')

    
        
    #! MAIN 
    with st.container():

        if 'dict' not in st.session_state:
            st.session_state['dict'] = dict
        else:
            dict = st.session_state['dict']
    
        with st.form (key = 'formula', clear_on_submit = True):
            st.markdown ('##### Enter Formula')
            #st.subheader('Enter Formula')
            rm_code= st.text_input ("Code")
            rm_conc = st.number_input (label="Concentration", min_value=0.000001, max_value=100.00, step=0.000001, format="%.7f")
            submit_button = st.form_submit_button ("Submit")           
            if submit_button:
                dict ["rm_code"] .append(rm_code)
                dict ["rm_conc"] .append(rm_conc)
   
               
    with st.container ():
        st.markdown ('### Table')
        create_table (dict)
        
        col_00, col_01,col_02 = st.columns (3)
        with col_00:
            st.write ("Total Sum")
        with col_01:
            str_disp = (sum(dict['rm_conc']))
            st.write (str_disp)
        with col_02:
            pass
    
            
    with st.container():
        col1,col2,col3 = st.columns (3)
        with col1:
            st.button ("Reset All", on_click=clear_form)
        with col2:
            var_list = ["b","c","d","e","f"]
            save_data =  st.button (label="Save all ", on_click=clear_form)
        with col3:
            st.button ("Clear Table", on_click=clear_table) 
  

      

    
def run_app_v3(dict):

    st.markdown("### Formula Entry Form")
    
        #! SIDE BAR 
    with st.expander("General Information"):  

        x1,x2,x3= st.columns (3)
        with x1:  
            cmf_no =st.text_input ("CMF No",key='j')  
        with x2:
            prod_code = st.text_input ('Product Code', key='c')
        with x3:
             a_o = st.text_input ("Account Officer (initials)",key='i')
         
         

        y1,y2,y3,y4 = st.columns (4)
        with y1:
            dosage = st.number_input ("Dosage", value = 0.4, key='d')
        with y2:
            resin_list = [ "HDPE", "PP-Homo", "PP-BLock", "PP-Random","LDPE", "LLDPE","PVC", "HIPS", "GPPS", 'others'  ]   
            #resin = st.text_input ("Resin",key='e')
            resin = st.selectbox ('Resin',resin_list,key ='resin')
        with y3:
            prod_kind = st.selectbox("Product Kind", ("DC", "MB",'Others'),key='g')
        with y4:
            color = st.color_picker ("Color", key='f')

        
        #!

        #date = st.sidebar.date_input ("Date", key= 'a')
        cust= st.text_input ("Customer Name", key='b')

        end_product = st.text_area ("End Product" ,key='h')

        remarks = st.text_area ("Remarks",key='k')

    
        
    #! MAIN 
    with st.container():

        if 'dict' not in st.session_state:
            st.session_state['dict'] = dict
        else:
            dict = st.session_state['dict']
    
        with st.form (key = 'formula', clear_on_submit = True):
            st.markdown ('###### Enter Formula')
            #st.subheader('Enter Formula')
            
            a1,a2 = st.columns (2)
            with a1:
                rm_code= st.text_input ("Code")
            with a2:
                rm_conc = st.number_input (label="Concentration",value =0.001, min_value=0.000001, max_value=100.00, step=0.000001, format="%.7f")
            
            submit_button = st.form_submit_button ("Submit")           
            if submit_button:
                dict ["rm_code"] .append(rm_code)
                dict ["rm_conc"] .append(rm_conc)
   
               
    with st.container ():
        

        st.markdown ('### Table')

            
        create_table (dict)
        
        col_00, col_01,col_02 = st.columns (3)
        with col_00:
            st.write ("Total Sum : ")
        with col_01:
            if len(dict['rm_conc'])>0:
                str_disp = (sum(dict['rm_conc']))
                st.write (str_disp)

        with col_02:
            pass
    
            
    with st.container():
        col1,col2,col3 = st.columns (3)
        with col1:
            st.button ("Reset All", on_click=clear_form)
        with col2:
            var_list = ["b","c","d","e","f"]
            save_data =  st.button (label="Save all ", on_click=clear_form)
        with col3:
            st.button ("Clear Table", on_click = clear_table) 
  

                      

        

    


            
    

def main ():
    
    #clear_form()
    
    dict = {
    'rm_code':[],
    'rm_conc':[] 
}

    
    #if check_password():

    df = run_app_v3 (dict) 
 
 
    
    
if __name__ == '__main__':
    main()


