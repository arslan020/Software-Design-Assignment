from utils import Utils
from constants import CUSTOMERS_FILE, TRANSACTIONS_FILE, CREDENTIALS_FILE, DASHBOARD_FILE

class DataManager:
    def __init__(self, customers_file=None, transactions_file=None, credentials_file=None):
        self.customers_file = customers_file or CUSTOMERS_FILE
        self.transactions_file = transactions_file or TRANSACTIONS_FILE
        self.credentials_file = credentials_file or CREDENTIALS_FILE
        
        self.customers = Utils.load_json(self.customers_file, {})
        self.transactions = Utils.load_json(self.transactions_file, [])
        self.credentials = Utils.load_json(self.credentials_file, {})
        
        for cid in self.customers:
            self.customers[cid].setdefault("history", [])

    def save_all(self):
        Utils.save_json(self.customers_file, self.customers)
        Utils.save_json(self.transactions_file, self.transactions)
        Utils.save_json(self.credentials_file, self.credentials)

    def save_dashboard(self):
        Utils.save_json(DASHBOARD_FILE, self.transactions)