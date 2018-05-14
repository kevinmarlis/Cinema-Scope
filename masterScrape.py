import acScrape as ac
import cinespiaScrape as cs
import independentScrape as id
import lacmaScrape as ls
import uclaScrape as us
import pandas as pd



master = ac.test_df
master = master.append(cs.test_df).append(id.test_df).append(ls.test_df).append(us.test_df)
print master
print(master.info())
master.to_csv('master.csv')
