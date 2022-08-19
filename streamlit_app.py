import streamlit

streamlit.title('My parents New Healthy Diner')

streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗Kale, Spinach & Rocket Smoothie')
streamlit.text('🥚🐔Hard-Boiled Free-Range Egg')
streamlit.text('🍞🥑 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
import pandas
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

import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/{fruits_to_show}")
print (fruityvice_response)
streamlit.text(fruityvice_response.json())

# normalize json stuff
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# display json stuff on screen
streamlit.dataframe(fruityvice_normalized)
