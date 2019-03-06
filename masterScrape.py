import acScrape as ac
import cinespiaScrape as cs
import uclaScrape as us
import newBevScrape as nb
import pandas as pd


master = ac.test_df
master = master.append(cs.test_df).append(us.test_df).append(nb.test_df)

print(master.info())
master.to_csv('master.csv')
