import re
import datetime
from requests import get
from bs4 import BeautifulSoup
import pandas as pd

year = datetime.datetime.now().year
month_dict = {'Jan' : '01', 'Feb' : '02', 'Mar' : '03', 'Apr' : '04', 'May' : '05', 'Jun' : '06',
              'Jul' : '07', 'Aug' : '08', 'Sep' : '09', 'Oct' : '10', 'Nov' : '11', 'Dec' : '12'}

dates = []
titles = []
links = []
times = []
locations = []
hosts = []

current_url = 'http://www.lacma.org/events-calendar?tid=68'
next_url = 'http://www.lacma.org/events-calendar?page=0%2C0%2C1&tid=68'

def scrape(url):
    response = get(url)
    html_soup = BeautifulSoup(response.text, 'lxml')
    event_containers = html_soup.find_all('div', class_ = 'events')

    for container in event_containers:
        date = container.find('h4').text.split(', ')[-1].encode('utf-8')
        a = date.split(' ')
        m = month_dict[a[0]]
        d = a[1]
        date = str(year) + '-' + m + '-' + d
        dates.append(date)

        title = container.find('a', class_ = 'title').text.encode('utf-8')
        title = title[6:]
        titles.append(title)

        link = 'http://www.lacma.org/' + container.find('a').get('href').encode('utf-8')
        links.append(link)

        time = container.find('div', class_ = 'details').text.split('|')[0].lstrip().encode('utf-8')
        times.append(time)

        location = container.find('div', class_ = 'details').text.split('|')[-1].encode('utf-8')
        locations.append(location)

scrape(current_url)
scrape(next_url)

test_df = pd.DataFrame({'date': dates,
                        'movie': titles,
                        'time': times,
                        'location': locations,
                        'link': links})

test_df = test_df[['date', 'movie', 'location', 'time', 'link']]

print(test_df.info())
print test_df
test_df.to_csv('LACMA.csv')
