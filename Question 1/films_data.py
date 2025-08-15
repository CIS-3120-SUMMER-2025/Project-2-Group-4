# importing libraries
import requests
import pandas as pd
from bs4 import BeautifulSoup
import json
from urllib.parse import quote
import sqlite3
from dotenv import load_dotenv
import os 

# load the environment variables from the .env file
load_dotenv()
# get the API_key from environment variables
api_key = os.getenv('API_KEY')

url='https://en.wikipedia.org/wiki/List_of_highest-grossing_films'

page = requests.get(url)

films = []
films_information = []
if page.status_code == 200:
  soup = BeautifulSoup(page.text,'html.parser')
  table = soup.find('table', {'class':'wikitable'})
  for row in table.find_all('tr'):
    # get the film titles in <i> tags
    title_cell = row.find('i') # title_cell only shows rows with i tag
    if title_cell and title_cell.a:
      films.append(title_cell.get_text())
  films_df = pd.DataFrame(films, columns = ['Title'],index=range(1,len(films)+1))
 
  for film in films:
    encoded_film = quote(film)
    # endpoint
    url = f'https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={encoded_film}'
    # make a request to the endpoint
    r = requests.get(url).json()
    if r['results']:
      first_result = r['results'][0]
      films_information.append({
        'Title': first_result['title'],
        'Original_title': first_result['original_title'],
        'Release_date': first_result['release_date'],
        'Overview': first_result['overview'],
        'Popularity': first_result['popularity'],
        'Vote_count': first_result['vote_count'],
        'Vote_average': first_result['vote_average'],
    })
    else:
        print(f'No results found for {film}')
  films_information_df = pd.DataFrame(films_information, index=range(1, len(films_information)+1))
  merged_df = pd.merge(films_df, films_information_df, on = 'Title', how = 'right')
  merged_df.to_csv('Top Gross-Profit movies.csv', index = False)
  df = pd.read_csv('Top Gross-Profit movies.csv')
  df.describe()
  db_conn = sqlite3.connect('Movies.db')
  cursor = db_conn.cursor()
  cursor.execute('DROP TABLE IF EXISTS Movies')
  cursor.execute('''
  CREATE TABLE Movies (
    Title TEXT,
    Original_title TEXT,
    Release_date TEXT,
    Overview TEXT,
    Popularity REAL,
    Vote_count INTEGER,
    Vote_average REAL
    )
  ''')
  db_conn.commit()
  merged_df.to_sql('Movies', db_conn, if_exists = 'replace', index=False)
  db_conn.close()
