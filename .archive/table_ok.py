import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode, GridUpdateMode
import pandas as pd
import numpy as np
import requests
import streamlit as st
import pandas as pd
from st_aggrid import AgGrid

def option_1(df):
    #AgGrid(df)
    grid_return = AgGrid(df, editable=True)
    new_df = grid_return['data']
    print (new_df)


def option_2(dict):
    # headername = col name
    # field where data is coming from 
    df = pd.DataFrame(dict) 
    grid_options = {
        "columnDefs": [ 
                        {"headerName": "Material Code", "field": "rm_code","editable": False,},
                        
                        {"headerName": "Material Conc","field": "rm_conc","editable": False,},
                        ]
                    }
    
    grid_return = AgGrid(df, grid_options)
    #new_df = grid_return["data"]
  

def gui (dict):
    
    if 'dict' not in st.session_state:
        st.session_state['dict'] = dict
    else:
        dict = st.session_state['dict']

    #dict = st.session_state['dict']
    with st.container():
        st.markdown ('### Enter Formula')
        rm_code= st.text_input ("Code")
        #rm_code= st.number_input ("Code")
        rm_conc = st.number_input (label="Concentration", min_value=0.000001, max_value=100.00, step=0.000001, format="%.7f")
        
        click_formula = st.button ("Save")
        if click_formula:
            st.balloons() 
            dict ["rm_code"] .append(rm_code)
            dict ["rm_conc"] .append(rm_conc)

    
    option_2(dict)
    
    


dict = { 'rm_code':[],
        'rm_conc':[]
        }      

gui (dict)

