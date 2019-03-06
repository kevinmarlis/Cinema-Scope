import re
from requests import get
from bs4 import BeautifulSoup
import pandas as pd

dates = []
titles = []
links = []
times = []
locations = []

current_url = 'http://cinespia.org'

def scrape(url):
    response = get(url)
    html_soup = BeautifulSoup(response.text, 'lxml')
    event_containers = html_soup.find_all('div', class_ = 'events')
    print len(event_containers)

    if len(event_containers) > 1:
        for container in event_containers:
            #Fix formatting
            date = container.find('ul').find_all('li')[0].text.split(' ', 1)[-1]
            dates.append(date)

            title = container.find('h1').text.encode('utf-8')
            titles.append(title)

            link = container.find('a').get('href')
            links.append(link)

            time = container.find('ul').find_all('li')[2].text.split(' ', 6)[-1]
            times.append(time)

            location = container.find('ul').find_all('li')[1].text
            locations.append(location)

scrape(current_url)

test_df = pd.DataFrame({'date': dates,
                        'movie': titles,
                        'link': links,
                        'time': times,
                        'location': locations})



print(test_df.info())
print test_df
test_df.to_csv('CS.csv')
