import re
import datetime
from requests import get
from bs4 import BeautifulSoup
import pandas as pd

year = datetime.datetime.now().year
month = datetime.datetime.now().month
if month == 12:
    next_year = year + 1
    next_month = 01
else:
    next_year = year
    next_month = month + 1

dates = []
titles = []
links = []
times = []
locations = []

current_url = 'https://www.cinema.ucla.edu/calendar/' + str(year) + '-' + str(month)
next_url = 'https://www.cinema.ucla.edu/calendar/' + str(next_year) + '-' + str(next_month)

def scrape(url):
    response = get(url)
    html_soup = BeautifulSoup(response.text, 'lxml')
    event_containers = html_soup.find_all(class_="calendar monthview")


    for container in event_containers:
        title = container.find('a').text.encode('utf-8').replace("\xc2\xa0", " ")
        if ('Off-Site Event' in title):
            continue
        titles.append(title)

        date = container.parent.parent.parent.parent.get('data-date')
        dates.append(date)

        link = 'https://www.cinema.ucla.edu' + container.find('a').get('href')
        links.append(link)

        time = container.span.text
        times.append(time)

        location = 'Billy Wilder Theater'
        locations.append(location)

scrape(current_url)
scrape(next_url)
test_df = pd.DataFrame({'date': dates,
                        'movie': titles,
                        'link': links,
                        'time': times,
                        'location': locations})


print(test_df.info())
print test_df
test_df.to_csv('UCLA.csv')
