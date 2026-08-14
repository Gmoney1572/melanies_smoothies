# Import python packages
import streamlit as st
import requests
from snowflake.snowpark.functions import col
#smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
#st_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

# Write directly to the app
st.title(f"Customize Your Smoothie! :cup_with_straw:")
st.write("""Choose the fruits you want in your custom smoothie!""")

name_on_order = st.text_input('Name on smoothie')
#st.write('The name is:',name_on_order)

cnx=st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    'Chose up to 5 ingredients:'
    , my_dataframe
    , max_selections = 5
)

if ingredients_list:
    ingredients_string = ''

    for fruits_chosen in ingredients_list:
        ingredients_string += fruits_chosen
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
        st_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
        
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
                    values ('""" + ingredients_string + """' ,'""" + name_on_order + """' )"""

   # st.write(my_insert_stmt)
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered ' + name_on_order + '!', icon="✅")




