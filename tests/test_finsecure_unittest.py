import unittest
import os
import sys
import json

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import Utils
from data_manager import DataManager
from audit_logger import AuditLogger
import tempfile

class TestUtils(unittest.TestCase):
    def test_encrypt_decrypt(self):
        original = "secret@example.com"
        encrypted = Utils.encrypt(original)
        decrypted = Utils.decrypt(encrypted)
        self.assertEqual(decrypted, original)
    
    def test_load_json(self):
        with tempfile.NamedTemporaryFile(mode='w+', suffix='.json', delete=False) as f:
            json.dump({"test": "value"}, f)
            f.flush()
            
            data = Utils.load_json(f.name, {})
            self.assertEqual(data["test"], "value")
            
            # Test with non-existent file
            data = Utils.load_json("nonexistent.json", {"default": "value"})
            self.assertEqual(data["default"], "value")
            
        os.unlink(f.name)
    
    def test_save_json(self):
        with tempfile.NamedTemporaryFile(mode='w+', suffix='.json', delete=False) as f:
            f.close()
            
            data = {"test": "value"}
            Utils.save_json(f.name, data)
            
            with open(f.name, 'r') as f_read:
                saved_data = json.load(f_read)
                self.assertEqual(saved_data["test"], "value")
                
        os.unlink(f.name)

class TestDataManager(unittest.TestCase):
    def setUp(self):
        self.cust_file = tempfile.NamedTemporaryFile(mode='w+', suffix='.json', delete=False)
        self.trans_file = tempfile.NamedTemporaryFile(mode='w+', suffix='.json', delete=False)
        self.cred_file = tempfile.NamedTemporaryFile(mode='w+', suffix='.json', delete=False)
        
        json.dump({"1": {"name": "Test Customer", "contact": "test@example.com", "history": []}}, self.cust_file)
        json.dump([{"customer_id": "1", "amount": 100.0}], self.trans_file)
        json.dump({"admin": "YWRtaW4xMjM="}, self.cred_file)
        
        self.cust_file.flush()
        self.trans_file.flush()
        self.cred_file.flush()
        
        self.dm = DataManager(
            customers_file=self.cust_file.name,
            transactions_file=self.trans_file.name,
            credentials_file=self.cred_file.name
        )
    
    
    def tearDown(self):
        for f in [self.cust_file, self.trans_file, self.cred_file]:
            f.close()
            try:
                os.unlink(f.name)
            except:
                pass
    
    def test_initialization(self):
        self.assertEqual(len(self.dm.customers), 1)
        self.assertEqual(len(self.dm.transactions), 1)
        self.assertEqual(len(self.dm.credentials), 1)
    
    def test_save_all(self):
        # Add test data
        self.dm.customers["2"] = {"name": "New Customer", "contact": "new@example.com", "history": []}
        self.dm.transactions.append({"customer_id": "2", "amount": 200.0})
        self.dm.credentials["new_user"] = Utils.encrypt("password")

        self.dm.save_all()

        # Reload data to verify
        self.dm.customers = Utils.load_json(self.cust_file.name, {})
        self.dm.transactions = Utils.load_json(self.trans_file.name, [])
        self.dm.credentials = Utils.load_json(self.cred_file.name, {})
        
        self.assertEqual(len(self.dm.customers), 2)
        self.assertEqual(len(self.dm.transactions), 2)
        self.assertEqual(len(self.dm.credentials), 2)


class TestAuditLogger(unittest.TestCase):
    def setUp(self):
        self.audit_file = tempfile.NamedTemporaryFile(mode='w+', suffix='.json', delete=False)
        json.dump([], self.audit_file)
        self.audit_file.flush()
        self.logger = AuditLogger(audit_file=self.audit_file.name)
    
    def tearDown(self):
        self.audit_file.close()
        try:
            os.unlink(self.audit_file.name)
        except:
            pass
    
    def test_add_log(self):
        initial_count = len(self.logger.log)
        self.logger.add("Test action")
        self.assertEqual(len(self.logger.log), initial_count + 1)
        self.assertEqual(self.logger.log[-1]["action"], "Test action")
    
    def test_save_log(self):
        self.logger.add("Test action")
        self.logger.save()

        # Create new logger with the same audit file path
        new_logger = AuditLogger(audit_file=self.audit_file.name)
        self.assertEqual(len(new_logger.log), 1)
        self.assertEqual(new_logger.log[0]["action"], "Test action")
if __name__ == '__main__':
    unittest.main()