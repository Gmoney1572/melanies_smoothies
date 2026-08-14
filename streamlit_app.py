# Import python packages
import streamlit as st
import requests
import pandas as pd
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f"Customize Your Smoothie! :cup_with_straw:")
st.write("""Choose the fruits you want in your custom smoothie!""")

name_on_order = st.text_input('Name on smoothie')
#st.write('The name is:',name_on_order)

cnx=st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'),col('search_on'))
#st.dataframe(data=my_dataframe, use_container_width=True)

#convert the dataframe to a pandas dataframe
pd_df = my_dataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop()

ingredients_list = st.multiselect(
    'Chose up to 5 ingredients:'
    , pd_df['fruit_name']
    , max_selections = 5
)

if ingredients_list:
    ingredients_string = ''

    for fruits_chosen in ingredients_list:
        ingredients_string += fruits_chosen
        
        search_on=pd_df.loc[pd_df['fruit_name'] == fruits_chosen, 'search_on'].iloc[0]
        
        st.subheader(fruits_chosen + ' Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/"+fruits_chosen)
        st_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
        
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
                    values ('""" + ingredients_string + """' ,'""" + name_on_order + """' )"""

   # st.write(my_insert_stmt)
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered ' + name_on_order + '!', icon="✅")




