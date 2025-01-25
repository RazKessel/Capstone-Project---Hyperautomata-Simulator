import tkinter as tk
from tkinter import ttk, messagebox
from components.utils.logger import operation_logger, error_logger

class LoginWindow(ttk.Frame):
    """
        Simple login window that checks credentials via DBManager.
        On success, sets self.master.current_user and closes.
    """

    def __init__(self, parent, db_manager, success_callback):
        super().__init__(parent)
        operation_logger.info("Initializing LoginFrame.")
        self.db_manager = db_manager
        self.parent = parent
        self.success_callback = success_callback

        self.configure(padding=20)

        # Configure grid to center the child frame
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Create a child frame to hold the widgets
        self.child_frame = tk.Frame(self)
        self.child_frame.grid(row=0, column=0)

        # Configure grid inside child frame
        for i in range(3):
            self.child_frame.grid_rowconfigure(i, weight=1, pad=10)
        self.child_frame.grid_columnconfigure(0, weight=1)
        self.child_frame.grid_columnconfigure(1, weight=1)

        ttk.Label(self.child_frame, text="Username:").grid(row=0, column=0, pady=5, sticky="e")
        self.username_var = tk.StringVar()
        username_entry = ttk.Entry(self.child_frame, textvariable=self.username_var, width=25)
        username_entry.grid(row=0, column=1, pady=5, padx=5, sticky="w")

        ttk.Label(self.child_frame, text="Password:").grid(row=1, column=0, pady=5, sticky="e")
        self.password_var = tk.StringVar()
        password_entry = ttk.Entry(self.child_frame, show="*", textvariable=self.password_var, width=25)
        password_entry.grid(row=1, column=1, pady=5, padx=5, sticky="w")

        frm = tk.Frame(self.child_frame)
        frm.grid(row=2, column=0, columnspan=2, pady=15)
        ttk.Button(frm, text="Login", command=self.on_login).pack(side=tk.LEFT, padx=10)
        ttk.Button(frm, text="Register", command=self.on_register).pack(side=tk.LEFT, padx=10)

        self.parent.protocol("WM_DELETE_WINDOW", self.on_cancel)

        operation_logger.info("LoginFrame widgets initialized.")
        
    def on_cancel(self):
        """ Handle the window close event by terminating the application. """
        operation_logger.info("LoginFrame closed by user.")
        self.success_callback(None)
        
    def on_login(self):
        """ Attempt to log in the user with provided credentials. """
        user = self.username_var.get().strip()
        pwd = self.password_var.get().strip()
        if not user or not pwd:
            messagebox.showerror("Error", "Please enter both username and password.")
            error_logger.warning("Login attempt with empty username or password.")
            return
        try:
            if self.db_manager.check_user_credentials(user, pwd):
                operation_logger.info(f"User logged in: {user}")
                self.success_callback(user)
            else:
                messagebox.showerror("Error", "Invalid credentials.")
                error_logger.warning(f"Invalid login attempt for user: {user}")
        except Exception as e:
            messagebox.showerror("Error", "An error occurred during login.")
            error_logger.error(f"Error during login for user {user}: {e}")
            self.success_callback(None)

    def on_register(self):
        """ Attempt to register a new user with provided credentials. """
        user = self.username_var.get().strip()
        pwd = self.password_var.get().strip()
        if not user or not pwd:
            messagebox.showerror("Error", "Please enter both username and password.")
            error_logger.warning("Registration attempt with empty username or password.")
            return
        try:
            ok, msg = self.db_manager.add_user(user, pwd)
            if not ok:
                messagebox.showerror("Error", msg)
                error_logger.error(f"Registration failed for user: {user}, Reason: {msg}")
            else:
                messagebox.showinfo("Registered", msg)
                operation_logger.info(f"User registered successfully: {user}")
                self.success_callback(user)
        except Exception as e:
            messagebox.showerror("Error", "An error occurred during registration.")
            error_logger.error(f"Error during registration for user {user}: {e}")
            self.success_callback(None)

