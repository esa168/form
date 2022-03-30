
import altair as alt
import streamlit as st
import pandas as pd 
import json

alt.data_transformers.disable_max_rows()

hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)


def cust_chart (df_cust):

    highlight = alt.selection(type='single', on='mouseover',
                            fields=['prod_code'], nearest=True)

    #:T
    
    base = alt.Chart(df_cust).encode(
        x='yr',
        y='qty',
        color='prod_code'
    )

    points = base.mark_circle().encode(
        opacity=alt.value(0),
            tooltip = [
                    alt.Tooltip('prod_code'),
                alt.Tooltip('qty'),
                alt.Tooltip ('yr'),
            ]
        
    ).add_selection(
        highlight
    ).properties(
        width=600
    )

    lines = base.mark_line().encode(
        size=alt.condition(~highlight, alt.value(1), alt.value(3))
    )

    chart1 = points + lines
    
    return chart1

def prod_chart3(df_prod):
    
    chart = alt.Chart (df_prod).mark_bar().encode(
        x='yr',
        y='qty',
        tooltip=[alt.Tooltip ('qty'), alt.Tooltip('yr')]
        )
    
    return chart
    
    

def prod_chart2(df_prod):
    
    hover = alt.selection_single (
        fields = ['yr'],
        nearest=True,
        on='mouseover',
        empy='none'   
    )

    lines = (
        alt.Chart(df_prod)
        .mark_line
        .encode (
            x= 'yr:T',
            y= 'qty:Q',
            color = 'prod_code:N')
        )
        
    points = lines.transform_filter(hover).mark_circle(size=65)
    
    tooltips = (
        alt.Chart(df_prod)
        .mark_rule()
        .encode(
            x='yr:T',
            y='qty:Q',
            tooltip = [
                alt.Tooltip('prod_code'),
                alt.Tooltip('qty'),
                ],
        )
        .add_selection(hover)
    )
    
    return (lines+points+tooltips).interactive()

def prod_chart (df_prod):
    
    chart2= alt.Chart(df_prod).mark_line(
                        cornerRadiusTopLeft=3,
                        cornerRadiusTopRight=3,
                        color = 'lightgray',
                        interpolate = 'step-after',
                        line = True
                    ).encode(
                        alt.X('yr'),
                        alt.Y('qty') ,
                        tooltip=[alt.Tooltip ('qty'), alt.Tooltip('yr')]
                        )
    

    return chart2

@st.experimental_memo
def get_data():
    df = pd.read_csv ('sales.csv')
    df['yr']= pd.to_datetime(df['yr'],format='%Y')
    return df

df = get_data()

#! CUSTOMER 
cust_list = df['customer'].to_list()
cust_list = sorted(set(cust_list))
customer = st.selectbox('Select Customer',cust_list)
df_cust = df[df['customer']==customer]
chart = cust_chart(df_cust)
st.altair_chart (chart.interactive(), use_container_width=True)



#! PRODUCT
prod_list = df_cust['prod_code'].to_list()
prod_list = sorted(set(prod_list))
pl = pd.DataFrame(prod_list,columns=['product'])
prod_code = st.selectbox ('Select Product',prod_list)
df_prod= df_cust[df_cust['prod_code']==prod_code]
chart2 = prod_chart3(df_prod)
st.altair_chart (chart2.interactive(), use_container_width=True)
