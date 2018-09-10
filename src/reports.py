import pymongo
from datetime import datetime, timedelta, date
import pandas as pd

host = "localhost"
port = 27017

db = pymongo.MongoClient(host, port)


def transaction_logger(money_record):
    for record in money_record:
        db["Bank"]["Transactions"].update_one(
            {"MessageID": record["MessageID"]},
            {"$set": record},
            upsert=True)


class Budget:
    def __init__(self, availablefunds):
        self.transactiondb = db["Bank"]["Transactions"]
        self.initalamt = availablefunds
        self.current_time = datetime.now()

    def breakdown(self, freq, group):
        if freq == "year":
            q = self.get_year()
        elif freq == "month":
            q = self.get_month()
        elif freq == "week":
            q = self.get_week()
        df = self.cursor_to_df(q)
        days = df.groupby(pd.Grouper(freq=group))
        return days

    def cursor_to_df(self, cursor):
        df = pd.DataFrame(list(cursor)).set_index("TransactionDate")
        return df

    def get_spend(self, starttime, endtime):
        bank_transactions = self.transactiondb
        cum_weekly = bank_transactions.find(
            {"TransactionDate": {"$gte": starttime,
                                 "$lte": endtime}})
        return cum_weekly

    def get_week(self):
        start, end = self.cumulative_week()
        spend = self.get_spend(start, end)
        return spend

    def get_month(self):
        start, end = self.cumulative_month()
        spend = self.get_spend(start, end)
        return spend

    def get_year(self):
        start, end = self.cumulative_year()
        spend = self.get_spend(start, end)
        return spend

    def cumulative_week(self):
        endtime = self.current_time
        starttime = endtime - timedelta(days=endtime.weekday())
        return starttime, endtime

    def cumulative_month(self):
        endtime = self.current_time
        m = endtime.month
        y = endtime.year
        starttime = datetime.combine(date(y, m, 1), datetime.min.time())
        return starttime, endtime

    def cumulative_year(self):
        endtime = self.current_time
        y = endtime.year
        starttime = datetime.combine(date(y, 1, 1), datetime.min.time())
        return starttime, endtime
