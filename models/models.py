import mongoengine 
import datetime

class coll_company_master(mongoengine.DynamicDocument):
    Industry = mongoengine.StringField()
    Symbol = mongoengine.StringField()
    ISIN_1 = mongoengine.StringField()
    Series = mongoengine.StringField()
    Company_1 = mongoengine.StringField()
    #meta = {"allow_inheritance":True}
  
class coll_ohlc(mongoengine.DynamicDocument):
    Volume  = mongoengine.LongField()            
    Last    = mongoengine.FloatField()
    Deliverable = mongoengine.FloatField()
    Turnover = mongoengine.LongField()
    Trades   = mongoengine.LongField()
    Low      = mongoengine.FloatField()  
    Open     = mongoengine.FloatField()
    Symbol   = mongoengine.StringField()
    Date     = mongoengine.DateField()
    Close    = mongoengine.FloatField()
    PercDeliverable = mongoengine.FloatField()
    VWAP = mongoengine.FloatField()
    High = mongoengine.FloatField()
    Series = mongoengine.StringField()
    PrevClose = mongoengine.FloatField()
    is_marubozu = mongoengine.StringField()
    daily_change_percent = mongoengine.FloatField()
    change_percent = mongoengine.FloatField()
    