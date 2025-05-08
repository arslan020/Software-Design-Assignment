from utils import Utils
from constants import CUSTOMERS_FILE, TRANSACTIONS_FILE, CREDENTIALS_FILE, DASHBOARD_FILE

class DataManager:
    def __init__(self):
        self.customers = Utils.load_json(CUSTOMERS_FILE, {})
        self.transactions = Utils.load_json(TRANSACTIONS_FILE, [])
        self.credentials = Utils.load_json(CREDENTIALS_FILE, {})
        for cid in self.customers:
            self.customers[cid].setdefault("history", [])

    def save_all(self):
        Utils.save_json(CUSTOMERS_FILE, self.customers)
        Utils.save_json(TRANSACTIONS_FILE, self.transactions)
        Utils.save_json(CREDENTIALS_FILE, self.credentials)

    def save_dashboard(self):
        Utils.save_json(DASHBOARD_FILE, self.transactions)
