import sys
import tkinter as tk


from components.db_integration import DBManager
from components.login_window import LoginWindow
from components.run_app import MainApplication

from components.utils.constants import LOGIN_HEIGHT, LOGIN_WIDTH

    
def main():
    # Initialize DB
    db_manager = DBManager(db_url="sqlite:///automata.db")

    login_root = tk.Tk()
    login_root.title("Login")
    
    screen_width = login_root.winfo_screenwidth()
    screen_height = login_root.winfo_screenheight()
    
    x = (screen_width // 2) - (LOGIN_WIDTH // 2)
    y = (screen_height // 2) - (LOGIN_HEIGHT // 2)
    
    login_root.geometry(f"{LOGIN_WIDTH}x{LOGIN_HEIGHT}+{x}+{y}")    

    
    
    
    def on_login_success(user):
        """
            Callback from LoginWindow: 
            If user is not None => success => destroy login root => open main app
            If user is None => user canceled => close everything
        """
        if user:
            login_root.destroy()
            app = MainApplication(current_user=user, db_manager=db_manager)
            app.mainloop()
        else:
            login_root.destroy()
            sys.exit(0)

    login_frame = LoginWindow(
        parent=login_root,
        db_manager=db_manager,
        success_callback=on_login_success
    )
    login_frame.pack(expand=True, fill="both")

    login_root.mainloop()

if __name__ == "__main__":
    main()
