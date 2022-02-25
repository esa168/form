import streamlit as st
import numpy as np
import pandas as pd


'''
https://docs.streamlit.io/library/api-reference/data/st.dataframe
https://docs.streamlit.io/library/cheatsheet
https://docs.streamlit.io/library/api-reference
https://www.youtube.com/watch?v=LZH_7PCpN2o
https://github.com/PablocFonseca/streamlit-aggrid
https://github.com/streamlit/streamlit/issues/455
https://www.youtube.com/watch?v=CYi0pPWQ1Do


'''

def random():
    # Randomly fill a dataframe and cache it
    @st.cache(allow_output_mutation=True)
    def get_dataframe():
        return pd.DataFrame(
            np.random.randn(50, 20),
            columns=('col %d' % i for i in range(20)))


    df = get_dataframe()

    # Create row, column, and value inputs
    row = st.number_input('row', max_value=df.shape[0])
    col = st.number_input('column', max_value=df.shape[1])
    value = st.number_input('value')

    # Change the entry at (row, col) to the given value
    df.values[row][col] = value

    # And display the result!
    st.dataframe(df)


def agrid():
    from st_aggrid import AgGrid
    
    rows = [0*x  for x in range(10)]

    df = pd.DataFrame({'col1': rows, 'col2': rows})
    grid_return = AgGrid(df, editable=True)
    new_df = grid_return['data']
    #print (new_df)
    return new_df
 
 
    
df= pd.read_csv ('form.csv')

cust= st.text_input ("cust")
dosage = st.number_input ("dosage")
#st.write(df)
st.table(df)
next_code = st.button ("New Code")
reset = st.button ("Reset")


st.sidebar.header('Options')
options_form = st.sidebar.form ('form')
code = options_form.text_input ("rm code")
dosage = options_form.number_input ("concentration")



add_data= options_form.form_submit_button ("add data")
if add_data:
    new_data = {'code': code, 'conc': float(dosage)}
    df= df.append(new_data, ignore_index=True)
    df.to_csv('form.csv', index=False)
    df= pd.read_csv ('form.csv')
    st.experimental_rerun()
    #st.write(df)

if next_code :
    new_data = {'code': [], 'conc': []}
    df = pd.DataFrame.from_dict(new_data)
    df.to_csv('form.csv', index=False)
    
if reset :
    new_data = {'code': [], 'conc': []}
    df = pd.DataFrame.from_dict(new_data)
    df.to_csv('form.csv', index=False)


