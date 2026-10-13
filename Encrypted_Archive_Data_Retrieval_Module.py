import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
#from tkinter import DateEntry
from tkcalendar import DateEntry
from datetime import datetime, timedelta
#import tkinter.font as tkFont
import sys
import csv
from tkinter import scrolledtext
from functools import partial

import decrypt_archive_data_files_datetime_format as datetimeformat
import decrypt_archive_data_files_epoch_time_format as epochformat
import get_filtered_data_from_csv_archive_file as filtereddatacsv
import tooltipclass as tooltip

def validate_spinbox(new_value, min_val, max_val):
    if new_value == "":
        return False  # Allow empty temporarily
    try:
        val = int(new_value)
        return min_val <= val <= max_val
    except ValueError:
        return False

def run_executable_for_date_time_task(d_path):
    # Set cursor to 'wait'
    root.config(cursor="wait")

    # Schedule the actual task to run after a short delay
    root.after(100, run_executable_for_date_time, d_path)

def run_executable_for_date_time(d_path):
    try:
        if not d_path:
            print("Directory is null or empty.")
            messagebox.showerror("Error", "Directory path is invalid or empty.")
            return

        # Call your actual processing function here
        datetimeformat.run_datetime_format_function(d_path)

        # Show success message
        messagebox.showinfo("Decrypt to DateTime","The task has been completed successfully!\nSee the console window for more details.")

    except Exception as e:
        print(f"An error occurred: {e}")
        messagebox.showerror("Error", f"An error occurred:\n{e}")
    
    finally:
        # Always reset the cursor
        root.config(cursor="")
      
def run_executable_for_epoch_time_task(d_path):
    # Set the wait cursor while performing the task
    root.config(cursor="wait")

    # Use after() to run the task asynchronously and keep the UI responsive
    root.after(100, run_executable_for_epoch_time, d_path)

def run_executable_for_epoch_time(d_path):
    try:
        # Set the wait cursor while performing the task
        root.config(cursor="wait")

        if not d_path:  # Check if the directory path is None or empty
            print("Directory is null or empty")
            messagebox.showerror("Error", "The directory path is invalid or empty.")
        else:
            # Assuming epochformat.run_epoch_time_format_function is defined elsewhere
            epochformat.run_epoch_time_format_function(d_path)
            
            # Show success message when the task completes
            messagebox.showinfo("Decrypt to Epoch", "The task has been completed successfully!\nSee the console window for more details.")
    except Exception as e:
        # Handle unexpected errors and restore the cursor
        print(f"An error occurred: {e}")
        messagebox.showerror("Error", f"An error occurred: {e}")
    finally:
        # Restore the normal cursor regardless of success or failure
        root.config(cursor="")

def run_filter_data_csv_function_task(d_path, f_name, s_time, e_time, time_interval_gap):
    # Change cursor to "wait" before the task starts
    root.config(cursor="wait")

    # Use after() to handle long-running task without blocking the main loop
    root.after(100, run_filter_data_csv_function, d_path, f_name, s_time, e_time, time_interval_gap)

def run_filter_data_csv_function(d_path, f_name, s_time, e_time, time_interval_gap):
    try:
        # Check if the directory path is None or empty
        if not d_path:  # Handles both None and empty string
            print("Directory is null or empty.")
            messagebox.showerror("Error", "Directory path is invalid or empty.")
            return

        # Check if the file name is None or empty
        if not f_name:
            print("File name is null or empty.")
            messagebox.showerror("Error", "File name is invalid or empty.")
            return

        # Check if the start and end time are valid
        if not s_time or not e_time:
            print("Start time or end time is invalid.")
            messagebox.showerror("Error", "Start time or end time is invalid.")
            return

        # Check if the time interval gap is valid
        if int(time_interval_gap) <= 0:
            print("Time interval gap must be greater than 0.")
            messagebox.showerror("Error", "Time interval gap must be greater than 0.")
            return

        # Call the function to get filtered data in CSV
        filtereddatacsv.get_filtered_data_in_csv_function(d_path, f_name, s_time, e_time, time_interval_gap)
        print("Data filtered and saved successfully.")

        # Show success message
        messagebox.showinfo("Filtered Data", "The task has been completed successfully!\nSee the console window for more details.")

    except Exception as e:
        # Handle unexpected errors
        print(f"An error occurred while processing the CSV: {e}")
        messagebox.showerror("Error", f"An error occurred: {e}")
    
    finally:
        # Restore the normal cursor after the task is done
        root.config(cursor="")

def save_treeview_to_csv(tree):
    # Ask user for a filename
    filename = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV files", "*.csv")],
        title="Save to CSV"
    )

    if filename:
        if not filename.endswith('.csv'):
            filename += '.csv'

        try:
            with open(filename, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)

                # Only write the second column (var_name)
                for row_id in tree.get_children():
                    row = tree.item(row_id)['values']
                    if len(row) > 1:  # Ensure var_name exists
                        writer.writerow([row[1]])  # Just var_name

            messagebox.showinfo("Success", f"Saved var_name data to {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file:\n{e}")

# Function to delete selected item(s) from the treeview
def delete_from_tree(event, tree):
    # Get all selected items from the treeview
    selected_items = tree.selection()
    if selected_items:
        # Loop through the selected items and delete each one
        for item_id in selected_items:
            tree.delete(item_id)

def on_double_click(event, tree1, tree2):
    # Get all selected items from tree1
    selected_items = tree1.selection()

    if not selected_items:
        return

    # Get existing items in tree2 (standardized)
    existing_items = [
        tuple(str(val) for val in tree2.item(child)['values'])
        for child in tree2.get_children()
    ]

    duplicates_found = False

    for item_id in selected_items:
        item_values = tree1.item(item_id, 'values')
        standardized_item = tuple(str(val) for val in item_values)

        if standardized_item in existing_items:
            duplicates_found = True
            continue  # Skip duplicates
        else:
            tree2.insert("", "end", values=item_values)

    if duplicates_found:
        messagebox.showwarning("Duplicate Entry", "Some rows were already added and were skipped.")
        
def filter_tree(tree, all_data, text, columns):
    tree.delete(*tree.get_children())  # Clear current items
    text = text.lower()
    for row in all_data:
        if not text or any(text in str(cell).lower() for cell in row):
            tree.insert("", "end", values=row)

def open_modal_dialog(csv_file):
    print(csv_file)
    # Create a new top-level window
    dialog = tk.Toplevel(root)
    dialog.title("Parameter Selection Dialog")
    dialog.geometry("800x400")

    # Create a frame to hold the tables side by side
    frame = ttk.Frame(dialog)
    frame.pack(padx=10, pady=10, fill='both', expand=True)

    # Define the column names for the tables
    columns = ["Point_Id", "Var_Name"]

    # Function to create a Treeview with scrollbars
    def create_treeview(parent, row, column):
        tree = ttk.Treeview(parent, columns=columns, show="headings", selectmode="extended")
        tree.grid(row=row, column=column, padx=10, pady=10, sticky='nsew')

        # Define headings and columns
        for col in columns:
            tree.heading(col, text=col)
            tree.column("Point_Id", width=100, minwidth=100, stretch=False)
            tree.column("Var_Name", width=300, minwidth=200, stretch=True)
            #tree.column(col, width=100, anchor='w', stretch=True)

        # Create vertical scrollbar
        vsb = ttk.Scrollbar(parent, orient="vertical", command=tree.yview)
        vsb.grid(row=row, column=column+1, sticky='ns')
        tree.configure(yscrollcommand=vsb.set)

        # Create horizontal scrollbar
        hsb = ttk.Scrollbar(parent, orient="horizontal", command=tree.xview)
        hsb.grid(row=row+1, column=column, columnspan=2, sticky='ew')
        tree.configure(xscrollcommand=hsb.set)

        return tree

    # Create the first table
    tree1 = create_treeview(frame, 0, 0)
    tree1.bind("<Double-1>", lambda event: on_double_click(event, tree1, tree2))
    # Create the second table
    tree2 = create_treeview(frame, 0, 2)
    tree2.bind("<Double-1>", lambda event: delete_from_tree(event, tree2))


    # Configure the frame to expand and fill the available space
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_rowconfigure(1, weight=0)
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(1, weight=0)
    frame.grid_columnconfigure(2, weight=1)
    frame.grid_columnconfigure(3, weight=0)

    all_rows = []  # Add this before the CSV reading section
    
    matched_values = set()

    if csv_file:
        try:
            with open(csv_file, newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                for row in reader:
                    if row:
                        matched_values.add(row[0].strip().lower())
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read selected file:\n{e}")
        
    # Read data from the CSV file and insert into tree1
    try:
        with open('all_point_ids_combined_list.csv', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) > 3:  # Ensure the row has enough columns
                    # Insert data into tree1 (columns 2 and 3)
                    values = (row[2], row[3])
                    all_rows.append(values)
                    tree1.insert("", "end", values=values)
                    # Check if Var_Name or Var_name match any value from the file
                    if values[0].strip().lower() in matched_values or values[1].strip().lower() in matched_values:
                        existing = [tree2.item(i)['values'] for i in tree2.get_children()]
                        if values not in existing:
                            tree2.insert("", "end", values=values)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while reading the CSV file: {e}")
    
    search_frame = ttk.Frame(dialog)
    search_frame.pack(padx=10, pady=(10, 0), fill='x')
    
    ttk.Label(search_frame, text="Search:").pack(side='left')
    
    search_var = tk.StringVar()
    search_entry = ttk.Entry(search_frame, textvariable=search_var)
    search_entry.pack(side='left', fill='x', expand=True, padx=5)
    search_entry.bind("<Return>", lambda event: filter_tree(tree1, all_rows, search_var.get(), columns))
    
    search_button = ttk.Button(search_frame, text="Filter", command=lambda: filter_tree(tree1, all_rows, search_var.get(), columns))
    search_button.pack(side='left')
    
    save_button = ttk.Button(dialog, text="Save Table2 as CSV", command=lambda: save_treeview_to_csv(tree2))
    save_button.pack(pady=10)


    # Make the dialog modal
    dialog.grab_set()
    dialog.transient(root)  # Keep the dialog on top of the main window
    dialog.protocol("WM_DELETE_WINDOW", dialog.destroy)  # Handle window close
    dialog.wait_window()  # Wait until the dialog is closed

class TextRedirector:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, text):
        self.text_widget.insert(tk.END, text)
        self.text_widget.see(tk.END)  # Scroll to the end
        self.text_widget.update_idletasks()  # Update the GUI

    def flush(self):
        pass  # This is needed for Python 3 compatibility

def browse_directory():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        path_var.set(folder_selected)

def browse_file():
    file_selected = filedialog.askopenfilename(
        title="Select CSV File",
        filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
    )
    if file_selected:
        file_var.set(file_selected)

def get_datetime(date_widget, hour_var, minute_var, second_var):
    date = date_widget.get_date()
    hour = int(hour_var.get())
    minute = int(minute_var.get())
    second = int(second_var.get())
    return datetime(date.year, date.month, date.day, hour, minute, second)

def get_filter_data_in_csv():
    directory = path_var.get()
    csv_file = file_var.get()
    start_datetime = get_datetime(start_date, start_hour_var, start_minute_var, start_second_var)
    end_datetime = get_datetime(end_date, end_hour_var, end_minute_var, end_second_var)
    time_interval_gap = time_interval_var.get();
    # Validate directory and file selections
    if not directory or not csv_file:
        messagebox.showerror("Input Error", "Please select both a directory and a CSV file.")
        return

    # Validate that start time is less than end time and within 24 hours
    if start_datetime >= end_datetime:
        messagebox.showerror("Time Error", "Start time must be earlier than end time.")
        return
    if (end_datetime - start_datetime).total_seconds() > 86400:
        messagebox.showerror("Time Error", "Time range cannot exceed 24 hours.")
        return

    # Process the collected data as needed
    print(f"Directory: {directory}")
    print(f"CSV File: {csv_file}")
    print(f"Start: {start_datetime}")
    print(f"End:   {end_datetime}")
    
    start_formatted = start_datetime.strftime("%Y-%m-%d %H:%M:%S")
    end_formatted = end_datetime.strftime("%Y-%m-%d %H:%M:%S")
    run_filter_data_csv_function_task(directory, csv_file, start_formatted, end_formatted, time_interval_gap)
    
def exit_action():
    root.quit()

# Main window Dialog started here
root = tk.Tk()
root.title("Archived Data Retrieval Module")
style = ttk.Style()
# List all available themes
#print(style.theme_names())

# Set to a more XP-ish theme
style.theme_use("groove") 
root.minsize(height=660, width=770)
root.maxsize(height=660, width=770)  # Set maximum height and width

# Create a canvas
canvas = tk.Canvas(root)
canvas.pack(fill=tk.BOTH, expand=True)

# Create vertical and horizontal scrollbars
#v_scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
#v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
#h_scrollbar = ttk.Scrollbar(root, orient="horizontal", command=canvas.xview)
#h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

# Configure the canvas to use the scrollbars
#canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
#canvas.configure(yscrollcommand=v_scrollbar.set)
#v_scrollbar.config(command=canvas.yview)
#h_scrollbar.config(command=canvas.xview)

#Create a frame inside the canvas
scrollable_frame = ttk.Frame(canvas)
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

# Update the scroll region whenever the window is resized
def on_frame_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

scrollable_frame.bind("<Configure>", on_frame_configure)

# Frame for file and directory selection
file_frame = ttk.LabelFrame(scrollable_frame, text="File and Directory Selection", padding="10")
file_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

# Directory selector
path_var = tk.StringVar()
ttk.Label(file_frame, text="Select Directory:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
path_entry = ttk.Entry(file_frame, textvariable=path_var, width=50)
path_entry.grid(row=0, column=1, padx=10, pady=10)
dir_browse = ttk.Button(file_frame, text="Browse", command=browse_directory)
dir_browse.grid(row=0, column=2, padx=10, pady=10)

tooltip.ToolTip(path_entry, "Shows the directory containing encrypted (*.enc) archive files");
tooltip.ToolTip(dir_browse, "Browse to find the directory with encrypted (*.enc) archive files");
# CSV file selector
file_var = tk.StringVar()
ttk.Label(file_frame, text="Select CSV File:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
file_entry = ttk.Entry(file_frame, textvariable=file_var, width=50)
file_entry.grid(row=1, column=1, padx=10, pady=10)
file_browse = ttk.Button(file_frame, text="Browse", command=browse_file)
file_browse.grid(row=1, column=2, padx=10, pady=10)

tooltip.ToolTip(file_entry, "Shows the file name containing the selected variable names for data");
tooltip.ToolTip(file_browse, "Browse and select the file where the list of selected variable names is stored");
# CSV file selector
# Frame for date and time selection
datetime_frame = ttk.LabelFrame(scrollable_frame, text="Date and Time Selection", padding="10")
datetime_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

# Function to create date and time picker in a single row
def datetime_picker_row(parent, row, label_text, hour_var, minute_var, second_var, default_date):
    # Label
    ttk.Label(parent, text=label_text).grid(row=row, column=0, padx=10, pady=10, sticky="w")
    
    # Date picker with custom date format
    date_widget = DateEntry(parent, width=12, date_pattern='dd-mm-yyyy', year=default_date.year,
                            month=default_date.month, day=default_date.day)
    date_widget.grid(row=row, column=1, padx=5, pady=10)
    
    # Time picker
    vcmd_hour = (root.register(partial(validate_spinbox, min_val=0, max_val=23)), "%P")
    vcmd_minute_second = (root.register(partial(validate_spinbox, min_val=0, max_val=59)), "%P")
    hour_spin = ttk.Spinbox(parent, from_=0, to=23, width=5, textvariable=hour_var, wrap=True, format="%02.0f", validate="key", validatecommand=vcmd_hour)
    hour_spin.grid(row=row, column=2, padx=5, pady=10, sticky="w")
    
    minute_spin = ttk.Spinbox(parent, from_=0, to=59, width=5, textvariable=minute_var, wrap=True, format="%02.0f", validate="key", validatecommand=vcmd_minute_second)
    minute_spin.grid(row=row, column=3, padx=5, pady=10, sticky="w")

    second_spin = ttk.Spinbox(parent, from_=0, to=59, width=5, textvariable=second_var, wrap=True, format="%02.0f", validate="key", validatecommand=vcmd_minute_second)
    second_spin.grid(row=row, column=4, padx=5, pady=10, sticky="w")

    return date_widget

# Calculate the previous day's date
previous_day = datetime.now() - timedelta(days=1)
current_day = datetime.now()
# Start date & time
start_hour_var = tk.StringVar()
start_minute_var = tk.StringVar()
start_second_var = tk.StringVar()
start_date = datetime_picker_row(datetime_frame, 0, "Start Time:", start_hour_var, start_minute_var, start_second_var, previous_day)

# End date & time
end_hour_var = tk.StringVar()
end_minute_var = tk.StringVar()
end_second_var = tk.StringVar()
end_date = datetime_picker_row(datetime_frame, 1, "End Time:", end_hour_var, end_minute_var, end_second_var, current_day)

# Set current time in spin boxes
def set_current_time():
    now = datetime.now()
    start_hour_var.set(f"{now.hour:02}")
    start_minute_var.set(f"{now.minute:02}")
    start_second_var.set(f"{now.second:02}")
    end_hour_var.set(f"{now.hour:02}")
    end_minute_var.set(f"{now.minute:02}")
    end_second_var.set(f"{now.second:02}")

set_current_time()

# Frame for console output
console_frame = ttk.LabelFrame(scrollable_frame, text="Console Output", padding="10")
console_frame.grid(row=4, column=0, padx=10, pady=10, sticky="ew")

# Text widget for displaying console output
text_widget = scrolledtext.ScrolledText(console_frame, wrap='word', height=10)
text_widget.grid(row=0, column=0, padx=10, pady=10)

# Redirect stdout to the Text widget
sys.stdout = TextRedirector(text_widget)

# Buttons frame
button_frame = ttk.Frame(scrollable_frame, padding="5")
button_frame.grid(row=2, column=0, padx=5, pady=5, sticky="ew")

#new pushbutton to launch pointid or var name selection
open_window_button = ttk.Button(button_frame, text="Select Parameter List", command=lambda: open_modal_dialog(file_var.get()))
open_window_button.grid(row=2, column=4, padx=10, pady=10)

tooltip.ToolTip(open_window_button, "Open a dialog to choose variable names for data retrieval.")

# Submit button
#submit_button = ttk.Button(button_frame, text="Submit", command=submit_action)
#submit_button.grid(row=0, column=1, padx=10, pady=10)

#exe_button_frame = ttk.Frame(scrollable_frame)
#exe_button_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

epoch_time_button = ttk.Button(button_frame, text="Decrypt Data(Epoch Time)", command=lambda: run_executable_for_epoch_time_task(path_var.get()))
epoch_time_button.grid(row=2, column=0, padx=10, pady=10)

filter_data_button = ttk.Button(button_frame, text="Retrieve Filtered Data", command=get_filter_data_in_csv)
filter_data_button.grid(row=2, column=1, padx=10, pady=10)

date_time_button = ttk.Button(button_frame, text="Decrypt Data(DateTime Format)", command=lambda: run_executable_for_date_time_task(path_var.get()))
date_time_button.grid(row=2, column=2, padx=10, pady=10)

# Exit button
exit_button = ttk.Button(button_frame, text="Exit", command=exit_action)
exit_button.grid(row=2, column=5, padx=10, pady=10)

# Buttons frame
timegap_frame = ttk.Frame(scrollable_frame, padding="5")
timegap_frame.grid(row=3, column=0, padx=5, pady=5, sticky="ew")
# First label
label1 = ttk.Label(timegap_frame, text="Enter seconds (1–3600)")
label1.grid(row=3, column=0, sticky="w")

# Time interval variable
time_interval_var = tk.StringVar(value="1")  # Default to "0001"
# Time picker
vcmd1 = (root.register(partial(validate_spinbox, min_val=1, max_val=3600)), "%P")
time_interval_spin = ttk.Spinbox(timegap_frame, from_=1, to=3600, width=10, textvariable=time_interval_var, wrap=True, format="%0.0f", validate="key", validatecommand=vcmd1)
time_interval_spin.grid(row=3, column=1, padx=5, pady=10, sticky="w")

tooltip.ToolTip(time_interval_spin, text="This allows the user to specify the time interval between consecutive data samples.")
tooltip.ToolTip(exit_button, text="Close this Window")
tooltip.ToolTip(date_time_button, text="Decrypts the encrypted file, parses timestamps into datetime format, and updates the header with corresponding variable names.")
tooltip.ToolTip(filter_data_button, text="This retrieves the data for the selected parameters within the chosen time period.")
tooltip.ToolTip(epoch_time_button, text="This decrypts the encrypted file, which is in epoch time format, and contains headers encoded as C1Value, C2Value, and so on")

# Second label (example: info or status)
label2 = ttk.Label(timegap_frame, text="Seconds (Interval between consecutive data samples)")
label2.grid(row=3, column=2, sticky="w")



root.mainloop()