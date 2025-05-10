# FinSecure Financial Management System

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green)
![License](https://img.shields.io/badge/license-MIT-orange)

A secure financial management system for handling customer data, transactions, and compliance reporting with robust audit logging.

PYTHON_GUI/
├── pytest_cache/ # Pytest cache directory
├── .venv/ # Virtual environment
├── reports/ # Generated reports
│ └── sample_report.csv # Example CSV report
├── tests/ # Test files
│ ├── pycache/
│ ├── init.py
│ ├── test_finsecure_pytest.py # Pytest tests
│ ├── test_finsecure_unittest.py # Unittest tests
│ ├── app.py # Test instance of app
│ ├── audit_log.json # Test audit logs
│ ├── audit_logger.py # Audit logger tests
│ ├── constants.py # Test constants
│ ├── credentials.json # Test credentials
│ ├── customers.json # Test customer data
│ ├── dashboard_data.json # Test dashboard data
│ ├── data_manager.py # Data manager tests
│ ├── diagram.xml # Architecture diagram
│ ├── main.py # Test entry point
│ ├── transactions.json # Test transactions
│ └── utils.py # Utility tests
├── app.py # Main application GUI
├── audit_log.json # Production audit logs
├── audit_logger.py # Audit logging system
├── constants.py # Path constants
├── credentials.json # User credentials (encrypted)
├── customers.json # Customer database
├── dashboard_data.json # Dashboard analytics data
├── data_manager.py # Data handling core
├── main.py # Entry point (login system)
├── transactions.json # Transaction records
└── utils.py # Encryption/helper functions



## Key Features

- 🔒 **Role-Based Access Control** (Admin/Staff)
- 📊 **Real-Time Transaction Monitoring** (Alerts for >$10k transactions)
- 📝 **Immutable Audit Logging** (All actions timestamped)
- 🔐 **Data Encryption** (Base64 for sensitive fields)
- 📈 **Interactive Dashboards** (Matplotlib visualizations)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/arslan020/Software-Design-Assignment.git
   cd finsecure

2. Set up a virtual environment:
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.\.venv\Scripts\activate   # Windows

3. Install dependencies: 
    - pip install matplotlib  


4. Usage
Start the application:

    - python main.py  (Run this is vs code)

    Login credentials:

        - Admin: admin / admin123

5. Testing
    Run all tests:
    - python -m pytest tests/ -v