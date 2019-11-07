from mongoengine import connect
from models.models import coll_company_master,coll_ohlc
import pandas as pd

#Connect to DB 
connect('capitalmarket')

#get symbol from coll_company_master 
company_master =coll_company_master.objects.only('Symbol')

company_list = [i.Symbol for i in coll_company_master.objects] 

#print(company_list)

ohlc = coll_ohlc.objects(Symbol='3MINDIA')[:10]
print(ohlc.to_json())


#Make empty dataframe
df = pd.DataFrame(ohlc.to_json())

print(df.head())
