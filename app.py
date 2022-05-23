import streamlit as st
import pandas as pd



def is_csv(infile):
    
    import csv
    
    #https://stackoverflow.com/questions/2984888/check-if-file-has-a-csv-format-with-python    
    try:
        with open(infile, newline='') as csvfile:
            start = csvfile.read(4096)

            # isprintable does not allow newlines, printable does not allow umlauts...
            if not all ( [c in start.printable or c.isprintable() for c in start ] ):
                return False
            dialect = csv.Sniffer().sniff(start)
            return True
        
    except csv.Error:
        # Could not get a csv dialect -> probably not a csv.
        return False
    



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





def no_duplicate_keys (df,col_name):
    '''
     check for duplicates in a column of a dataframe and returns a list containing the values of duplicates

    df = dataframe
    col_name = string , col name where key is located  (where there must not have duplicates

    return 
         list values in the col_name that has duplicates 
         list = null if no duplicates
    '''

    from collections import Counter

    row_values = list(df[col_name])
    d =  Counter(row_values)  

    #https://stackoverflow.com/questions/52072381/how-to-print-only-the-duplicate-elements-in-python-list
    list_of_duplicate_key = [k for k, v in d.items() if v > 1]

    return list_of_duplicate_key





def chk_primary_keys (df, list_of_keys):
    # good for a dataframe that has 1 or 2 primary keys only. 
    # cannot be more than 2 primary keys
    # Check for duplicates in the dataframe where the col name are in a LIST 

    # df = the dataframe
    # list_of_keys = the list of the keys  ; w/ [0] as the first key

    # Returns
    # =  a dictionary where duplicates are listed 
    # if 2 primary keys : key = value of the first key, value = in a list, the values of the 2nd key
    # if 1 primary key : {duplicates : [list of the values of the duplicates]}
    # = Null dictionary  if no duplicates
    # this update also now prints the error before returing the dict 

    # get the column name of the first primary key
    
    dup_dict = {}
    
    if len (list_of_keys) > 0:
        prim_key_col_name = list_of_keys[0]

        if len(list_of_keys)== 1:
            
            list_of_duplicate_key =  no_duplicate_keys (df, prim_key_col_name )
            if len (list_of_duplicate_key)>0:
                dup_dict [prim_key_col_name] = list_of_duplicate_key


        elif len(list_of_keys) == 2:
            # get the first set
            unique_prim_key = df[prim_key_col_name].unique()

            # get the 2nd key col name 
            second_key_col_name = list_of_keys[1]

            # Loop to each 1st key to get 2nd key
            for each_key in unique_prim_key:
                # filter using first key
                filter_df = df[df[prim_key_col_name] == each_key ]

                list_of_duplicate_key =  no_duplicate_keys (filter_df , second_key_col_name)
                if len(list_of_duplicate_key)>0:
                    # { primary_key : seocndary_key with duplicate}
                    dup_dict[each_key] = list_of_duplicate_key
    
                
    # check if there are any contents in the dictionary    
    if len (dup_dict) > 0:
        # print the error 
        
        st.header  ('There are  Primary Key Conflicts.' )
   
        st.subheader  ('The details of the duplicates/conficts are :')
       
        str_1 = str(list_of_keys[0]) + ' : ' + str(list_of_keys[1]) 
        st.write ('Format of output is : ' + str_1 )
        
        for key in dup_dict:
            string = str(key) + ' : ' + str(dup_dict[key])
            st.write (string)
    
        
    else :
        st.title ('All consistent !!')
        st.balloons ()

            
    return dup_dict




    
    
def process(df, list_of_keys):
    
    # check if uploaded file is a csv file
    #input_csv = is_csv (uploaded_files)
    
    #list_of_keys  = ['key_1','key_2']
    with st.spinner('Procesing....'):
        
        chk_primary_keys (df, list_of_keys)
        


            

            
def main ():
    

 
    st.markdown(""" <style> #MainMenu {visibility: hidden;} 
                footer {visibility: hidden;}</style> """, 
                unsafe_allow_html=True)
    
    
    st.header ('FILE REQUIREMENTS')
    st.subheader ('Pls read carefully before using this app')
    
    
    '''

    * (1)  Must be a csv file
    * (2)  Must have exactly 2 columns w/c signifies the primary keys 
    * (3)  Values much have no white space and no null values 
    * (4)  Both Columns must have the same number of rows
    * (5)  Format of row values in each column must be of the same format (ie all integer or all string or all floats)
    * (6)  Impt to note that the ff are NOT the same : 
        *   W-2 , w2 , w-2  = as they have different asccii value
        *   12  3 , 123 , 1  23  
        *   123 , 123.00  =  must either both be an integer or both be a float
    '''
    
    
    uploaded_files = st.file_uploader("CSV file ONLY ", accept_multiple_files=False, type={'csv'} )
    
    if uploaded_files is not None:
        df = pd.read_csv (uploaded_files)
        
        # get col names
        old_col_names = df.columns.values.tolist()
        if len (old_col_names)!=2 :
            # col  should be 2 columns only
            return
        else:
            process (df, old_col_names)
    
    
    
if check_password():
    main()


 