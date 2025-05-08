from utils import Utils
from constants import AUDIT_LOG_FILE
import datetime

class AuditLogger:
    def __init__(self, audit_file=None):
        self.audit_file = audit_file or AUDIT_LOG_FILE
        self.log = Utils.load_json(self.audit_file, [])

    def add(self, action):
        self.log.append({"action": action, "timestamp": str(datetime.datetime.now())})
        self.save()

    def get_log(self):
        return self.log

    def save(self):
        Utils.save_json(self.audit_file, self.log)