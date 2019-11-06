from mongoengine import connect
from models.models import coll_company_master,coll_ohlc

#Connect to DB 
connect('capitalmarket')

#get symbol from coll_company_master 
company_master =coll_company_master.objects.only('Symbol')

company_list = [i.Symbol for i in coll_company_master.objects] 

ohlc = coll_ohlc.objects.only('change_percent').first()

print(ohlc.change_percent)


