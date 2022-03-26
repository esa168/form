
from numpy import save
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


def send_data():

    if 'final_dict' in st.session_state:
        data = st.session_state['final_dict']
        with open (file_name,'w') as data_file:
            json.dump ( data , data_file, indent = 4)
        
        st.success("Data Saved")
        st.balloons()
        clear_all_entries()
        # todo: EMAIL STUFF 
    else :
        st.markdown ("# No DATA TO SAVE !! ")




def save_one_entry (main_dict, dict , counter_number):
    '''
    THE SAVE ENTRY BUTTON = save the current entry 
    loads existing json
    appends new data (dict)
    saves it again 
    
    '''
 
    st.session_state['primary_key'] = st.session_state['primary_key'] + 1
    
    main_dict[counter_number] ['formula']= dict

    #st.session_state['main_dict'] = main_dict

    if 'final_dict' not in st.session_state:
        st.session_state['final_dict'] = main_dict
    else:
        st.session_state['final_dict'].update(main_dict)
    

    # every time we save the data we clear the session state main dict    
    st.session_state.pop ('main_dict', None)
    clear_form()
        
         

def clear_all_entries ():
    '''
    CLEAR ALL ENTRIES BUTTON ADD FORMULAS ENTERED 
    zeros the json
    '''
    #with open (file_name,'w') as data_file:
    #    json.dump ( {}, data_file, indent=4)


    st.session_state.pop ('final_dict', None)
    st.session_state.pop('primary_key', None)
    st.session_state.pop ('main_dict', None)
    clear_form()


def clear_form ():
    
    '''
    clear all the entries in the form
    '''

    st.session_state['cmf'] = ""
    st.session_state['prod_code'] = ""
    st.session_state['sm'] = ""
    
    
    st.session_state['cust'] = ''
    st.session_state['end_product'] = ""
    st.session_state['remarks'] = "" 
    
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





def run_app(main_dict, dict):
    
    if "primary_key" not in st.session_state:
        st.session_state ['primary_key'] = 1  
  
    
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
        'formula':{}
        }
        
    
    # if 'main_dict' exist then wont go here, and normaly 
    # when SAVE ENTRY we have to clear session state
    if 'main_dict' not in st.session_state : 
        st.session_state['main_dict'] = main_dict
    else :
        dict = st.session_state['main_dict']

    
        

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
                st.session_state['dict'] = dict
   
               
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
            st.button ("Clear Table", on_click = clear_table)
        
        
        
    
        #! CLEAR SCREEN BUTTON (clear the PAGE only )
        with col2:
            st.button ("Clear Screen ", on_click = clear_form)

    
        #! SAVE ENTRY BUTTON  (save ONE ENTRY )  
        with col3:
            st.button (label="Save Entry", on_click= save_one_entry, args = (main_dict,dict,counter_number))

    

      


        with st.expander ("Clear All Entries or Quit (Pls Save Before Quiting"):
            
            x_col1,x_col2 = st.columns (2)
            
            #! CLEAR ALL ENTRIES BUTTON
            with x_col1:
                # clear all entries made in this session
                st.button ("Clear ALL Entries", on_click = clear_all_entries)
  
                    
                    
            #! SAVE AND QUIT BUTTON     
            with x_col2:            
                st.button ("Save and Quit", on_click = send_data)
                
  
                    
                    
                    


        
            
def main ():
    
    
    dict = {
    'rm_code':[],
    'rm_conc':[] 
}
    main_dict= {
    }
    
    
    if check_password():

        run_app (main_dict,dict) 


 
 
    
    
if __name__ == '__main__':
    main()




#! ARCHIVE ################################################################################################################################

