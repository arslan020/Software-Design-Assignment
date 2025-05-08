import pytest
import os
import sys
import json

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import Utils
from data_manager import DataManager
from audit_logger import AuditLogger
import tempfile

# Fixtures for testing
@pytest.fixture
def temp_files():
    # Create temporary files for testing
    with tempfile.NamedTemporaryFile(mode='w+', suffix='.json', delete=False) as cust_file, \
         tempfile.NamedTemporaryFile(mode='w+', suffix='.json', delete=False) as trans_file, \
         tempfile.NamedTemporaryFile(mode='w+', suffix='.json', delete=False) as cred_file, \
         tempfile.NamedTemporaryFile(mode='w+', suffix='.json', delete=False) as audit_file:
        
        # Write initial test data
        json.dump({"1": {"name": "Test Customer", "contact": "test@example.com", "history": []}}, cust_file)
        json.dump([{"customer_id": "1", "amount": 100.0}], trans_file)
        json.dump({"admin": "YWRtaW4xMjM="}, cred_file)
        json.dump([], audit_file)
        
        cust_file.flush()
        trans_file.flush()
        cred_file.flush()
        audit_file.flush()
        
        yield cust_file.name, trans_file.name, cred_file.name, audit_file.name
        
    # Cleanup
    for f in [cust_file.name, trans_file.name, cred_file.name, audit_file.name]:
        try:
            os.unlink(f)
        except:
            pass

def test_utils_encrypt_decrypt():
    original = "test@example.com"
    encrypted = Utils.encrypt(original)
    decrypted = Utils.decrypt(encrypted)
    assert decrypted == original

def test_utils_load_save_json(temp_files):
    cust_file, _, _, _ = temp_files
    data = Utils.load_json(cust_file, {})
    assert "1" in data
    assert data["1"]["name"] == "Test Customer"
    
    # Test save
    data["2"] = {"name": "New Customer"}
    Utils.save_json(cust_file, data)
    new_data = Utils.load_json(cust_file, {})
    assert "2" in new_data

def test_data_manager_initialization(temp_files):
    cust_file, trans_file, cred_file, _ = temp_files
    dm = DataManager(
        customers_file=cust_file,
        transactions_file=trans_file,
        credentials_file=cred_file
    )
    assert len(dm.customers) == 1
    assert len(dm.transactions) == 1
    assert len(dm.credentials) == 1

def test_audit_logger(temp_files):
    _, _, _, audit_file = temp_files
    logger = AuditLogger(audit_file=audit_file)  # Pass the temp file path
    initial_count = len(logger.log)
    
    logger.add("Test action")
    assert len(logger.log) == initial_count + 1
    assert logger.log[-1]["action"] == "Test action"
    
    # Verify persistence
    new_logger = AuditLogger(audit_file=audit_file)
    assert len(new_logger.log) == initial_count + 1