import tkinter as tk
from tkinter import ttk, messagebox
from data_generator import generate_data  # Assume this handles data generation
import json

#Tooltip Class
class Tooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event=None):
        if self.tooltip_window or not self.text:
            return
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25
        self.tooltip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(
            tw, text=self.text, justify="left",
            background="lightyellow", relief="solid", borderwidth=1,
            font=("tahoma", "8", "normal")
        )
        label.pack(ipadx=1)

    def hide_tooltip(self, event=None):
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None

# Main Application Logic
def launch_ui():
    # Variables to store user selections
    selected_fields = []
    field_constraints = {}

    def add_placeholder(entry, placeholder):
        entry.insert(0, placeholder)
        entry.config(foreground="grey")

        def on_focus_in(event):
            if entry.get() == placeholder:
                entry.delete(0, tk.END)
                entry.config(foreground="black")

        def on_focus_out(event):
            if not entry.get():
                add_placeholder(entry, placeholder)

        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)

    def show_second_screen():
        # Collect selected field types
        selected_fields.clear()
        for field, var in field_vars.items():
            if var.get():
                selected_fields.append(field)
        
        # Validate: Ensure at least one field type is selected
        if not selected_fields:
            messagebox.showerror("Error", "At least one field type must be selected.")
            return
        
        # Switch to second screen
        first_screen.pack_forget()
        second_screen.pack(fill="both", expand=True)

        # Display selected fields with constraints text boxes
        for widget in second_screen.winfo_children():
            widget.destroy()  # Clear previous widgets

        row = 0
        for field in selected_fields:
            label = ttk.Label(second_screen, text=f"{field} Constraints (optional):")
            label.grid(row=row, column=0, padx=10, pady=5, sticky="w")
            entry = ttk.Entry(second_screen, width=30)
            entry.grid(row=row, column=1, padx=10, pady=5)
            constraint_entries[field] = entry

            # Add a placeholder based on the field type
            placeholder_messages = {
                "Hobbies": "example: sports, traveling",
                "Age": "example: <30, >40",
                "Address": "example: Country: Romania",
                "Gender": "example: male, female, non binary",
                "Email": "example: example.com",
                "Phone": "example: Country: Romania",
                "Education": "example: High School, PhD",
                "Pets": "example: dog, cat",
                "Random Strings": "example: Length: 10"
            }

            # Get the placeholder message for the current field
            placeholder_text = placeholder_messages.get(field, "Enter constraints if any")

            # Add the placeholder to the entry
            add_placeholder(entry, placeholder_text)

            row += 1

        # Add "Generate Data" button
        generate_button = ttk.Button(second_screen, text="Generate Data", command=generate)
        generate_button.grid(row=row, column=0, columnspan=2, pady=20)

    def generate():
        # Validate number of entries
        try:
            num_entries = int(num_entries_entry.get())
            if num_entries <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid positive integer for the number of entries.")
            return

        # Add a placeholder based on the field type
        placeholder_messages = {
        }

        # Collect constraints for selected fields
        field_constraints.clear()  # Ensure we start fresh
        for field in selected_fields:
            entry_content = constraint_entries[field].get().strip()
            placeholder_text = placeholder_messages.get(field, "Enter constraints if any")

            # Treat placeholder or empty content as no constraint
            if entry_content == "" or entry_content == placeholder_text:
                field_constraints[field] = None  # No constraint
            else:
                field_constraints[field] = entry_content

        # Generate data
        try:
            data = generate_data(selected_fields, field_constraints, num_entries)
            with open("generated_data.json", "w") as f:
                json.dump(data, f, indent=4)
            messagebox.showinfo("Success", "Test data generated successfully! Saved as 'generated_data.json'.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    # Create the main window
    root = tk.Tk()
    root.title("Dynamic Test Data Generator")

    # First screen
    first_screen = tk.Frame(root)
    first_screen.pack(fill="both", expand=True)

    # Field type section
    field_types = [
        "Hobbies", "Age", "Address", "Gender", "Email", 
        "Phone", "Education", "Pets", "Random Strings"
    ]
    field_vars = {field: tk.BooleanVar() for field in field_types}
    constraint_entries = {}

    # Create the LabelFrame to hold checkboxes
    field_frame = ttk.LabelFrame(first_screen, text="Select Field Types")
    field_frame.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    # Add "Select All" checkbox
    select_all_var = tk.BooleanVar()

    def toggle_select_all():
        # Set all checkboxes to the same state as "Select All"
        state = select_all_var.get()
        for var in field_vars.values():
            var.set(state)

    def update_select_all():
        # Update "Select All" checkbox based on individual checkboxes
        if all(var.get() for var in field_vars.values()):
            select_all_var.set(True)
        elif any(var.get() for var in field_vars.values()):
            select_all_var.set(False)
        else:
            select_all_var.set(False)

    # Add the "Select All" checkbox
    select_all_checkbox = ttk.Checkbutton(
        field_frame, text="Select All", variable=select_all_var, command=toggle_select_all
    )
    select_all_checkbox.grid(row=0, column=0, sticky="w", padx=5, pady=5)

    # Add individual field checkboxes below "Select All"
    for idx, field in enumerate(field_types, start=1):
        checkbox = ttk.Checkbutton(
            field_frame,
            text=field,
            variable=field_vars[field],
            command=update_select_all  # Ensure "Select All" is updated on individual changes
        )
        checkbox.grid(row=idx, column=0, sticky="w", padx=5, pady=2)

    # Number of entries
    num_entries_label = ttk.Label(first_screen, text="Number of Entries:")
    num_entries_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
    num_entries_entry = ttk.Entry(first_screen, width=10)
    num_entries_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

    # Next button to proceed to second screen
    next_button = ttk.Button(first_screen, text="Next", command=show_second_screen, state=tk.DISABLED)
    next_button.grid(row=2, column=0, columnspan=2, pady=20)

    # Create the tooltip for the "Next" button
    tooltip = Tooltip(next_button, "Enter a positive integer to enable the button.")

    # Function to validate and enable/disable the Next button
    def validate_next_button():
        # Enable "Next" button only if num_entries_entry contains a valid positive integer
        try:
            value = int(num_entries_entry.get())
            if value > 0:
                next_button.config(state=tk.NORMAL)
                tooltip.text = ""  # Hide tooltip when button is enabled
            else:
                next_button.config(state=tk.DISABLED)
                tooltip.text = "Enter a positive integer to enable the button."
        except ValueError:
            next_button.config(state=tk.DISABLED)
            tooltip.text = "Enter a positive integer to enable the button."

    # Bind validation function to the entry widget
    num_entries_entry.bind("<KeyRelease>", lambda event: validate_next_button())

    # Second screen
    second_screen = tk.Frame(root)

    root.mainloop()
