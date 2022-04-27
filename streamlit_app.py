import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Mom\'s New Healthy Diner')

streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

#import pandas
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
try:
  fruit_choise = streamlit.text_input('What fruit you like information about?')
  if not fruit_choise:
    streamlit.error("Please select a fruit to get informatio.")
  else:  
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choise)
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
streamlit.dataframe(fruityvice_normalized)

except URLError as e:
  streamlit.error()
#don't run anything past here while we troubleshoot
streamlit.stop()

#import snowflake.connector
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_rows)

#allow the uses to add a fruit
add_my_fruit = streamlit.text_input('What fruit you like to add?')
streamlit.write('Thanks for adding:', add_my_fruit)

# this will not work correctly, but just go with it for now
my_cur.execute("insert into fruit_load_list values ('from stramlit')")
