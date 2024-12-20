import tkinter as tk
from tkinter import ttk, messagebox
from data_generator import generate_data  # Assume this handles data generation
import json

# Tooltip Class
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

    # Fixed dimensions for the application window
    window_width = 500  # Set a fixed width
    window_height = 400  # Set a fixed height

    placeholder_messages = {
        "Hobbies": "example: sports, traveling",
        "Age": "example: <30, >40, 30-40",
        "Gender": "example: Male, Female, Non-Binary",
        "Address": "example: Country: Romania",
        "Phone": "example: Country: Romania",
        "Email": "example: example.com",
        "Education": "example: High School, Bachelor, Master, PhD",
        "Pets": "example: dogs, cats",
        "Random Strings": "example: Length: 10"
    }

    # Placeholder handling
    def apply_placeholder(entry, placeholder):
        entry.insert(0, placeholder)
        entry.config(foreground="grey")

        def on_focus_in(event):
            if entry.get() == placeholder:
                entry.delete(0, tk.END)
                entry.config(foreground="black")

        def on_focus_out(event):
            if not entry.get():
                entry.insert(0, placeholder)
                entry.config(foreground="grey")

        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)

    def show_third_screen():
        # Clear the second screen and switch to the third screen
        second_screen.pack_forget()
        center_frame(third_screen)
        show_screen(second_screen, third_screen)
        
        # Clear all children of the third screen
        for widget in third_screen.winfo_children():
            widget.destroy()

        # Create a new Canvas and set its layout
        canvas = tk.Canvas(third_screen)
        canvas.pack(side="top", fill="both", expand=True)

        # Create a frame inside the canvas for the scrollable content
        scrollable_frame = ttk.Frame(canvas)
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        # Create a vertical Scrollbar linked to the canvas
        scrollbar = ttk.Scrollbar(canvas, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Update the canvas scrollregion dynamically
        def update_scroll_region():
            canvas.update_idletasks()
            canvas.config(scrollregion=scrollable_frame.bbox("all"))

        # Generate and display data
        try:
            num_entries = int(num_entries_entry.get())
            data = generate_data(selected_fields, field_constraints, num_entries)
            formatted_data = json.dumps(data, indent=4)

            # Display the generated data in a Text widget inside the scrollable frame
            data_display = tk.Text(scrollable_frame, wrap="word", height=30, width=60)
            data_display.insert("1.0", formatted_data)
            data_display.configure(state="disabled")
            data_display.pack(padx=10, pady=10)

        except Exception as e:
            error_label = tk.Label(scrollable_frame, text=f"Error: {e}", fg="red")
            error_label.pack(padx=10, pady=10)

        # "Back" button
        back_button = ttk.Button(third_screen, text="Back", command=lambda: show_screen(third_screen, second_screen))
        back_button.pack(side="bottom", padx=10)

        # "Exit" button
        exit_button = ttk.Button(third_screen, text="Exit", command=root.quit)
        exit_button.pack(side="bottom", padx=10)

        # Update the scrollable region
        update_scroll_region()

    def show_screen(current, target):
        # If leaving the third screen, explicitly destroy the canvas and scrollbar
        if current == third_screen:
            for widget in current.winfo_children():
                widget.destroy()

        # Hide the current screen and display the target screen
        current.pack_forget()
        target.pack(fill="both", expand=True)

    # Create the main window
    root = tk.Tk()
    root.title("Dynamic Test Data Generator")
    root.geometry(f"{window_width}x{window_height}")  # Set fixed size
    root.resizable(False, False)  # Disable resizing

    # Helper function to center frames within the fixed width
    def center_frame(frame):
        frame.pack(fill="both", expand=True)
        frame.place(relx=0.5, rely=0.5, anchor="center")

    # All screens
    first_screen = tk.Frame(root, width=window_width, height=window_height)
    center_frame(first_screen)
    second_screen = tk.Frame(root)
    center_frame(second_screen)
    third_screen = tk.Frame(root)
    center_frame(third_screen)

    # Second screen handler
    def show_second_screen():
        first_screen.pack_forget()
        center_frame(second_screen)

        # Collect selected fields
        selected_fields.clear()
        for field, var in field_vars.items():
            if var.get():
                selected_fields.append(field)

        # Validation: Ensure at least one field is selected
        if not selected_fields:
            messagebox.showerror("Error", "At least one field type must be selected.")
            return

        # Switch to second screen
        show_screen(first_screen, second_screen)

        # Display constraints inputs
        for widget in second_screen.winfo_children():
            widget.destroy()

        row = 0
        for field in selected_fields:
            label = ttk.Label(second_screen, text=f"{field} Constraints (optional):")
            label.grid(row=row, column=0, padx=10, pady=5, sticky="w")

            entry = ttk.Entry(second_screen, width=40)
            entry.grid(row=row, column=1, padx=10, pady=5)
            constraint_entries[field] = entry

            apply_placeholder(entry, placeholder_messages.get(field, "Enter constraints if any"))
            row += 1

        # Back Button
        ttk.Button(second_screen, text="Back", command=lambda: show_screen(second_screen, first_screen)).grid(
            row=row, column=0, columnspan=2, pady=10
        )
        
        # Generate Data Button
        ttk.Button(second_screen, text="Generate Data", command=generate).grid(
            row=row + 1, column=0, columnspan=2, pady=10
        )

    # First screen handler
    first_screen.pack(fill="both", expand=True)

    field_vars = {field: tk.BooleanVar() for field in placeholder_messages.keys()}
    constraint_entries = {}

    # Field selection frame
    field_frame = ttk.LabelFrame(first_screen, text="Select Field Types", width=window_width)
    field_frame.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    # Add "Select All" Checkbox
    select_all_var = tk.BooleanVar()

    def toggle_select_all():
        # Set all checkboxes to the same state as "Select All"
        state = select_all_var.get()
        for var in field_vars.values():
            var.set(state)
        validate_next_button()  # Update the "Next" button state

    def update_select_all():
        # Update "Select All" checkbox based on individual checkboxes
        if all(var.get() for var in field_vars.values()):
            select_all_var.set(True)
        elif any(var.get() for var in field_vars.values()):
            select_all_var.set(False)
        else:
            select_all_var.set(False)
        validate_next_button()  # Update the "Next" button state

    # Add the "Select All" checkbox
    select_all_checkbox = ttk.Checkbutton(
        field_frame, text="Select All", variable=select_all_var, command=toggle_select_all
    )
    select_all_checkbox.grid(row=0, column=0, sticky="w", padx=5, pady=5)

    # Add individual field checkboxes below "Select All"
    for idx, field in enumerate(placeholder_messages.keys(), start=1):
        checkbox=ttk.Checkbutton(
            field_frame,
            text=field,
            variable=field_vars[field],
            command=lambda: [update_select_all(), validate_next_button()] # Ensure "Select All"/"Next" is updated on individual changes
        )
        checkbox.grid(row=idx, column=0, sticky="w", padx=5, pady=2)

    # Number of entries
    num_entries_label = ttk.Label(first_screen, text="Number of Entries:")
    num_entries_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
    num_entries_entry = ttk.Entry(first_screen, width=40)
    num_entries_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

    # Set the default value of 5
    num_entries_entry.insert(0, "5")  # Set the default value as 5

    # Next button to proceed to second screen
    next_button = ttk.Button(first_screen, text="Next", command=show_second_screen, state=tk.DISABLED)
    next_button.grid(row=2, column=0, columnspan=2, pady=10)

    # Create the tooltip for the "Next" button
    tooltip = Tooltip(next_button, "Enter a positive integer to enable the button.")

    # Function to validate and enable/disable the Next button
    def validate_next_button():
        try:
            # Validate the number of entries
            value = int(num_entries_entry.get())  # Get the value entered by the user
            is_positive_integer = value > 0
        except ValueError:
            is_positive_integer = False

        # Check if at least one checkbox is selected
        is_field_selected = any(var.get() for var in field_vars.values())

        # Update "Next" button state based on both conditions
        if is_field_selected and is_positive_integer:
            next_button.config(state=tk.NORMAL)
            tooltip.text = ""  # Clear the tooltip message when the button is enabled
        else:
            next_button.config(state=tk.DISABLED)
            if not is_field_selected:
                tooltip.text = "At least one field type must be selected."
            elif not is_positive_integer:
                tooltip.text = "Enter a positive integer to enable the button."

    # Bind validation function to the entry widget
    num_entries_entry.bind("<KeyRelease>", lambda event: validate_next_button())  # Trigger on each key release

    # Call validate_next_button to enable/disable the Next button based on the default value
    validate_next_button()  # Check if the default value is valid and enable the button if it is
    
    # Data generation
    def generate():
        try:
            # Validate number of entries
            num_entries = int(num_entries_entry.get())
            if num_entries <= 0:
                raise ValueError

            # Collect constraints
            field_constraints.clear()
            for field in selected_fields:
                entry = constraint_entries[field]
                content = entry.get().strip()
                placeholder = placeholder_messages.get(field, "Enter constraints if any")
                field_constraints[field] = None if content == placeholder or not content else content

            # Generate data and navigate to third screen
            data = generate_data(selected_fields, field_constraints, num_entries)
            show_third_screen()

            # Save to file
            with open("generated_data.json", "w") as f:
                json.dump(data, f, indent=4)

            # Display success message
            messagebox.showinfo("Success", "Test data generated successfully! Saved as 'generated_data.json'.")

        except ValueError:
            messagebox.showerror("Error", "Please enter a valid positive integer for the number of entries.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def show_first_screen():
        # Switch to the first screen
        second_screen.pack_forget()
        center_frame(first_screen)

    root.mainloop()
