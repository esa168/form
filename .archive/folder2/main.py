import streamlit as st
import numpy as np
import pandas as pd



def clear_cache(df):
    #new_data = {'code': [], 'conc': []}
    new_data =  {
        'customer' : [],
        'prod_code' : [],
        'dosage' : [],
        'resin' : [],
        'code': [],
        'conc': [],
        'date': []
        }
    
    df = pd.DataFrame.from_dict(new_data)
    df.to_csv('form.csv', index=False)
    
    return df 
    
def streamlit_app(df):
    
    date = st.date_input ("Date")
    cust= st.text_input ("Customer Name")
    prod_code = st.text_input ('Product Code')
    dosage = st.number_input ("dosage")
    resin = st.text_input ("Resin")
    #st.write(df)
    
    
      #! the TABLE 
    st.table(df)
    next_code = st.button ("New Code")
    reset = st.button ("Reset")
    #exit = st.button ("Exit")

    
    #! SIDEBAR 
    # create side bar for user to enter code and concentration
    st.sidebar.header('Options')
    options_form = st.sidebar.form ('form')
    code = options_form.text_input ("rm code")
    dosage = options_form.number_input ("concentration")
    append_data= options_form.form_submit_button ("add data")
    
    
    if append_data:
        # append formula to the prod code 
        
        # date  
        # classiifcaiton,  end product, 
        # total, others, dosage, sm, cmf #, remarks
        # HTML 
        
        new_data = {
            'customer' : cust,
            'prod_code' : prod_code,
            'dosage' : dosage,
            'resin' : resin,
            'code': code, 
            'conc': float(dosage),
            'date': date
            }
          
        df = df.append(new_data, ignore_index=True)
        df.to_csv('form.csv', index=False)
        df= pd.read_csv ('form.csv')
        st.experimental_rerun()
        #st.write(df)

    if next_code :
        # next product code to enter
        # save the data first before clearing 
        df_master = df_master.append(df, ignore_index=True)
        df_master.to_csv ('master.csv', index=False) 
        df = pd.DataFrame.from_dict(temp_dict)
        df = clear_cache(df)
        st.experimental_rerun()

    
    if reset :
        # erase all entry we made 
        df = clear_cache(df)
        st.experimental_rerun()
     
    
def streamlit_app_form(df):
    
    #! SIDE BAR 
    st.sidebar.header ('Main Data')
    date = st.sidebar.date_input ("Date")
    cust= st.sidebar.text_input ("Customer Name")
    prod_code = st.sidebar.text_input ('Product Code')
    dosage = st.sidebar.number_input ("dosage")
    resin = st.sidebar.text_input ("Resin")
    color = st.sidebar.color_picker ("Color")



 
    
    #! the user interface to enter formula 
    with st.form (key='myform', clear_on_submit=True):

        
        
        rm_code = st.text_input ("Raw Material Code")
        rm_conc = st.number_input ("Raw Material Concentration")
        #! 3
        submit_formula = st.form_submit_button ("Submit")    
        
        #print ()
        #print (submit_formula)
        
        if submit_formula:
            #print ('inside')
            new_data = {
                'customer' : [cust],
                'prod_code' : [prod_code],
                'dosage' : [dosage],
                'resin' : [resin],
                'code': [rm_code],
                'conc': [rm_conc] ,
                'date': [date],
                'color' : [color]
                }
            
            df_new = pd.DataFrame.from_dict(new_data)
        
            df= df.append(new_data, ignore_index=True)
            #print ('in')
            #print (df)           
            st.experimental_rerun() 
 
 
 
    #! TABLE NOW 
    st.title ('Output')
    st.table(df)            
                
    

    
    col3, col4 = st.columns(2)
    with col3:
        #! 4
        next_prod_code = st.button ("New Code")
    with col4:
        #! 5
        reset_formula = st.button ("Reset")
        
        st.experimental_rerun()
       



def main ():
    master_dict = {
        'customer' : [],
        'prod_code' : [],
        'dosage' : [],
        'resin' : [],
        'code': [],
        'conc': [],
        'date': []
        }
    
    temp_dict = master_dict.copy()
    df = pd.DataFrame.from_dict(temp_dict)
    streamlit_app_form (df)
    
    #df= pd.read_csv ('form.csv')
    #df_master= pd.read_csv ("master.csv")


    
  
        

if __name__ == '__main__':
    main()
    

#! ARCHIVE ##############


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




