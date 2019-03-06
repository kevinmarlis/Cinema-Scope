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

current_url = 'http://www.americancinemathequecalendar.com/calendar/' + str(year) + '-' + str(month)
next_url = 'http://www.americancinemathequecalendar.com/calendar/' + str(next_year) + '-' + str(next_month)

def scrape(url):
    response = get(url)
    html_soup = BeautifulSoup(response.text, 'lxml')
    event_containers = html_soup.find_all(class_="view-item view-item-calendar")

    for container in event_containers:
        date = container.parent.parent.get('id')
        date = date[9:]

        dates.append(date)

        title = container.a.text.encode('utf-8')
        titles.append(title)

        link = 'http://www.americancinemathequecalendar.com' + container.find('a').get('href')
        links.append(link)

        time = container.span.text
        times.append(time)

        location = container.find('div', class_="stripe").get('title').replace(' EVENT', ' Theater').replace('Key: ', '')
        locations.append(location)

scrape(current_url)
scrape(next_url)

test_df = pd.DataFrame({'date': dates,
                        'movie': titles,
                        'link': links,
                        'time': times,
                        'location': locations})

test_df = test_df[['date', 'movie', 'location', 'time', 'link']]

print(test_df.info())
print test_df
test_df.to_csv('AC.csv')
