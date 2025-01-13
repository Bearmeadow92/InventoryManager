from tkinter import messagebox
from tkinter import ttk
import tkinter as tk
from db_utils import init_db, execute_query, fetch_all

# Initialize the database
init_db()

# Update treeview with assets from the database
def update_treeview(treeview):
    """Fetch data from SQLite and populate the treeview."""
    treeview.delete(*treeview.get_children())  # Clear the treeview
    query = "SELECT id, assigned_to, brand, model, serial_number FROM assets"
    assets = fetch_all(query)
    for asset in assets:
        treeview.insert("", "end", iid=asset[0], values=asset[1:])

# Add a device to the database
def add_device(fields, treeview):
    """Add a new asset to the database and update the treeview."""
    asset_data = tuple(field.get() for field in fields.values())
    if all(asset_data):
        query = """
        INSERT INTO assets (assigned_to, brand, model, serial_number, mac_address, ip_address, warranty_expiration, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        execute_query(query, asset_data)
        update_treeview(treeview)
        messagebox.showinfo("Success", "Asset added successfully!")
        for field in fields.values():
            field.delete(0, tk.END)
    else:
        messagebox.showwarning("Input Error", "All fields are required!")

# Edit an existing device
def edit_device(treeview, fields, save_button):
    """Edit a selected asset."""
    selected_item = treeview.focus()
    if not selected_item:
        messagebox.showwarning("Selection Error", "Please select an asset to edit.")
        return

    query = "SELECT * FROM assets WHERE id = ?"
    asset = fetch_all(query, (selected_item,))[0]

    for i, key in enumerate(fields.keys()):
        fields[key].delete(0, tk.END)
        fields[key].insert(0, asset[i + 1])  # Skip the id field

    save_button.config(state="normal")

# Save changes to an edited device
def save_changes(treeview, fields, save_button):
    """Save changes to an edited asset."""
    selected_item = treeview.focus()
    if not selected_item:
        messagebox.showwarning("Save Error", "No asset selected for saving.")
        return

    asset_data = tuple(field.get() for field in fields.values()) + (selected_item,)
    if all(asset_data):
        query = """
        UPDATE assets
        SET assigned_to = ?, brand = ?, model = ?, serial_number = ?, mac_address = ?, ip_address = ?, warranty_expiration = ?, notes = ?
        WHERE id = ?
        """
        execute_query(query, asset_data)
        update_treeview(treeview)
        messagebox.showinfo("Success", "Changes saved successfully!")
        for field in fields.values():
            field.delete(0, tk.END)
        save_button.config(state="disabled")
    else:
        messagebox.showwarning("Input Error", "All fields are required!")

# Delete a device from the database
def delete_device(treeview):
    """Delete a selected asset."""
    selected_item = treeview.focus()
    if not selected_item:
        messagebox.showwarning("Delete Error", "No asset selected for deletion.")
        return

    confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete the selected asset?")
    if confirm:
        query = "DELETE FROM assets WHERE id = ?"
        execute_query(query, (selected_item,))
        update_treeview(treeview)
        messagebox.showinfo("Success", "Asset deleted successfully!")

# GUI Setup
def start_gui():
    """Launch the graphical user interface for the Inventory Manager."""
    root = tk.Tk()
    root.title("IT Inventory Manager")

    # GUI layout and styling
    input_frame = ttk.LabelFrame(root, text="Asset Information", padding=10)
    input_frame.pack(fill="x", padx=10, pady=10)

    fields = {}
    field_names = [
        "Assigned To", "Brand", "Model", "Serial Number", "MAC Address",
        "IP Address", "Warranty Expiration", "Notes"
    ]

    for i, name in enumerate(field_names):
        ttk.Label(input_frame, text=name).grid(row=i, column=0, sticky="w", padx=5, pady=5)
        entry = ttk.Entry(input_frame, width=40)
        entry.grid(row=i, column=1, padx=5, pady=5)
        fields[name] = entry

    button_frame = ttk.Frame(root, padding=10)
    button_frame.pack(fill="x", padx=10, pady=10)

    save_button = ttk.Button(button_frame, text="Save Changes", state="disabled",
                        command=lambda: save_changes(device_tree, fields, save_button))
    save_button.pack(side="left", padx=5)

    ttk.Button(button_frame, text="Add Device",
            command=lambda: add_device(fields, device_tree)).pack(side="left", padx=5)
    ttk.Button(button_frame, text="Delete Device",
            command=lambda: delete_device(device_tree)).pack(side="left", padx=5)

    tree_frame = ttk.LabelFrame(root, text="Asset List", padding=10)
    tree_frame.pack(fill="both", expand=True, padx=10, pady=10)

    columns = ["Assigned To", "Brand", "Model", "Serial Number"]
    device_tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
    for col in columns:
        device_tree.heading(col, text=col)

    device_tree.pack(fill="both", expand=True)

    ttk.Button(button_frame, text="Edit Device",
            command=lambda: edit_device(device_tree, fields, save_button)).pack(side="left", padx=5)

    update_treeview(device_tree)

    root.mainloop()

if __name__ == "__main__":
    start_gui()
