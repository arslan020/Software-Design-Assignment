from utils import Utils
from constants import AUDIT_LOG_FILE
import datetime

class AuditLogger:
    def __init__(self):
        self.log = Utils.load_json(AUDIT_LOG_FILE, [])

    def add(self, action):
        self.log.append({"action": action, "timestamp": str(datetime.datetime.now())})
        Utils.save_json(AUDIT_LOG_FILE, self.log)

    def get_log(self):
        return self.log
