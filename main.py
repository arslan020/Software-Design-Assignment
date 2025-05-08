import datetime
import tkinter as tk
from tkinter import ttk, messagebox
from data_manager import DataManager
from audit_logger import AuditLogger
from app import FinSecureApp
from utils import Utils

def login_window():
    data_manager = DataManager()
    logger = AuditLogger()

    def apply_styles():
        style = ttk.Style()
        style.theme_use('clam')
        
        bg_color = "#2c3e50"
        fg_color = "#ecf0f1"
        accent_color = "#3498db"
        
        style.configure('TFrame', background=bg_color)
        style.configure('TLabel', background=bg_color, foreground=fg_color, font=('Helvetica', 10))
        style.configure('TButton', background=accent_color, foreground=fg_color, 
                       font=('Helvetica', 10, 'bold'), borderwidth=1)
        style.map('TButton', 
                 background=[('active', '#2980b9'), ('pressed', '#2980b9')],
                 foreground=[('active', fg_color), ('pressed', fg_color)])
        style.configure('TCombobox', fieldbackground=fg_color)
        style.configure('Header.TLabel', font=('Helvetica', 16, 'bold'))
        
        return bg_color, fg_color

    def login():
        username = user_entry.get()
        password = pass_entry.get()

        if username in data_manager.credentials:
            stored_password = Utils.decrypt(data_manager.credentials[username])
            if stored_password == password:
                role = "admin" if username == "admin" else "staff"
                login_win.destroy()
                root = tk.Tk()
                FinSecureApp(root, role, data_manager, logger, username)  # Pass username here
                root.mainloop()
            else:
                messagebox.showerror("Login Failed", "Invalid credentials")

    def signup():
        # Create signup dialog with matching styling
        signup_dialog = tk.Toplevel(login_win)
        signup_dialog.title("FinSecure Sign Up")
        signup_dialog.geometry("400x400")
        signup_dialog.resizable(False, False)
        signup_dialog.configure(bg=bg_color)
        
        # Header
        ttk.Label(signup_dialog, text="Create New Account", style='Header.TLabel').pack(pady=15)
        
        # Form frame
        form_frame = ttk.Frame(signup_dialog)
        form_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
        
        # Form fields with consistent styling
        fields = [
            ("Username", "text"),
            ("Password", "password"),
            ("Full Name", "text"),
            ("Contact Info", "text"),
            ("Role", "role")
        ]
        
        entries = {}
        for i, (label, field_type) in enumerate(fields):
            ttk.Label(form_frame, text=label+":").grid(row=i, column=0, padx=5, pady=5, sticky='e')
            
            if field_type == "password":
                entry = ttk.Entry(form_frame, show="*")
            elif field_type == "role":
                role_var = tk.StringVar()
                entry = ttk.Combobox(form_frame, textvariable=role_var, 
                                    values=("admin", "staff"), state='readonly')
                entry.current(1)  # Default to staff
            else:
                entry = ttk.Entry(form_frame)
                
            entry.grid(row=i, column=1, padx=5, pady=5, sticky='ew')
            entries[label] = entry
        
        # Configure grid weights
        form_frame.columnconfigure(1, weight=1)
        
        def submit():
            # Get all field values
            username = entries["Username"].get()
            password = entries["Password"].get()
            name = entries["Full Name"].get()
            contact = entries["Contact Info"].get()
            role = entries["Role"].get() if hasattr(entries["Role"], 'get') else "staff"
            
            # Validate inputs
            if not all([username, password, name]):
                messagebox.showerror("Error", "Username, Password and Full Name are required")
                return
                
            if username in data_manager.credentials:
                messagebox.showerror("Error", "Username already exists")
                return
                
            # Save credentials
            data_manager.credentials[username] = Utils.encrypt(password)
            
            # Create customer record for staff
            if role == "staff":
                new_customer_id = str(len(data_manager.customers) + 1)
                data_manager.customers[new_customer_id] = {
                    "name": name,
                    "contact": Utils.encrypt(contact) if contact else Utils.encrypt(""),
                    "created_at": str(datetime.datetime.now()),
                    "history": [],
                    "is_staff": True,
                    "username": username
                }
            
            data_manager.save_all()
            messagebox.showinfo("Success", "Account created successfully!")
            signup_dialog.destroy()
        
        # Button frame with matching style
        button_frame = ttk.Frame(signup_dialog)
        button_frame.pack(pady=15)
        
        ttk.Button(button_frame, text="Submit", command=submit, 
                style='TButton').pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Cancel", command=signup_dialog.destroy,
                style='TButton').pack(side=tk.LEFT, padx=10)
        
        # Make the dialog modal
        signup_dialog.transient(login_win)
        signup_dialog.grab_set()
        login_win.wait_window(signup_dialog)
# Create the main window
    login_win = tk.Tk()
    login_win.title("FinSecure Login")
    login_win.geometry("350x300")
    login_win.resizable(False, False)
    
    bg_color, fg_color = apply_styles()
    login_win.configure(bg=bg_color)
    
    # Header
    ttk.Label(login_win, text="FinSecure Login", style='Header.TLabel').pack(pady=15)
    
    # Form frame
    form_frame = ttk.Frame(login_win)
    form_frame.pack(padx=20, pady=10)
    
    ttk.Label(form_frame, text="Username").grid(row=0, column=0, padx=5, pady=5, sticky='e')
    user_entry = ttk.Entry(form_frame)
    user_entry.grid(row=0, column=1, padx=5, pady=5)
    
    ttk.Label(form_frame, text="Password").grid(row=1, column=0, padx=5, pady=5, sticky='e')
    pass_entry = ttk.Entry(form_frame, show="*")
    pass_entry.grid(row=1, column=1, padx=5, pady=5)
    
    ttk.Label(form_frame, text="Role").grid(row=2, column=0, padx=5, pady=5, sticky='e')
    role_var = tk.StringVar()
    role_combobox = ttk.Combobox(form_frame, textvariable=role_var, values=("admin", "staff"), state='readonly')
    role_combobox.grid(row=2, column=1, padx=5, pady=5)
    role_combobox.current(0)
    
    # Button frame
    button_frame = ttk.Frame(login_win)
    button_frame.pack(pady=15)
    
    ttk.Button(button_frame, text="Login", command=login).pack(side=tk.LEFT, padx=10)
    ttk.Button(button_frame, text="Sign Up", command=signup).pack(side=tk.LEFT, padx=10)

    login_win.mainloop()

if __name__ == "__main__":
    login_window()