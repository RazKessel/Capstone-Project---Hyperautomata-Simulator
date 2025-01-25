def centered_popup(parent, popup):
    """Centers the popup window over the parent window without waiting."""
    popup.withdraw()  
    popup.update_idletasks() 

    width = popup.winfo_width()
    height = popup.winfo_height()
    if width == 1 and height == 1:
        popup.update_idletasks()
        width = popup.winfo_width()
        height = popup.winfo_height()

    x = (popup.winfo_screenwidth() // 2) - (width // 2)
    y = (popup.winfo_screenheight() // 2) - (height // 2)
    popup.geometry(f"+{x}+{y}")

    if parent:
        popup.transient(parent)
    popup.deiconify()
    popup.grab_set()
