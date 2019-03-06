import re
import datetime
from requests import get
from bs4 import BeautifulSoup
import pandas as pd

year = datetime.datetime.now().year
monthDict = {"January":"01", "February":"02", "March":"03", "April":"04", "May":"05", "June":"06", "July":"07",
    "August":"08", "September":"09", "October":"10", "November":"11", "December":"12"}

dates = []
titles = []
links = []
times = []
locations = []

current_url = 'http://thenewbev.com/schedule/'

def scrape(url):
    response = get(url)
    html_soup = BeautifulSoup(response.text, 'lxml')
    event_containers = html_soup.find_all(class_="event-card")

    for container in event_containers:
        for title in container.h4.strings:
            titles.append(title.encode('utf-8').strip().replace("/", ""))
            dates.append(str(year) + "-" + monthDict[container.find(class_="event-card__month").string]
                + "-" + container.find(class_="event-card__numb").string)
            links.append(container.find('a').get('href'))
            locations.append("The New Beverly")

        for time in container.find_all('time'):
            times.append(time.string)

scrape(current_url)

test_df = pd.DataFrame({'date': dates,
                        'movie': titles,
                        'link': links,
                        'time': times,
                        'location': locations})

test_df = test_df[['date', 'movie', 'location', 'time', 'link']]

print(test_df.info())
print test_df
test_df.to_csv('NB.csv')
