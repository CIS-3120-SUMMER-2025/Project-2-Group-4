#import libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3

sports_teams = {

    'mens_volleyball' : ['https://ccnyathletics.com/sports/mens-volleyball/roster?view=2',
                         'https://lehmanathletics.com/sports/mens-volleyball/roster?view=2',
                         'https://www.brooklyncollegeathletics.com/sports/mens-volleyball/roster?view=2',
                         'https://johnjayathletics.com/sports/mens-volleyball/roster?view=2',
                         'https://athletics.baruch.cuny.edu/sports/mens-volleyball/roster?view=2',
                         'https://mecathletics.com/sports/mens-volleyball/roster/2024?view=2',
                         'https://www.huntercollegeathletics.com/sports/mens-volleyball/roster/2024?view=2',
                         'https://yorkathletics.com/sports/mens-volleyball/roster'],

    'mens_swimming' : ['https://csidolphins.com/sports/mens-swimming-and-diving/roster/2023-2024?view=2',
                       'https://yorkathletics.com/sports/mens-swimming-and-diving/roster',
                       'https://athletics.baruch.cuny.edu/sports/mens-swimming-and-diving/roster',
                       'https://www.brooklyncollegeathletics.com/sports/mens-swimming-and-diving/roster/2022-23?view=2',
                       'https://lindenwoodlions.com/sports/mens-swimming-and-diving/roster/2021-22?view=2',
                       'https://mckbearcats.com/sports/mens-swimming-and-diving/roster/2023-24?view=2',
                       'https://ramapoathletics.com/sports/mens-swimming-and-diving/roster',
                       'https://oneontaathletics.com/sports/mens-swimming-and-diving/roster?view=2',
                       'https://binghamtonbearcats.com/sports/mens-swimming-and-diving/roster/2021-22?view=2',
                       'https://albrightathletics.com/sports/mens-swimming-and-diving/roster/2020-21?view=2'],

    'womens_volleyball' : ['https://bmccathletics.com/sports/womens-volleyball/roster/2022?view=2',
                           'https://yorkathletics.com/sports/womens-volleyball/roster',
                           'https://hostosathletics.com/sports/womens-volleyball/roster/2022-2023?view=2',
                           'https://bronxbroncos.com/sports/womens-volleyball/roster/2023?view=2',
                           'https://queensknights.com/sports/womens-volleyball/roster?view=2',
                           'https://augustajags.com/sports/wvball/roster?view=2',
                           'https://flaglerathletics.com/sports/womens-volleyball/roster?view=2',
                           'https://pacersports.com/sports/womens-volleyball/roster',
                           'https://www.lockhavenathletics.com/sports/womens-volleyball/roster/2024?view=2'],

    'womens_swimming' : ['https://csidolphins.com/sports/womens-swimming-and-diving/roster/2023-2024?view=2',
                         'https://queensknights.com/sports/womens-swimming-and-diving/roster/2019-20',
                         'https://yorkathletics.com/sports/womens-swimming-and-diving/roster/2019-20',
                         'https://athletics.baruch.cuny.edu/sports/womens-swimming-and-diving/roster/2021-22?view=2',
                         'https://www.brooklyncollegeathletics.com/sports/womens-swimming-and-diving/roster/2022-23?view=2',
                         'https://lindenwoodlions.com/sports/womens-swimming-and-diving/roster/2021-22?view=2',
                         'https://mckbearcats.com/sports/womens-swimming-and-diving/roster?view=2',
                         'https://ramapoathletics.com/sports/womens-swimming-and-diving/roster?view=2',
                         'https://keanathletics.com/sports/womens-swimming-and-diving/roster?view=2',
                         'https://oneontaathletics.com/sports/womens-swimming-and-diving/roster/2021-22?view=2']
    }

"""Men's Sports Teams comparsion"""

sports_teams['mens_volleyball']

sports_teams['mens_swimming']

def average_height(url_list):

  # list to store heights and names
  heights = []
  names = []

  # visit each url in the list
  for url in url_list:

    # headers Source: https://www.zenrows.com/blog/web-scraping-headers#user-agent
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
      'Accept-Language': 'en-US,en;q=0.9',
      'Connection': 'keep-alive'
      }

    # making a request to the server
    page = requests.get(url, headers = headers)

    # scrape data only if connection is successful
    if page.status_code == 200:
      # import the raw html into BeautifulSoup
      soup = BeautifulSoup(page.content, 'html.parser')

      # find all td tags with a class of height
      raw_heights = soup.find_all('td', class_ = 'height')

      # find all td tags with a class of sidearm-table-player-name
      name_tags = soup.find_all('td', class_ = 'sidearm-table-player-name')

      # extracting the name from the name tags
      for name_tag in name_tags:
        names.append((name_tag.text).strip())

      # extract the raw height from the list
      for raw_height in raw_heights:
        x = raw_height.get_text()
        # splitting the string by the '-'
        feet = float(x.split('-')[0]) * 12
        inches = float(x.split('-')[1])

        # converting height to inches
        height_inches = feet + inches
        heights.append(height_inches)


  # organized the data as a dictionary
  data = {
      'Name': names,
      'Height': heights
  }

  df = pd.DataFrame(data)
  return df

"""Question 1"""

# DATAFRAME FOR MENS SWIMMING TEAM

mens_swim_df = average_height(sports_teams['mens_swimming'])
mens_swim_df

mens_swim_df.to_csv('Men\'s swimming teams.csv', index = False)

"""Question 2"""

# DATAFRAME FOR WOMENS SWIMMING TEAM

womens_swim_df = average_height(sports_teams['womens_swimming'])
womens_swim_df

womens_swim_df.to_csv('Women\'s swimming teams.csv', index = False)

"""Question 3"""

# DATAFRAME FOR MENS VOLLEYBALL TEAM

mens_volleyball_df = average_height(sports_teams['mens_volleyball'])
mens_volleyball_df

mens_volleyball_df.to_csv('Men\'s volleyball teams.csv', index = False)

"""Question 4"""

# DATAFRAME FOR WOMENS VOLLEYBALL TEAM

womens_volleyball_df = average_height(sports_teams['womens_volleyball'])
womens_volleyball_df

womens_volleyball_df.to_csv('Women\'s volleyball teams.csv', index = False)

"""Question 5"""

mens_swim_avg = mens_swim_df['Height'].mean()
print(f'The average height of the mens swim team is {mens_swim_avg}')
print()

womens_swim_avg = womens_swim_df['Height'].mean()
print(f'The average height of the womens swim team is {womens_swim_avg}')
print()

mens_volleyball_avg = mens_volleyball_df['Height'].mean()
print(f'The average height of the mens volleyball team is {mens_volleyball_avg}')
print()

womens_volleyball_avg = womens_volleyball_df['Height'].mean()
print(f'The average height of the womens volleyball team is {womens_volleyball_avg}')
print()

"""Question 6"""

# tallest man volleyball players

top_heights = mens_volleyball_df['Height'].nlargest(5).unique()
fifth_height = top_heights[-1]

# filter the dataframe to include all athletes with height >=fifth height
mens_volleyball_df[mens_volleyball_df['Height'] >= fifth_height]

# shortest man volleyball players

shortest_heights = mens_volleyball_df['Height'].nsmallest(5).unique()
fifth_height = shortest_heights[-1]

# filter the dataframe to include all athletes with height <= fifth height
mens_volleyball_df[mens_volleyball_df['Height'] <= fifth_height]

# tallest women volleyball players

top_heights = womens_volleyball_df['Height'].nlargest(5).unique()
fifth_height = top_heights[-1]

# filter the dataframe to include all athletes with height >=fifth height
womens_volleyball_df[womens_volleyball_df['Height'] >= fifth_height]

# shortest women volleyball players

shortest_heights = womens_volleyball_df['Height'].nsmallest(5).unique()
fifth_height = shortest_heights[-1]

# filter the dataframe to include all athletes with height <= fifth height
womens_volleyball_df[womens_volleyball_df['Height'] <= fifth_height]

# tallest man swimmers

top_heights = mens_swim_df['Height'].nlargest(5).unique()
fifth_height = top_heights[-1]

# filter the dataframe to include all athletes with height >=fifth height
mens_swim_df[mens_swim_df['Height'] >= fifth_height]

# shortest man swimmers

top_heights = mens_swim_df['Height'].nsmallest(5).unique()
fifth_height = top_heights[-1]

# filter the dataframe to include all athletes with height >=fifth height
mens_swim_df[mens_swim_df['Height'] <= fifth_height]

# tallest women swimmers

top_heights = womens_swim_df['Height'].nlargest(5).unique()
fifth_height = top_heights[-1]

# filter the dataframe to include all athletes with height >=fifth height
womens_swim_df[womens_swim_df['Height'] >= fifth_height]

# shortest women swimmers

shortest_heights = womens_swim_df['Height'].nsmallest(5).unique()
fifth_height = shortest_heights[-1]

# filter the dataframe to include all athletes with height <= fifth height
womens_swim_df[womens_swim_df['Height'] <= fifth_height]

"""Question 7"""

mens_volleyball_df.describe()

mens_swim_df.describe()

womens_volleyball_df.describe()

womens_swim_df.describe()

# Generate a pandas dataframe that has two columns: Team, Avg Height
mens_avg_data = {
    'Team' : ['Mens Volleyball Team', 'Mens Swimming Team'],
    'Avg Height' : [mens_volleyball_avg, mens_swim_avg]
}

mens_avg_data_df = pd.DataFrame(mens_avg_data)
mens_avg_data_df

# Generate a pandas dataframe that has two columns: Team, Avg Height
womens_avg_data = {
    'Team' : ['Womens Volleyball Team', 'Womens Swimming Team'],
    'Avg Height' : [womens_volleyball_avg, womens_swim_avg]
}

womens_avg_data_df = pd.DataFrame(womens_avg_data)
womens_avg_data_df

ax = mens_avg_data_df.plot.bar(x = 'Team', y = 'Avg Height', title = 'Average Heights Among Athletes')
# Loop through bars to annotate values
for bars in ax.containers:
  ax.bar_label(bars)
plt.show()

ax = womens_avg_data_df.plot.bar(x = 'Team', y = 'Avg Height', title = 'Average Heights Among Athletes')
for bars in ax.containers:
  ax.bar_label(bars)
plt.show()

db_conn = sqlite3.connect('sports_teams.db')

cursor = db_conn.cursor()

cursor.execute('''
  CREATE TABLE Althetes (
    name TEXT,
    height REAL
  )
''')
db_conn.commit()

# add mens_volleyball_df to sql
mens_volleyball_df.to_sql('Players', db_conn, if_exists='replace', index=False)

# add mens_swim_df to sql
mens_swim_df.to_sql('Players', db_conn, if_exists='append', index=False)

# add womens_volleyball_df to sql
womens_volleyball_df.to_sql('Players', db_conn, if_exists='append', index=False)

# add womens_swim_df to sql
womens_swim_df.to_sql('Players', db_conn, if_exists='append', index=False)

db_conn.commit()
db_conn.close()
