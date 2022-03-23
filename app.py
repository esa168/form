# streamlit_app.py

#from pyrsistent import v
#from tkinter import font
from itertools import count
import streamlit as st
import pandas as pd 
#import numpy as np
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode, GridUpdateMode
import requests
import json

file_name = 'data.json'

# ngrok
# new page for summary before sending 
# TODO: email json file , use image to capture stuff and store
# TODO : cant save as json as empty dict 
# TODO : IP AND MAC ADDRESS



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


def send_data(dict):

    with open (file_name,'w') as f:
        json.dump (dict,f)
  

def save_data (dict):
    '''
    loads existing json
    appends new data (dict)
    saves it again 
    
    '''
    
    with open (file_name,'r') as data_file:
        data = json.load (data_file)
        data.update (dict)

    with open (file_name,'w') as data_file:
        json.dump ( data , data_file, indent = 4)
    # every time we save the data we clear the session state main dict    
    st.session_state.pop ('main_dict', None)
        
    
        

def clear_all_entries ():
    '''
    zeros the json
    '''
    with open (file_name,'w') as data_file:
        json.dump ( {}, data_file, indent=4)


    st.session_state.pop('primary_key', None)
    st.session_state.pop ('main_dict', None)



def clear_form ():
    # a is a datetime.date class
    # 2022-02-21 format 

    
    #! st expand vars
    st.session_state['cmf'] = ""
    st.session_state['prod_code'] = ""
    st.session_state['sm'] = ""
    
    # cannot reset dosage as there is a default value ; resin kind and color are not ordinary input widget
    #st.session_state['dos'] = 0
    #st.session_state['resin'] = ""
    #st.session_state['kind'] = ""
    #st.session_state['color'] = ""
    
    st.session_state['cust'] = ''
    st.session_state['end_product'] = ""
    st.session_state['remarks'] = "" 
    
    #!
    #st.session_state.pop('counter', None)

    st.session_state['dict']={
                        'rm_code':[],
                        'rm_conc':[] 
                        }  

  

def clear_table (): 
    st.session_state['dict']={
                        'rm_code':[],
                        'rm_conc':[] 
                        } 





def run_app_v5(main_dict, dict):
    

    # counter number for formula number and later on the key in the dict
    if "primary_key" not in st.session_state:
        st.session_state['primary_key'] = 1  
    counter_number = st.session_state['primary_key']     

    
    st.markdown("### FORMULA ENTRY NO  :  "+ str(counter_number))
    
    #? EXPANDER SECTION
    with st.expander("General Information"):  

        x1,x2,x3= st.columns (3)
        with x1:  
            cmf_no =st.text_input ("CMF No",key='cmf')  
        with x2:
            prod_code = st.text_input ('Product Code', key='prod_code')
        with x3: 
            sm = st.text_input ("Account Officer (initials)",key='sm')
         
         
        y1,y2,y3,y4 = st.columns (4)
        with y1:
            dosage = st.number_input ("Dosage", value = 0.4, key='dos')
        with y2:
            resin_list = [ "HDPE", "PP-Homo", "PP-BLock", "PP-Random","LDPE", "LLDPE","PVC", "HIPS", "GPPS", 'others'  ]   
            resin = st.selectbox ('Resin',resin_list,key ='resin')
        with y3:
            prod_kind = st.selectbox("Product Kind", ("DC", "MB",'Others'),key='kind')
        with y4:
            color = st.color_picker ("Color", key='color')

        
        #date = st.sidebar.date_input ("Date", key= 'a')
        cust= st.text_input ("Customer Name", key='cust')
        end_product = st.text_area ("End Product" ,key='end_product')
        remarks = st.text_area ("Remarks",key='remarks')
   
    # assign all entered values to a dict and the session state     
    main_dict[counter_number] = {
        'cmf_no' : cmf_no,
        'prod_code': prod_code,
        'sm': sm,
        'dosage': dosage,
        'resin': resin,
        'prod_kind':prod_kind,
        'color':color,
        'cust':cust,
        'end_product':end_product,
        'remarks':remarks,
        }
        
        
    if 'main_dict' not in st.session_state : 
        st.session_state['main_dict'] = main_dict

    
        

    with st.container():
        
        # this is only true on the first run but once we clear table this is not true anymore
        if 'dict' not in st.session_state:
            st.session_state['dict'] = dict
        else:
            dict = st.session_state['dict']
    
    
        #? ENTER FORMULA 
        with st.form (key = 'formula', clear_on_submit = True):
            st.markdown ('#### *Enter Formula*')
            #st.subheader('Enter Formula')
            
            a1,a2 = st.columns (2)
            with a1:
                rm_code= st.text_input ("Code")
            with a2:
                rm_conc = st.number_input (label="Concentration",value =0.001, min_value=0.000001, max_value=100.00, step=0.000001, format="%.7f")
            
            #! SUBMIT BUTTON 
            submit_button = st.form_submit_button ("Submit")           
            if submit_button:
                dict ["rm_code"] .append(rm_code)
                dict ["rm_conc"] .append(rm_conc)
   
               
    with st.container ():
        
        tbl1,tb12,tbl3 = st.columns (3)
        with tbl1:
            st.write ('  ')
        with tb12:
            st.markdown ('#### *Table of Entries*')
        with tbl3:
            st.write ('')
            
        create_table (dict)
        
        # calc the total sum of mat conc
        col_00, col_01 = st.columns (2)
        with col_00:
            st.write ("Total Sum : ")
        with col_01:
            if len(dict['rm_conc'])>0:
                str_disp = (sum(dict['rm_conc']))
                st.write (str_disp)


            
    with st.container():
        col1,col2,col3 = st.columns (3)
        
        # CLEAR TABLE BUTTON = ok  
        with col1:
            clr_tbl = st.button ("Clear Table", on_click = clear_table)
        
        
        #! CLEAR SCREEN BUTTON
        with col2:
            clr_scrn = st.button ("Clear Screen ", on_click = clear_form)
            if clr_scrn:
                st.session_state.pop ('main_dict', None)
    
        #! SAVE ENTRY BUTTON    
        with col3:
            var_list = ["b","c","d","e","f"]
            save_entry =  st.button (label="Save Entry", on_click = clear_form)
            st.session_state['primary_key'] = st.session_state['primary_key'] + 1
            if save_entry:
                main_dict = st.session_state['main_dict']
                save_data(main_dict)
    

      


        with st.expander ("Clear All Entries or Quit (Pls Save Before Quiting"):
            
            x_col1,x_col2 = st.columns (2)
            
            #! CLEAR ALL ENTRIES BUTTON
            with x_col1:
                # clear all entries made in this session
                reset_all = st.button ("Clear ALL Entries", on_click = clear_form)
                if reset_all:
                    clear_all_entries()
                    
                    
            #! SAVE AND QUIT BUTTON     
            with x_col2:            
                end_program = st.button ("Save and Quit")
                
                if end_program:
                    # email json and reset json to zero
                    send_data(main_dict)
                    st.success("Data Saved")
                    


        
            
def main ():
    
    #clear_form()
    
    dict = {
    'rm_code':[],
    'rm_conc':[] 
}
    main_dict= {
    }
    
    
    #if check_password():

    run_app_v5 (main_dict,dict) 
    #st.balloons()

 
 
    
    
if __name__ == '__main__':
    main()




#! ARCHIVE ################################################################################################################################


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
  


def run_app_v3(main_dict, dict):
    

    
    # counter number for formula number and later on the key in the dict
    if "primary_key" not in st.session_state:
        st.session_state['primary_key'] = 1  
    counter_number = st.session_state['primary_key']     

    

    st.markdown("### FORMULA ENTRY NO  :  "+ str(counter_number))
    
    # EXPANDER SECTION
    with st.expander("General Information"):  

        x1,x2,x3= st.columns (3)
        with x1:  
            cmf_no =st.text_input ("CMF No",key='cmf')  
        with x2:
            prod_code = st.text_input ('Product Code', key='prod_code')
        with x3:
             sm = st.text_input ("Account Officer (initials)",key='sm')
         
         
        y1,y2,y3,y4 = st.columns (4)
        with y1:
            dosage = st.number_input ("Dosage", value = 0.4, key='dos')
        with y2:
            resin_list = [ "HDPE", "PP-Homo", "PP-BLock", "PP-Random","LDPE", "LLDPE","PVC", "HIPS", "GPPS", 'others'  ]   
            resin = st.selectbox ('Resin',resin_list,key ='resin')
        with y3:
            prod_kind = st.selectbox("Product Kind", ("DC", "MB",'Others'),key='kind')
        with y4:
            color = st.color_picker ("Color", key='color')

        
        #date = st.sidebar.date_input ("Date", key= 'a')
        cust= st.text_input ("Customer Name", key='cust')

        end_product = st.text_area ("End Product" ,key='end_product')

        remarks = st.text_area ("Remarks",key='remarks')

    
        
    #! MAIN 
    with st.container():
        

 
        # this is only true on the first run but once we clear table this is not true anymore
        if 'dict' not in st.session_state:
            st.session_state['dict'] = dict
        else:
            dict = st.session_state['dict']
    
    
        #! enter formula FORM 
        with st.form (key = 'formula', clear_on_submit = True):
            st.markdown ('#### *Enter Formula*')
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
        
        tbl1,tb12,tbl3 = st.columns (3)
        with tbl1:
            st.write ('  ')
        with tb12:
            st.markdown ('#### *Table of Entries*')
        with tbl3:
            st.write ('')
            
        create_table (dict)
        
        col_00, col_01 = st.columns (2)
        with col_00:
            st.write ("Total Sum : ")
        with col_01:
            if len(dict['rm_conc'])>0:
                str_disp = (sum(dict['rm_conc']))
                st.write (str_disp)


            
    with st.container():
        col1,col2,col3 = st.columns (3)
        
        with col1:
            clr_tbl = st.button ("Clear Table", on_click = clear_table)
        
        with col2:
            st.button ("Clear Screen ", on_click = clear_form)
            
        with col3:
            var_list = ["b","c","d","e","f"]
            save_entry =  st.button (label="Save Entry", on_click = clear_form)
            st.session_state['primary_key'] = st.session_state['primary_key'] + 1
            if save_entry:
  
                
                '''
                main_dict[st.session_state['primary_key']] = {
                    'cmf_no':cmf_no,
                    'prod_code':prod_code,
                    'sm':sm,
                    'dosage':dosage,
                    'resin':resin,
                    'product_kind':prod_kind,
                    'color':color,
                    'customer':cust,
                    'end_product':end_product,
                    'remarks':remarks,
                    'formula' : dict
                }

                '''
                main_dict[cmf_no] = {
                    'cmf_no':cmf_no,
                    'prod_code':prod_code,
                    'sm':sm,
                    'dosage':dosage,
                    'resin':resin,
                    'product_kind':prod_kind,
                    'color':color,
                    'customer':cust,
                    'end_product':end_product,
                    'remarks':remarks,
                    'formula' : dict
                }
                
                save_data(main_dict)
                clear_form()


            


        with st.expander ("Clear All Entries or Quit (Pls Save Before Quiting"):
            
            x_col1,x_col2 = st.columns (2)
            
            with x_col1:
                # clear all entries made in this session
                reset_all = st.button ("Clear ALL Entries", on_click = clear_form)
                if reset_all:
                    clear_all_entries()
                    
                    
                
            with x_col2:            
                end_program = st.button ("Save and Quit")
                
                if end_program:
                    send_data(main_dict)
                    st.success("Data Saved")
                    



