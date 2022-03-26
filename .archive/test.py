import streamlit as st
import time

menu ={'Get Help':'https://www.cnn.com', 'Report a Bug':'https://www.yahoo.com', 'About':'https://www.googSle.com'}
st.set_page_config(page_title='TITLE', page_icon='random', layout="centered", initial_sidebar_state="auto", menu_items = menu)



@st.cache(suppress_st_warning=True)  # 👈 Changed this
def expensive_computation(a, b):
    # 👇 Added this
    st.write("Cache miss: expensive_computation(", a, ",", b, ") ran")
    time.sleep(2)  # This makes the function take 2s to run
    return a * b


def cache():
    a = 2
    b = 21
    res = expensive_computation(a, b)
    st.write("Result:", res)


def run_click():
    #st.write("run_click routine")
    
    counter = st.session_state['counter']
    
    #st.write (counter+10)
    #time.sleep(5)

def test_state():
    
    counter = 0
    if 'counter' not in st.session_state:
        st.session_state['counter'] = 0
    else:
        st.session_state['counter'] += 1
        
    counter = st.session_state['counter']
    
    st.write(counter)
    
    # after the line below no code is run as it goes to the run click routine 
    # then go back to main; so no point to assign to x 
    # and we cannot pass a var in the run clik function
    # st.session_state is like a global dict
    x= st.button("click me", on_click= run_click)
    
def save_and_exit (dict,x,y):
    dict['cust'].append(x)
    dict['qty'].append(y)
    dict['prod'].append(st.session_state['product'])
    st.session_state['dict'] = dict
    
    dict

def clear_session():
    st.session_state.clear()

def test_saving():
    
    '''
    pass arguments
    session states
    '''
    
    dict ={'cust':[],
           'qty':[],
           'prod':[]}

    if 'dict' not in st.session_state:
        st.session_state['dict'] = dict
    else:
        dict = st.session_state['dict']
        
        
    x= st.text_input ("customer",key="customer")
    y= st.number_input ("quantity",key="quantity") 
    st.selectbox ("product",["MB","DC","OTHERS"],key="product")
    st.button ('save and exit',key="save",on_click=save_and_exit, args=(dict,x,y) )
    st.button ('clear',key="clear",on_click=clear_session)
    

def third_routine(a,b):
    st.write("Result:", a+b)
    return
 
def second_routine(a,b):
    #st.write("Result:", a*b) 
    third_routine(a,b)
    st.date_input("date",key="date")
    return
    

def multip_routine():
    st.header("Multiplication routine")
    
    with st.form('x'):
        
        col1,col2= st.columns(2)
        with col1:
            a = st.number_input("value a",value=0)
        with col2:
            b = st.number_input("value b",value=0)
        x = st.form_submit_button ("multiply")
        if x:
            second_routine(a,b)
       
def agrid(): 
            
    from st_aggrid import AgGrid
    import pandas as pd

    df = pd.read_csv('https://raw.githubusercontent.com/fivethirtyeight/data/master/airline-safety/airline-safety.csv')
    AgGrid(df)
            

            
    


def main():
    st.title("Streamlit App")
    
    #multip_routine()
    
    #test_state()
    #cache()
    
    agrid()
    



if __name__ == "__main__":
    main()
    
    
    
    