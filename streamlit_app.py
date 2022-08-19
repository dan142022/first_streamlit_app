import streamlit
import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My parents New Healthy Diner')

streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗Kale, Spinach & Rocket Smoothie')
streamlit.text('🥚🐔Hard-Boiled Free-Range Egg')
streamlit.text('🍞🥑 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
#import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index))
fruits_to_show = my_fruit_list.loc[fruits_selected]
# Display the table on the page.
if fruits_to_show.empty:
    streamlit.dataframe(my_fruit_list)
else:
    streamlit.dataframe(fruits_to_show)

#New Section to display FRUITYVICE API Response
streamlit.header("Fruityvice Fruit Advice!")
fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('The user entered ', fruit_choice)

#import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+ fruit_choice)


# normalize json stuff
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# display json stuff on screen
streamlit.dataframe(fruityvice_normalized)

#dont run anything past here until we troubleshoot
streamlit.stop()

#import snowflake.connector
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * from fruit_load_list")
#my_data_row = my_cur.fetchone()
#Get all rows
my_data_rows = my_cur.fetchall()
streamlit.header("the fruit load list contains:")
#streamlit.dataframe(my_data_row)
streamlit.dataframe(my_data_rows)

#Allow the user to add a fruit to the list
add_my_fruit = streamlit.text_input('What fruit would you like to add?','')
streamlit.write('Thanks for adding', add_my_fruit)

#it will fail 100%
my_cur.execute("insert into fruit_load_list values ('from streamlit')")
