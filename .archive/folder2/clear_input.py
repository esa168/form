import streamlit as st

def clear_form():
    st.session_state["foo"] = ""
    st.session_state["bar"] = ""


def ver_1():    
    with st.form("myform"):
        f1, f2 = st.columns([1, 1])
        with f1:
            st.text_input("Foo", key="foo")
        with f2:
            st.text_input("Bar", key="bar")
        f3, f4 = st.columns([1, 1])
        with f3:
            submit = st.form_submit_button(label="Submit")
        with f4:
            clear = st.form_submit_button(label="Clear", on_click=clear_form)

    if submit:
        st.write('Submitted')

    if clear:
        st.write('Cleared')


def ver_2():    
    # regardless of where rhe button is
    # if ind=side side bar or not it clears////
        
    x= st.sidebar.text_input("Foo", key="foo")
    y= st.sidebar.text_input("Bar", key="bar")
    clear = st.button(label="Clear", on_click=clear_form)



    if clear:
        st.write('Cleared')




def main ():
    ver_2()



if __name__ == '__main__':
    main()

