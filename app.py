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
        
        st.header  ('There are  Primary Key Conflicts. Please check the files and correct the  primary key conflicts.' )
        #st.subheader ('The columns that have the  primary key conficts are named:')
        
        #for keys in list_of_keys:
        #    st.write (keys)
        #st.write  (list_of_keys)
        st.header  ('The details of the duplicates are :')
        st.write ('(Format of output below is  primary key 1 : primary key 2)')
        #st.write (dup_dict)
        # {2: [15], 6599: [15], 6603: [15]}
        
        for key in dup_dict:
            string = str(key) + ' : ' + str(dup_dict[key])
            st.write (string)
    
        
    else :
        st.title ('All consistent !!')
        st.balloons ()

            
    return dup_dict





    
def process(uploaded_files):
    
    # check if uploaded file is a csv file
    #input_csv = is_csv (uploaded_files)
    
    input_csv = True
    
    if input_csv :
    
        df = pd.read_csv (uploaded_files)
        # rename 2 columns
        # make sure all lowcaps
        
        
        list_of_keys  = ['key_1','key_2']
        dict = chk_primary_keys (df, list_of_keys)
        

        #st.write(df)
    else :
        st.write ('Not a csv file')
        
     
    
def process_1(df, list_of_keys):
    
    # check if uploaded file is a csv file
    #input_csv = is_csv (uploaded_files)
    
    #list_of_keys  = ['key_1','key_2']
    with st.spinner('Wait for it...'):
        
        chk_primary_keys (df, list_of_keys)
        


            
def main_1 ():
 
    st.markdown(""" <style> #MainMenu {visibility: hidden;} 
                footer {visibility: hidden;}</style> """, 
                unsafe_allow_html=True)
    
    with st.sidebar:
    
        #date = st.date_input ('Select Date Of Incoming')
        #code = st.text_input ('Enter Rm Code')
        #qty = st.text_input ('Enter Qty in kgs' )
        
        
        uploaded_files = st.file_uploader("Choose a CSV file", accept_multiple_files=False, type='csv')
        
        
        '''
        spectra = st.file_uploader("upload file", type={"csv", "txt"})
        if spectra is not None:
            spectra_df = pd.read_csv(spectra)
        st.write(spectra_df)
        '''

        
        st.button ('Press Enter', key='enter',on_click= process , args = [uploaded_files])

    
            
def main ():
    

 
    st.markdown(""" <style> #MainMenu {visibility: hidden;} 
                footer {visibility: hidden;}</style> """, 
                unsafe_allow_html=True)
    
    
    st.header ('FILE REQUIREMENTS')
    st.subheader ('Pls read carefully before using this app')
    st.write ('1) Must be a csv file')
    st.write ('2) Must have exactly 2 columns w/c signifies the primary keys ')
    st.write ('3) Values much have no white space and no null values ')
    st.write ('4) Each Column must have the same number of rows')
    st.write ('5) Format of row values in each column must be of the same format  ')
    st.write ('6) Impt to note that the ff are NOT the same : ')
    
    
    lst = ['a', 'b', 'c']

    for i in lst:
        st.markdown("- " + i)
    

    
    col1, col2,col3,col4 = st.columns(4)
    
    with col1 :
        pass
    with col2:
        st.write ( 'a) W-2 , w2 , w-2  = must be the same asccii value')
        st.write ( 'b) 12  3 , 123 , 1  23  ')
        st.write ( 'c) 123 , 123.00  = must either both be an integer or both be a float ')
    with col3:
        pass
    with col4:
        pass
        
    st.empty ()
 
    
    
    uploaded_files = st.file_uploader("Choose a CSV file", accept_multiple_files=False, type={'csv'} )
    
    if uploaded_files is not None:
        df = pd.read_csv (uploaded_files)
        
        # get col names
        old_col_names = df.columns.values.tolist()
        if len (old_col_names)!=2 :
            # col  should be 2 columns only
            return
        else:
            process_1 (df, old_col_names)
    

    
    #st.button ('Press Enter', key='enter',on_click= process , args = [uploaded_files])

    
    
    
main ()

 