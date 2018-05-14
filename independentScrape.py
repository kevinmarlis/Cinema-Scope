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
event_containers = []

current_url = 'http://downtownindependent.ning.com/events/event/listByType?type=screening'
next_url = 'http://downtownindependent.ning.com/events/event/listByType?type=screening&page_q=AAAA+AAAACY=&page=2'

def scrape(url):
    response = get(url)
    html_soup = BeautifulSoup(response.text, 'lxml')

    for ultag in html_soup.find_all('ul', {'class': 'clist'}):
        for litag in ultag.find_all('li'):
            event_containers.append(litag)
    print (len(event_containers))
    for event in event_containers:
        title = event.find('h3').a.text.encode('utf-8')
        titles.append(title)
        #FIX FORMATTING
        date = event.find(class_='item_date').a.text.encode('utf-8')
        dates.append(date)

        link = event.find('h3').a.get('href')
        links.append(link)

        time = event.find(class_='item_date').text
        time = time[time.find('from ')+ 5:time.find(' to')]
        times.append(time)

        location = 'Downtown Independent'
        locations.append(location)
    event_containers[:] = []

scrape(current_url)
scrape(next_url)

test_df = pd.DataFrame({'date': dates,
                        'movie': titles,
                        'link': links,
                        'time': times,
                        'location': locations})


print(test_df.info())
print test_df
test_df.to_csv('DTI.csv')
