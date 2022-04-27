import streamlit

streamlit.title('My Mom\'s New Healthy Diner')

streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

import pandas
my_fruit_lits = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_lits = my_fruit_lits.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_lits.index),['Avocado', 'Strawberries'])

# If you want to know more about pandas.dataframe.loc[ ], you find more information here: 
# https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.loc.html 
fruits_to_show = my_fruit_lits.loc[fruits_selected]

# display the table on the page
streamlit.dataframe(fruits_to_show)

# New Section to display fruitvice api response
streamlit.header('Fruityvice Fruit Advice!')
fruit_choise = streamlit.text_input('What fruit you like information about?', 'kiwi')
streamlit.write('The user entered', fruit_choise)

import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choise)
#streamlit.text(fruityvice_response.json()) # just writes the data to the screen

# Take the json version fo the response an normalize it
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# Output it the screen as a table
streamlit.dataframe(fruityvice_normalized)

import snowflake.connector
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from fruit_load_list")
my_data_row = my_cur.fetchone()
streamlit.text("The fruit load list contains:")
streamlit.text(my_data_row)
