import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import os
import csv
import datetime
import matplotlib.pyplot as plt
from utils import Utils
from constants import REPORTS_DIR
from tkinter import font as tkfont
import uuid

class FinSecureApp:
    def __init__(self, root, role, data_manager, logger, username=None):
        self.root = root
        self.role = role
        self.data = data_manager
        self.logger = logger
        self.username = username

        # Initialize ttk Style
        self.style = ttk.Style()

        # Modern styling configuration
        self.bg_color = "#2c3e50"
        self.card_bg = "#34495e"
        self.fg_color = "#ecf0f1"
        self.accent_color = "#3498db"
        self.success_color = "#2ecc71"
        self.warning_color = "#e74c3c"
        self.highlight_color = "#2980b9"
        self.chart_color = "#3498db"
        self.chart_edge = "#ecf0f1"
      
        # Configure styles
        self.style.configure('TFrame', background=self.bg_color)
        self.style.configure('TLabel', background=self.bg_color, foreground=self.fg_color, 
                           font=('Helvetica', 10))
        self.style.configure('Blue.TButton', background='#3498db',  foreground='white',  font=('Helvetica', 10, 'bold'), padding=8, borderwidth=1)

        self.style.map('Blue.TButton', background=[('active', '#2980b9')], foreground=[('active', '#ecf0f1')])
        
        self.style.configure('Card.TFrame', background=self.card_bg, relief=tk.RAISED, borderwidth=2)
        self.style.configure('CardHeader.TLabel', background=self.card_bg, foreground=self.fg_color,
                           font=('Helvetica', 12, 'bold'))
        self.style.configure('Stat.TLabel', background=self.card_bg, foreground=self.fg_color,
                           font=('Helvetica', 14))
        self.style.configure('Header.TLabel', font=('Helvetica', 18, 'bold'))
        
        # Main window configuration
        self.root.title(f"FinSecure Dashboard ({role.capitalize()})")
        self.root.geometry("1000x700")
        self.root.configure(bg=self.bg_color)
        self.root.minsize(900, 600)
        
        # Header frame
        self.header_frame = ttk.Frame(self.root, style='Card.TFrame')
        self.header_frame.pack(fill=tk.X, padx=20, pady=20)
        
        ttk.Label(self.header_frame, text=f"FinSecure {role.capitalize()} Dashboard", 
                 style='Header.TLabel').pack(side=tk.LEFT, padx=10, pady=10)
        
        # Add logout button
        ttk.Button(self.header_frame, text="Logout", command=self.root.quit,
                  style='TButton').pack(side=tk.RIGHT, padx=10)
        
        if role == "admin":
            self.load_admin_dashboard()
        else:
            self.load_staff_dashboard()

    def load_admin_dashboard(self):
        # Main content frame
        content_frame = ttk.Frame(self.root)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # Stats cards row
        stats_frame = ttk.Frame(content_frame)
        stats_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Card 1: Total Customers
        card1 = ttk.Frame(stats_frame, style='Card.TFrame')
        card1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        ttk.Label(card1, text="TOTAL CUSTOMERS", style='CardHeader.TLabel').pack(pady=(10, 5))
        ttk.Label(card1, text=str(len(self.data.customers)), style='Stat.TLabel').pack(pady=(0, 10))
        
        # Card 2: Total Transactions
        card2 = ttk.Frame(stats_frame, style='Card.TFrame')
        card2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        ttk.Label(card2, text="TOTAL TRANSACTIONS", style='CardHeader.TLabel').pack(pady=(10, 5))
        ttk.Label(card2, text=str(len(self.data.transactions)), style='Stat.TLabel').pack(pady=(0, 10))
        
        # Card 3: Total Volume
        card3 = ttk.Frame(stats_frame, style='Card.TFrame')
        card3.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        ttk.Label(card3, text="TOTAL VOLUME", style='CardHeader.TLabel').pack(pady=(10, 5))
        total_amount = sum(txn["amount"] for txn in self.data.transactions)
        ttk.Label(card3, text=f"${total_amount:,.2f}", style='Stat.TLabel').pack(pady=(0, 10))
        
        # Card 4: Suspicious Activity
        card4 = ttk.Frame(stats_frame, style='Card.TFrame')
        card4.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        ttk.Label(card4, text="SUSPICIOUS TXNS", style='CardHeader.TLabel').pack(pady=(10, 5))
        suspicious = len([txn for txn in self.data.transactions if txn["amount"] > 10000])
        ttk.Label(card4, text=str(suspicious), style='Stat.TLabel').pack(pady=(0, 10))
        
        # Charts and actions row
        bottom_frame = ttk.Frame(content_frame)
        bottom_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left panel - Chart
        chart_frame = ttk.Frame(bottom_frame, style='Card.TFrame')
        chart_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        ttk.Label(chart_frame, text="TRANSACTION DISTRIBUTION", style='CardHeader.TLabel').pack(pady=10)
        
        amounts = [txn["amount"] for txn in self.data.transactions]
        if amounts:
            fig, ax = plt.subplots(figsize=(6, 4), facecolor=self.card_bg)
            ax.set_facecolor(self.card_bg)
            
            # Customize plot
            bars = ax.hist(amounts, bins=10, color=self.chart_color, edgecolor=self.chart_edge)
            ax.set_title("Transaction Amount Distribution", color=self.fg_color)
            ax.set_xlabel("Amount ($)", color=self.fg_color)
            ax.set_ylabel("Frequency", color=self.fg_color)
            
            # Customize ticks and spines
            ax.tick_params(colors=self.fg_color)
            for spine in ax.spines.values():
                spine.set_color('#7f8c8d')
            
            from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
            canvas = FigureCanvasTkAgg(fig, master=chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        else:
            ttk.Label(chart_frame, text="No transactions to visualize").pack()
        
        # Right panel - Actions
        action_frame = ttk.Frame(bottom_frame, style='Card.TFrame')
        action_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=False, padx=(10, 0), ipadx=10)
        ttk.Label(action_frame, text="ADMIN ACTIONS", style='CardHeader.TLabel').pack(pady=10)
        
        actions = [
            ("➕ Add Customer", self.add_customer),
            ("👥 View Customers", self.view_customers),
            ("📊 Generate Report", self.generate_report),
            ("📝 Audit Logs", self.view_audit),
            ("💳 Add Transaction", self.add_transaction),
            # ("📈 View Dashboard", self.view_dashboard)
        ]
        
        for text, command in actions:
            btn = ttk.Button(action_frame, text=text, command=command, style='TButton')
            btn.pack(fill=tk.X, padx=10, pady=5)
    def load_staff_dashboard(self):
    # Main content frame
        content_frame = ttk.Frame(self.root)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # Filter transactions for this user only
        user_txns = [txn for txn in self.data.transactions if txn.get("staff_username") == self.username]
        
        # Stats cards row
        stats_frame = ttk.Frame(content_frame)
        stats_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Card 1: Total Transactions
        card1 = ttk.Frame(stats_frame, style='Card.TFrame')
        card1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        ttk.Label(card1, text="YOUR TRANSACTIONS", style='CardHeader.TLabel').pack(pady=(10, 5))
        ttk.Label(card1, text=str(len(user_txns)), style='Stat.TLabel').pack(pady=(0, 10))
        
        # Card 2: Total Volume
        card2 = ttk.Frame(stats_frame, style='Card.TFrame')
        card2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        ttk.Label(card2, text="YOUR VOLUME", style='CardHeader.TLabel').pack(pady=(10, 5))
        user_amount = sum(txn["amount"] for txn in user_txns)
        ttk.Label(card2, text=f"${user_amount:,.2f}", style='Stat.TLabel').pack(pady=(0, 10))
        
        # Card 3: Recent Activity
        card3 = ttk.Frame(stats_frame, style='Card.TFrame')
        card3.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        ttk.Label(card3, text="RECENT ACTIVITY", style='CardHeader.TLabel').pack(pady=(10, 5))
        recent = len(user_txns[-5:]) if user_txns else 0
        ttk.Label(card3, text=f"{recent}/5", style='Stat.TLabel').pack(pady=(0, 10))
        
        # Charts and actions row
        bottom_frame = ttk.Frame(content_frame)
        bottom_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left panel - Chart (using filtered transactions)
        chart_frame = ttk.Frame(bottom_frame, style='Card.TFrame')
        chart_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        ttk.Label(chart_frame, text="YOUR TRANSACTIONS", style='CardHeader.TLabel').pack(pady=10)
        
        amounts = [txn["amount"] for txn in user_txns]
        if amounts:
            fig, ax = plt.subplots(figsize=(6, 4), facecolor=self.card_bg)
            ax.set_facecolor(self.card_bg)
            
            # Pie chart for staff view
            amounts_pos = [amt for amt in amounts if amt >= 0]
            amounts_neg = [abs(amt) for amt in amounts if amt < 0]
            labels = ['Credits', 'Debits'] if amounts_neg else ['Transactions']
            sizes = [sum(amounts_pos), sum(amounts_neg)] if amounts_neg else [sum(amounts_pos)]
            colors = [self.success_color, self.warning_color] if amounts_neg else [self.chart_color]
            
            ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
                textprops={'color': self.fg_color}, wedgeprops={'edgecolor': self.chart_edge})
            ax.set_title("Your Transaction Breakdown", color=self.fg_color)
            
            from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
            canvas = FigureCanvasTkAgg(fig, master=chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        else:
            ttk.Label(chart_frame, text="No transactions to visualize").pack()
        
        # Right panel - Actions
        action_frame = ttk.Frame(bottom_frame, style='Card.TFrame')
        action_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=False, padx=(10, 0), ipadx=10)
        ttk.Label(action_frame, text="QUICK ACTIONS", style='CardHeader.TLabel').pack(pady=10)
        
        actions = [
            ("💳 Add Transaction", self.add_transaction),
            ("✏️ Edit Transaction", self.edit_transaction),
            ("🗑️ Delete Transaction", self.delete_transaction),
            ("📋 My Transactions", self.view_my_transactions)
        ]
        
        for text, command in actions:
            btn = ttk.Button(action_frame, text=text, command=command, style='TButton')
            btn.pack(fill=tk.X, padx=10, pady=5)
    def add_customer(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Customer")
        dialog.geometry("400x400")
        dialog.configure(bg=self.bg_color)
        dialog.resizable(False, False)
        
        # Header
        ttk.Label(dialog, text="Add New Customer", style='Header.TLabel').pack(pady=15)
        
        # Form frame
        form_frame = ttk.Frame(dialog)
        form_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
        
        # Form fields with consistent styling
        fields = [
            ("Full Name", "text"),
            ("Contact Info", "text"),
            ("Create Staff Account", "checkbox")
        ]
        
        entries = {}
        for i, (label, field_type) in enumerate(fields):
            ttk.Label(form_frame, text=label+":").grid(row=i, column=0, padx=5, pady=5, sticky='e')
            
            if field_type == "checkbox":
                create_staff_var = tk.BooleanVar()
                checkbox = ttk.Checkbutton(form_frame, variable=create_staff_var)
                checkbox.grid(row=i, column=1, padx=5, pady=5, sticky='w')
                entries[label] = create_staff_var
            else:
                entry = ttk.Entry(form_frame)
                entry.grid(row=i, column=1, padx=5, pady=5, sticky='ew')
                entries[label] = entry
        
        # Add username/password fields when creating staff account
        ttk.Label(form_frame, text="Username:").grid(row=3, column=0, padx=5, pady=5, sticky='e')
        username_entry = ttk.Entry(form_frame)
        username_entry.grid(row=3, column=1, padx=5, pady=5, sticky='ew')
        
        ttk.Label(form_frame, text="Password:").grid(row=4, column=0, padx=5, pady=5, sticky='e')
        password_entry = ttk.Entry(form_frame, show="*")
        password_entry.grid(row=4, column=1, padx=5, pady=5, sticky='ew')
        
        # Initially hide staff account fields
        username_entry.grid_remove()
        password_entry.grid_remove()
        
        def toggle_staff_fields():
            if entries["Create Staff Account"].get():
                username_entry.grid()
                password_entry.grid()
            else:
                username_entry.grid_remove()
                password_entry.grid_remove()
        
        entries["Create Staff Account"].trace("w", lambda *args: toggle_staff_fields())
        
        # Configure grid weights
        form_frame.columnconfigure(1, weight=1)
        
        def submit():
            name = entries["Full Name"].get()
            contact = entries["Contact Info"].get()
            create_staff = entries["Create Staff Account"].get()
            username = username_entry.get() if create_staff else None
            password = password_entry.get() if create_staff else None
            
            # Validate inputs
            if not all([name, contact]):
                messagebox.showerror("Error", "Full Name and Contact Info are required")
                return
                
            if create_staff and not all([username, password]):
                messagebox.showerror("Error", "Username and Password are required for staff accounts")
                return
                
            if create_staff and username in self.data.credentials:
                messagebox.showerror("Error", "Username already exists")
                return
                
            # Create customer ID
            cid = str(len(self.data.customers) + 1)
            
            # Create customer record
            self.data.customers[cid] = {
                "name": name,
                "contact": Utils.encrypt(contact),
                "created_at": str(datetime.datetime.now()),
                "history": [],
                "is_staff": create_staff,
                "username": username if create_staff else None
            }
            
            # Create staff credentials if needed
            if create_staff:
                self.data.credentials[username] = Utils.encrypt(password)
            
            self.data.save_all()
            self.logger.add(f"Customer added: {name}" + (" (staff account)" if create_staff else ""))
            messagebox.showinfo("Success", f"Customer {name} added successfully!")
            dialog.destroy()
        
        # Button frame with matching style
        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=15)
        
        ttk.Button(button_frame, text="Submit", command=submit, 
                style='TButton').pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy,
                style='TButton').pack(side=tk.LEFT, padx=10)
        
        # Make the dialog modal
        dialog.transient(self.root)
        dialog.grab_set()
        self.root.wait_window(dialog)
    def view_customers(self):
        win = tk.Toplevel(self.root)
        win.title("Customer Profiles")
        win.configure(bg=self.bg_color)
        
        # Configure treeview style
        self.style.configure("Treeview", 
                           background="#ecf0f1",
                           fieldbackground="#ecf0f1",
                           foreground="#2c3e50",
                           rowheight=25)
        self.style.configure("Treeview.Heading", 
                           background="#3498db",
                           foreground="#ecf0f1",
                           font=('Helvetica', 10, 'bold'))
        self.style.map("Treeview", 
                      background=[('selected', '#2980b9')],
                      foreground=[('selected', '#ecf0f1')])
        
        tree_frame = ttk.Frame(win)
        tree_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Treeview scrollbar
        tree_scroll = ttk.Scrollbar(tree_frame)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        tree = ttk.Treeview(tree_frame, columns=("ID", "Name", "Contact"), 
                           show='headings', yscrollcommand=tree_scroll.set)
        tree.pack(fill='both', expand=True)
        
        tree_scroll.config(command=tree.yview)
        
        tree.heading("ID", text="ID")
        tree.heading("Name", text="Name")
        tree.heading("Contact", text="Contact")
        
        tree.column("ID", width=50, anchor='center')
        tree.column("Name", width=150, anchor='w')
        tree.column("Contact", width=200, anchor='w')
        
        for cid, data in self.data.customers.items():
            tree.insert("", "end", values=(cid, data['name'], Utils.decrypt(data['contact'])))
# add Transaction method

    def add_transaction(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Transaction")
        dialog.configure(bg=self.bg_color)
        dialog.resizable(False, False)
        
        ttk.Label(dialog, text="Customer ID:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        cid_entry = ttk.Entry(dialog)
        cid_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(dialog, text="Amount:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        amount_entry = ttk.Entry(dialog)
        amount_entry.grid(row=1, column=1, padx=5, pady=5)
        
        def submit():
            cid = cid_entry.get()
            try:
                amount = float(amount_entry.get())
            except ValueError:
                messagebox.showerror("Error", "Invalid amount")
                return
                
            if cid in self.data.customers and amount:
                txn = {
                    "customer_id": cid,
                    "amount": amount,
                    "timestamp": str(datetime.datetime.now()),
                    "staff_username": self.username  # Track which staff member created this
                }
                self.data.transactions.append(txn)
                self.data.customers[cid]["history"].append(txn)
                self.data.save_all()
                self.data.save_dashboard()
                self.logger.add(f"Transaction added for customer {cid}: {amount} by {self.username}")
                messagebox.showinfo("Transaction", "Transaction recorded")
                if amount > 10000:
                    messagebox.showwarning("Alert", "Suspicious transaction detected!")
                dialog.destroy()
            else:
                messagebox.showerror("Error", "Invalid customer ID or amount")
        
    # Rest of the method remains the same...
        
        btn_frame = ttk.Frame(dialog)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        ttk.Button(btn_frame, text="Submit", command=submit).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
        
        dialog.transient(self.root)
        dialog.grab_set()
        self.root.wait_window(dialog)

    # def view_dashboard(self):
    #     amounts = [txn['amount'] for txn in self.data.transactions]
    #     if not amounts:
    #         messagebox.showinfo("No Data", "No transactions to show")
    #         return
        
    #     fig, ax = plt.subplots(figsize=(8, 5), facecolor='#34495e')
    #     ax.set_facecolor('#34495e')
        
    #     # Customize plot
    #     bars = ax.hist(amounts, bins=10, color="#3498db", edgecolor='#ecf0f1')
    #     ax.set_title("Transaction Distribution", color='#ecf0f1')
    #     ax.set_xlabel("Amount", color='#ecf0f1')
    #     ax.set_ylabel("Frequency", color='#ecf0f1')
        
    #     # Customize ticks and spines
    #     ax.tick_params(colors='#ecf0f1')
    #     for spine in ax.spines.values():
    #         spine.set_color('#7f8c8d')
        
    #     plt.tight_layout()
    #     plt.show()

    def view_my_transactions(self):
    # No need for customer ID dialog since we're showing current user's transactions
        win = tk.Toplevel(self.root)
        win.title(f"{self.username}'s Transactions")
        win.configure(bg=self.bg_color)
        
        # Configure treeview style
        self.style.configure("Treeview", 
                        background="#ecf0f1",
                        fieldbackground="#ecf0f1",
                        foreground="#2c3e50",
                        rowheight=25)
        self.style.configure("Treeview.Heading", 
                        background="#3498db",
                        foreground="#ecf0f1",
                        font=('Helvetica', 10, 'bold'))
        self.style.map("Treeview", 
                    background=[('selected', '#2980b9')],
                    foreground=[('selected', '#ecf0f1')])
        
        tree_frame = ttk.Frame(win)
        tree_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Treeview scrollbar
        tree_scroll = ttk.Scrollbar(tree_frame)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        tree = ttk.Treeview(tree_frame, columns=("Customer", "Amount", "Timestamp"), 
                        show='headings', yscrollcommand=tree_scroll.set)
        tree.pack(fill='both', expand=True)
        
        tree_scroll.config(command=tree.yview)
        
        tree.heading("Customer", text="Customer")
        tree.heading("Amount", text="Amount")
        tree.heading("Timestamp", text="Timestamp")
        
        tree.column("Customer", width=150, anchor='w')
        tree.column("Amount", width=150, anchor='e')
        tree.column("Timestamp", width=250, anchor='w')
        
        # Filter transactions for this user
        user_txns = [txn for txn in self.data.transactions if txn.get("staff_username") == self.username]
        
        for txn in user_txns:
            customer_name = self.data.customers.get(txn["customer_id"], {}).get("name", "Unknown")
            tree.insert("", "end", values=(customer_name, f"${txn['amount']:,.2f}", txn["timestamp"]))
    def show_my_transactions(self, cid):
        win = tk.Toplevel(self.root)
        win.title("My Transactions")
        win.configure(bg=self.bg_color)
        
        # Configure treeview style
        self.style.configure("Treeview", 
                           background="#ecf0f1",
                           fieldbackground="#ecf0f1",
                           foreground="#2c3e50",
                           rowheight=25)
        self.style.configure("Treeview.Heading", 
                           background="#3498db",
                           foreground="#ecf0f1",
                           font=('Helvetica', 10, 'bold'))
        self.style.map("Treeview", 
                      background=[('selected', '#2980b9')],
                      foreground=[('selected', '#ecf0f1')])
        
        tree_frame = ttk.Frame(win)
        tree_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Treeview scrollbar
        tree_scroll = ttk.Scrollbar(tree_frame)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        tree = ttk.Treeview(tree_frame, columns=("Amount", "Timestamp"), 
                           show='headings', yscrollcommand=tree_scroll.set)
        tree.pack(fill='both', expand=True)
        
        tree_scroll.config(command=tree.yview)
        
        tree.heading("Amount", text="Amount")
        tree.heading("Timestamp", text="Timestamp")
        
        tree.column("Amount", width=150, anchor='e')
        tree.column("Timestamp", width=250, anchor='w')
        
        for txn in self.data.customers[cid]["history"]:
            tree.insert("", "end", values=(f"${txn['amount']:,.2f}", txn["timestamp"]))

    def edit_transaction(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Transaction")
        dialog.configure(bg=self.bg_color)
        dialog.resizable(False, False)
        
        ttk.Label(dialog, text="Customer ID:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        cid_entry = ttk.Entry(dialog)
        cid_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(dialog, text="Timestamp:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        ts_entry = ttk.Entry(dialog)
        ts_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(dialog, text="New Amount:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        amount_entry = ttk.Entry(dialog)
        amount_entry.grid(row=2, column=1, padx=5, pady=5)
        
        def submit():
            cid = cid_entry.get()
            ts = ts_entry.get()
            try:
                new_amount = float(amount_entry.get())
            except ValueError:
                messagebox.showerror("Error", "Invalid amount")
                return
                
            found = False
            for txn in self.data.transactions:
                if txn["customer_id"] == cid and txn["timestamp"] == ts:
                    txn["amount"] = new_amount
                    found = True
            
            if cid in self.data.customers:
                for txn in self.data.customers[cid].get("history", []):
                    if txn["timestamp"] == ts:
                        txn["amount"] = new_amount
                        found = True
            
            if found:
                self.data.save_all()
                messagebox.showinfo("Success", "Transaction updated")
                dialog.destroy()
            else:
                messagebox.showerror("Error", "Transaction not found")
        
        btn_frame = ttk.Frame(dialog)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        ttk.Button(btn_frame, text="Update", command=submit).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
        
        dialog.transient(self.root)
        dialog.grab_set()
        self.root.wait_window(dialog)

    def delete_transaction(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Delete Transaction")
        dialog.configure(bg=self.bg_color)
        dialog.resizable(False, False)
        
        ttk.Label(dialog, text="Customer ID:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        cid_entry = ttk.Entry(dialog)
        cid_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(dialog, text="Timestamp:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        ts_entry = ttk.Entry(dialog)
        ts_entry.grid(row=1, column=1, padx=5, pady=5)
        
        def submit():
            cid = cid_entry.get()
            ts = ts_entry.get()
            
            # Delete from transactions list
            initial_count = len(self.data.transactions)
            self.data.transactions = [txn for txn in self.data.transactions 
                                     if not (txn["customer_id"] == cid and txn["timestamp"] == ts)]
            
            # Delete from customer history
            if cid in self.data.customers:
                initial_history_count = len(self.data.customers[cid].get("history", []))
                self.data.customers[cid]["history"] = [
                    txn for txn in self.data.customers[cid].get("history", []) 
                    if txn["timestamp"] != ts
                ]
                final_history_count = len(self.data.customers[cid].get("history", []))
            else:
                initial_history_count = final_history_count = 0
            
            if initial_count != len(self.data.transactions) or initial_history_count != final_history_count:
                self.data.save_all()
                messagebox.showinfo("Success", "Transaction deleted")
                dialog.destroy()
            else:
                messagebox.showerror("Error", "Transaction not found")
        
        btn_frame = ttk.Frame(dialog)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        ttk.Button(btn_frame, text="Delete", command=submit).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
        
        dialog.transient(self.root)
        dialog.grab_set()
        self.root.wait_window(dialog)

    def view_audit(self):
        win = tk.Toplevel(self.root)
        win.title("Audit Logs")
        win.configure(bg=self.bg_color)
        
        # Header frame
        header_frame = ttk.Frame(win)
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(header_frame, text="Audit Logs", style='Header.TLabel').pack()
        
        # Text frame with scrollbar
        text_frame = ttk.Frame(win)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        text_scroll = ttk.Scrollbar(text_frame)
        text_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        text = tk.Text(text_frame, wrap=tk.WORD, yscrollcommand=text_scroll.set,
                      bg="#34495e", fg="#ecf0f1", insertbackground="#ecf0f1",
                      selectbackground="#3498db", selectforeground="#ecf0f1",
                      font=('Consolas', 10))
        text.pack(fill=tk.BOTH, expand=True)
        
        text_scroll.config(command=text.yview)
        
        for entry in self.logger.get_log():
            text.insert(tk.END, f"{entry['timestamp']} - {entry['action']}\n")
        
        text.config(state=tk.DISABLED)

    def generate_report(self):
        report_file = os.path.join(REPORTS_DIR, "sample_report.csv")
        try:
            with open(report_file, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Customer ID", "Name", "Contact", "Total Transactions"])
                for cid, data in self.data.customers.items():
                    total = sum(txn["amount"] for txn in data.get("history", []))
                    writer.writerow([cid, data["name"], Utils.decrypt(data["contact"]), total])
            
            # Show success message with modern styling
            success_dialog = tk.Toplevel(self.root)
            success_dialog.title("Report Generated")
            success_dialog.configure(bg=self.bg_color)
            success_dialog.resizable(False, False)
            
            ttk.Label(success_dialog, 
                     text=f"Report successfully saved to:\n{report_file}",
                     style='TLabel').pack(padx=20, pady=20)
            
            ttk.Button(success_dialog, text="OK", command=success_dialog.destroy,
                      style='TButton').pack(pady=(0, 10))
            
            self.logger.add("Admin generated report")
        except PermissionError:
            messagebox.showerror("Permission Denied", f"Close '{report_file}' and try again.")
