import tkinter as tk 
#from tkinter import *
from tkinter import filedialog,ttk, messagebox, scrolledtext, colorchooser
import traceback
from tkcalendar import DateEntry
#global label_output
import subprocess
#import sys
import glob
from pathlib import Path
import pandas as pd
import csv
import os
from functools import partial
import sys
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from docx import Document
from docx.shared import Inches
import mplcursors
#import tooltipclass as tooltip

global Li

def on_close():
    
    if os.path.exists("first_final.csv"): 
        os.remove("first_final.csv")
    if os.path.exists("output.csv"):
        os.remove("output.csv")
    if os.path.exists("initial.csv"):
        os.remove("initial.csv")
    if os.path.exists("Final.csv"):
        os.remove("Final.csv")
    root.destroy()

def validate_spinbox(new_value, min_val, max_val):
    if new_value == "":
        return False  # Allow empty temporarily
    try:
        val = int(new_value)
        return min_val <= val <= max_val
    except ValueError:
        return False
    
class TextRedirector:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, text):
        self.text_widget.insert(tk.END, text)
        self.text_widget.see(tk.END)  # Scroll to the end
        self.text_widget.update_idletasks()  # Update the GUI

    def flush(self):
        pass  # This is needed for Python 3 compatibility    
        
def show_exception(exc, val, tb):
    error= ''.join(traceback.format_exception(exc, val, tb))
    messagebox.showerror("unexpected error", error)
    
# Functions for handling the tree nodes insertion    
def sort_table(tree_no, column_no):
    rows=[]
    for i in tree_no.get_children(''):
        #print("index", i)
        #print("Tree", tree_no.item(i, "values"))
        #print("Tree child", tree_no.item(i, "values")[0])
        cell_val=tree_no.item(i, "values")[0].split(',')
        cell_final = cell_val[0].split('\t')
        #print("celll", cell_final)
        if len(cell_final) > column_no:
            id_val=int(cell_final[column_no])
        else:
            id_val= 0
        rows.append((id_val, i))
    rows.sort()
    #print("rows", rows)
    for idx, (val, i) in enumerate(rows):
        tree_no.move(i,'',idx)
    
def move_row(event):
    tree=event.widget
    sel_i=tree.selection()
    if not sel_i:
        return
    #print("selection", sel_i)
    c_i=sel_i[0]
    #print("C_I", c_i)
    row_index = tree.index(c_i)
    #print("row_index", row_index)
    item_d=tree.item(c_i)
    #print("item_d", item_d)
    row_v=item_d["values"]
    #print("row_v type", row_v, type(row_v))
    tree1.insert("",row_index, values=row_v)
    tree.delete(c_i)
    sort_table(tree1, column_no=0)
    
def move_row_back(event):
    tree1=event.widget
    sel_i=tree1.selection()
    if not sel_i:
        return
    #print(sel_i)
    c_i=sel_i[0]
    #row_index1 = tree1.index(c_i)
    item_d=tree1.item(c_i)
    row_v=item_d["values"]
    new_id=int(row_v[0])
    #print(row_v)
    position= "end"
    for i, item in enumerate(tree.get_children()):
        existing_values = tree.item(item, "values")
        existing_id= int(existing_values[0])
        if existing_id > new_id:
            position = i
            break
    tree.insert("",position, values=row_v)
    tree1.delete(c_i)
    #sort_table(tree, column_no=0)

def get_point():
    col_point=[]
    for i in tree1.get_children(''):
        cell_val=tree1.item(i, "values")[0].split('\t')
        #print("cell_val", cell_val)
        col_point.append(cell_val[0])
    return col_point

def print_vals():
    
    root.config(cursor = "watch")
    dialog.config(cursor = "watch")
    global output_directory
    L=get_point()
    #if len(L)==0:
    hr=str(hour_var.get())
    mi=str(minute_var.get())
    se=str(second_var.get())
    pl=[hr,mi,se]
   # print("pl",pl)
    if pl==["","",""]:
        messagebox.showerror("Error", "No time selected")
    else:
        time_taken=":".join(pl)
       # print("time_taken",time_taken)
        
        date_taken=str(cal.get())
        #print("date_taken",date_taken)
        tl=[date_taken,time_taken]
        global time_req
        time_req=" ".join(tl)
        #print("time_req",time_req)
        label_date.config(text = f"Selected Date and Time: {time_req}")
     
        if not L:
            messagebox.showerror("Error", "No IDS selected")
  
        else:
            command_filter=["python3", "-u", "filtering_data_with_time.py", "-d",directory.get(), "-i"]
        
            for i in L:
                command_filter.append(i)
            
            command_filter.append("-r")
            command_filter.append(time_req)
            #subprocess.run(command_filter)
            cmd_output=subprocess.Popen(command_filter,stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            for line in cmd_output.stdout:
                text_widget.insert(tk.END,line)
                
                if line.startswith("Output Directory = "):
                    output_directory = line.split("=", 1)[1].strip()
                
                text_widget.see(tk.END)
                root.update()
            cmd_output.wait()  
            
            messagebox.showinfo("DONE", "Process Completed!")
            
    root.config(cursor = "")
    dialog.config(cursor = "")
            
def load_csv():
    
    if directory.get()=="":
        messagebox.showerror("ERROR", "No folder has been selected")
    
    root.config(cursor = "watch")
    
    L=["python3", "-u", "create_static_csv.py", "-d",directory.get()]
    #subprocess.run(L)
    cmd_output=subprocess.Popen(L,stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    for line in cmd_output.stdout:
        text_widget.insert(tk.END,line)
        text_widget.see(tk.END)
        root.update()
    cmd_output.wait()  
    

#creation of different dialog box to get to required point ids
    global dialog
    dialog = tk.Toplevel(root)
    dialog.title("Parameter Selection Dialog")
    dialog.geometry("1000x1000")
    
    
    display_frame = tk.Frame(dialog, bg = "lightgray", relief = "groove")
    display_frame.pack(fill = "both", padx = 5,pady = 5)
    display_frame.grid_rowconfigure(0,weight = 1)
    display_frame.grid_rowconfigure(1,weight = 1)
    display_frame.grid_columnconfigure(0,weight = 1)
    
    display_frame.grid_columnconfigure(2,weight = 1)
    
    
    global tree
    global tree1
    global all_rows
    all_rows=[]
    
    tree=ttk.Treeview(display_frame, show="headings")
    scrollbar = ttk.Scrollbar(display_frame, orient = "vertical", command = tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    
    tree1=ttk.Treeview(display_frame, show="headings")
    
    tree_label = tk.Label(display_frame, text = "Select the required Point IDs:")
    tree_label.grid(row = 0, column = 0, sticky = 'nsew')
    
    tree1_label = tk.Label(display_frame, text = "Selected Point IDs:")
    tree1_label.grid(row = 0, column = 2, sticky = 'nsew')
    
    tree.grid(row = 1, column = 0, sticky = 'nsew')
    scrollbar.grid(row = 1, column = 1, sticky = 'nsw')
    tree1.grid(row = 1, column = 2, padx = 10, sticky = 'nsew')
    tree.bind("<Double-1>", move_row)
    tree1.bind("<Double-1>", move_row_back)
    
    tree.delete(*tree.get_children())
    tree1.delete(*tree.get_children())
    with open("first_final.csv",newline="", encoding="utf-8-sig") as f:
        reader=csv.reader(f, delimiter="\t")
        header = next(reader, None)
        
        new_header=[col.strip().lower() for col in header]
        tree["columns"]=new_header
        tree1["columns"]=new_header

        for col in new_header:
            tree.heading(col,text=col)
            tree1.heading(col,text=col)
            
            tree.column(col, stretch=True)
            tree1.column(col, stretch=True)
        for row in reader:
            tree.insert("",tk.END, values=row)
            all_rows.append(row)
    all_rows.sort()
    #print("Completed inserting to source table")
    
    sort_table(tree, 0)
    #print("Sorted the table successfully!!")
    search_frame = ttk.Frame(dialog)
    search_frame.pack(padx=10, pady=(10, 0), fill='x')

    ttk.Label(search_frame, text="Search:").pack(side='left')

    search_var = tk.StringVar()
    search_entry = ttk.Entry(search_frame, textvariable=search_var)
    search_entry.pack(side='left', fill='x', expand=True, padx=5)
    search_entry.bind("<Return>", lambda event: filter_tree(tree, all_rows, search_var.get()))

    search_button = ttk.Button(search_frame, text="Filter", command=lambda: filter_tree(tree, all_rows, search_var.get()))
    search_button.pack(side='left')
    # date - time frame
    date_frame = ttk.LabelFrame(dialog, text="Date and Time", padding="10")
    date_frame.pack(fill = "both", padx = 5,pady = 5)
    
    date_label = tk.Label(date_frame,text = "Select the required time")
    date_label.grid(row = 0, column = 0)
    
     #tooltip.ToolTip(date_label, text="The time period will include half an hour before and after: ")
    global label_date
    label_date = tk.Label(date_frame)
    label_date.grid(row=2, column= 0)
         
    global cal
    cal=DateEntry(date_frame, selectmode='day', bg="darkblue", borderwidth=2, date_pattern='yyyy-mm-dd')
    cal.grid(row=0, column= 1)
    
    vcmd_hour = (root.register(partial(validate_spinbox, min_val=0, max_val=23)), "%P")
    vcmd_minute_second = (root.register(partial(validate_spinbox, min_val=0, max_val=59)), "%P")
    
    hour_label = tk.Label(date_frame, text="Hour: ").grid(row=0, column=2, pady=10, sticky="w")
    hour_spin = ttk.Spinbox(date_frame, from_=0, to=23, width=5, textvariable=hour_var, wrap=True, format="%02.0f", validate="key", validatecommand=vcmd_hour)
    hour_spin.grid(row=0, column=3, padx=5, pady=10, sticky="w")
    
    minute_label = tk.Label(date_frame, text="Minute: ").grid(row=0, column=4, padx=5, pady=10, sticky="w")
    minute_spin = ttk.Spinbox(date_frame, from_=0, to=59, width=5, textvariable=minute_var, wrap=True, format="%02.0f", validate="key", validatecommand=vcmd_minute_second)
    minute_spin.grid(row=0, column=5, pady=10, sticky="w")
    
    second_label = tk.Label(date_frame, text="Seconds: ").grid(row=0, column=6, padx=5, pady=10, sticky="w")
    second_spin = ttk.Spinbox(date_frame, from_=0, to=59, width=5, textvariable=second_var, wrap=True, format="%02.0f", validate="key", validatecommand=vcmd_minute_second)
    second_spin.grid(row=0, column=7, padx=5, pady=10, sticky="w")
   
    btn_print=tk.Button(dialog, text="create csv files",command=print_vals)
    btn_print.pack(fill = "both", padx = 5,pady = 5)

    root.config(cursor = "")
 
def find_data_folders(root_dir):
    matching = []
    direct = Path(root_dir)
    for dydn in direct.iterdir():
        if dydn.is_dir():
            #print("dydn", dydn)
            for folders in dydn.iterdir():
                matching.append(folders)
            
    #print("matching", matching)
    return matching

def get_all_static_files(folder):
    static_paths=sorted(glob.glob(str(folder/"*_static_DB_File.csv")))
    #print("static_paths", static_paths)
    return static_paths

#reading the static csv files, and creating a dict of col_name, filename according to the required point id
def read_static(static_paths):
    try:
        for i in static_paths:
            path=Path(i)
            #print("PATH", i)
        
            df = pd.read_csv(path , sep='\t', usecols= lambda col: col in ["Point_Id"] + ["Var_Name"]+["Description"])
            if os.path.exists("initial.csv"):
                df.to_csv("initial.csv", mode='a', index=False, header=None)
            else:
                df.to_csv("initial.csv", mode='a', index=False)
        
        #print(df)
        if os.path.exists("initial.csv"):
            df1=pd.read_csv("initial.csv" , sep='\t', usecols= lambda col: col in ["Point_Id"] + ["Var_Name"]+["Description"])
            df1.drop_duplicates(subset=["Point_Id"], inplace=True)
            df1.to_csv("Final.csv",mode='a', index=False)
            #print("DF1", df1)
    except Exception as e:
            #print("Error: reading static files in {}:{}".format(path.name,e))
            print("Error")
            return [] 
    '''if os.path.exists("initial.csv"):
        os.remove("initial.csv")
    '''
                #print("l",L)
    return 
        

def find_list():
    all_folders = find_data_folders(directory.get())
    Lis = []

    for folder in all_folders:
        #print("folder", folder)
        static_paths = get_all_static_files(folder)
        #print("static",static_paths)
        p=read_static(static_paths)
        if p!=None:
            #print("p",p)
            for i in p:
                if i not in Lis:
                    Lis.append(i)
    
    List_final= [str(item) for item in Lis]
    return List_final

def pass_folder(folder_path):
    root.config(cursor = "watch") 
    L=["python3", "-u", "decrypt_archive_data_files_epoch_time_format.py", "-d",folder_path]
    cmd_output=subprocess.Popen(L,stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    for line in cmd_output.stdout:
        text_widget.insert(tk.END,line)
        text_widget.see(tk.END)
        root.update()
    cmd_output.wait()    
        
    all_folders = find_data_folders(directory.get())
    global Li
    Li = []

    for folder in all_folders:
        #print("folder", folder)
        static_paths = get_all_static_files(folder)
        #print("static",static_paths)
        read_static(static_paths)
    root.config(cursor = "") 
    
def filter_tree(tree, all_data, text):
    tree.delete(*tree.get_children())  # Clear current items
    text = text.lower()
    for row in all_data:
        if not text or any(text in str(cell).lower() for cell in row):
            tree.insert("", "end", values=row)
    #print("the end")
    
def browse_folder():
    folder_path = filedialog.askdirectory(initialdir = "/home/ows/Trainee_Work", title = "Select a folder")
    if folder_path:
        #print("folder_path", folder_path)
        label_output.config(text = f"Selected folder: \n {folder_path}")
        
        directory.set(folder_path)
                  

def plot_graph():
    
    csv_folder= Path(output_directory)
    if not csv_folder.exists():
        raise FileNotFoundError(f"folder not found: {csv_folder.absolute()}")
        
    data = {}
    for file in csv_folder.glob("*.csv"):
        try:
            df=pd.read_csv(file,sep='\t')
            
            time_stamp = []
            values = []
            
            for idx, row in df.iterrows():
                time_stamp.append(pd.to_datetime(row[6]))
                values.append(row[4])
            data[file.stem]={"x":time_stamp,"y":values}
            
        except StopIteration:
            print(f"skipping {file.name}:""could not find timestamp or value column")
        except Exception as e :
            print(f"error reading {file.name} : {e}")
    #print("dataa", data)
    if not data:
        raise ValueError("no valid csv files found")
        
    default_colors=["red","yellow","cyan","magenta","black","blue","orange","pink","purple","brown","green"]
    colors={}
    
    for i, name in enumerate(data.keys()):
        colors[name]=default_colors[i%len(default_colors)]
        
    global dialog1
    dialog1 = tk.Toplevel(root)
    dialog1.title(" Graph Dialog")
    dialog1.geometry("1000x1000")
    dialog1.transient(dialog)
    dialog1.grab_set()
    
    fig, ax=plt.subplots(figsize=(8,5))
    global lines
    lines = {}
    
    for name, values in data.items():
        line, =ax.plot(values["x"],values["y"],label=name,color=colors[name])
        lines[line]= name
    cursor = mplcursors.cursor(lines.keys(), hover=True)
    
    @cursor.connect("add")
    def on_add(sel):
        line=sel.artist
        filename=lines[line]
        index=int(sel.index)
        x=line.get_xdata()[index]     
        y=line.get_ydata()[index]
        sel.annotation.set_text(f"File: {filename}\n"f"Time: {x}\n"f"Value: {y}")

        
    ax.xaxis.set_major_locator(mdates.MinuteLocator(interval = 10))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
    fig.autofmt_xdate()
    ax.set_title("plot")
    ax.set_xlabel("X axis")
    ax.set_ylabel("Y axis")
    ax.legend()
    
    canvas=FigureCanvasTkAgg(fig,master = dialog1)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)
    
    control_frame=tk.Frame(dialog1)
    control_frame.pack(pady=10)
    
    tk.Label(control_frame,text="select line").pack(side="left")
    combo=ttk.Combobox(control_frame, values=list(data.keys()), state="read only", width=30)
    combo.pack(side="left",padx=5)
    combo.current(0)
    
    def change_color():
        sel=combo.get()
        if not sel:
            messagebox.showwarning("warning","pls selct a line")
            return
        color=colorchooser.askcolor(title=f"choose color for line {sel}")[1]
        if color:
            colors[sel]=color
            for line, name in lines.items():
                if name== sel:
                    colors[sel]=color
                    line.set_color(color)
                    break
            #lines[sel].set_color(color)
    
            ax.legend()
            canvas.draw()
    
    def save_graph():
        fig.savefig(f"{output_directory}/Graph_{unit_id.get()}_{time_req}.png",dpi =300, bbox_inches="tight")
        #print("dsdafdsfdf")
        #fig.savefig("graph.png",dpi =300, bbox_inches="tight")
        doc = Document()
        
        columns=tree1["columns"]
        table = doc.add_table(rows=1, cols=len(columns))
        table.style="Table Grid"
        
        doc.add_heading(f"report of {unit_id.get()} at {time_req}", level=1)
        
        header = table.rows[0].cells
        for i, col in enumerate(columns):
            header[i].text=col
        for item in tree1.get_children():
            values=tree1.item(item,"values")
            cells = table.add_row().cells
            for i, value in enumerate(values):
                cells[i].text=str(value)
        
        doc.add_picture(f"{output_directory}/Graph_{unit_id.get()}_{time_req}.png", width=Inches(6))
        doc.save(f"{output_directory}/report_{unit_id.get()}_{time_req}.docx")
        #doc.save("report.docx")
        
    tk.Button(control_frame, text="colour change", command=change_color).pack(side="left",padx=5)
    tk.Button(control_frame, text="save graph", command=save_graph).pack(side="left",padx=5)

    root.mainloop()                  

def analysis_csv():
    file_path = filedialog.askopenfilename(title = "Select the required Output CSV file: ", filetypes = [("CSV Files", "*.csv"), ("All Files", "*,*")])
    L=["python3", "-u", "analysis.py", "-d", file_path, "-i", max_range.get()]
    #subprocess.run(L)
    list_alert = subprocess.Popen(L,stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    

    alert_dialog = tk.Toplevel(root)
    alert_dialog.title(" Alert ")
    alert_dialog.geometry("500x300")
    
    alert_dialog.grid_rowconfigure(1, weight = 1)
    alert_dialog.grid_columnconfigure(0, weight = 1)
    
    tk.Label(alert_dialog, text = "Value has gotten out of range at: \n").grid(row=0, column=0)
    text_widget = scrolledtext.ScrolledText(alert_dialog, wrap='word', height=10)
    text_widget.grid(row=1, column=0)

    # Redirect stdout to the Text widget
    sys.stdout = TextRedirector(text_widget)
    
    
    for line in list_alert.stdout:
        
        #print(list_alert[i])
        text_widget.insert(tk.END,line)
        root.update()

######## MAIN #########

#FRAME IS IN PLACE; INSIDE WIDGETS IN GRID
root = tk.Tk()
root.title("GUI for Filtering and getting required Data")
root.minsize(height=500, width=600)
root.maxsize(height=2000, width=2000)
root.report_callback_exception=show_exception
#file dialog
directory = tk.StringVar()
time_req = tk.StringVar()
hour_var = tk.StringVar()
minute_var = tk.StringVar()
second_var = tk.StringVar()
unit_id= tk.StringVar()

max_range = tk.StringVar()

#encrypt_file = tk.Label(root, text = "Decrypt the files", bg = "lightgray").pack(fill = "both", expand = True, padx = 20, pady = 20)


#FRAME FOR DECRYPTING 
browse_frame = ttk.LabelFrame(root, text="Decryption", padding="10")
browse_frame.pack(fill = "both", padx = 5,pady = 5, expand = True)

browse_frame.grid_rowconfigure(0,weight = 1)
browse_frame.grid_columnconfigure(0,weight = 1)
#browse_frame.grid_rowconfigure(,weight = 1)
browse_frame.grid_columnconfigure(1,weight = 1)

browse_frame.grid_rowconfigure(2,weight = 1)
browse_frame.grid_rowconfigure(0,weight = 1)
browse_frame.grid_columnconfigure(0,weight = 1)

search_folder_label = tk.Label(browse_frame, text = "Search for the directory that contains the encrypted files: ")
search_folder_label.grid(row = 0, column = 0)
find_folder_button = tk.Button(browse_frame, text = "Browse Folder", bg = "white", command = browse_folder)
find_folder_button.grid(row = 0, column = 1, sticky="w")

label_output = tk.Label(browse_frame, text = "No selection yet")
label_output.grid(row = 1, column = 0)
decrypt_button = tk.Button(browse_frame, text = "Decrypt",bg = "white", command = lambda: pass_folder(directory.get()))
decrypt_button.grid(row = 1, column = 1, sticky="w")

unit_entry=tk.Entry(browse_frame, textvariable=unit_id)
unit_entry.grid(row=2,column=1, sticky="w")
unit_label=tk.Label(browse_frame, text = "unit id").grid(row=2,column=0)


btn_load=tk.Button(root, text="Proceed", command=load_csv)
btn_load.pack(expand = True, padx = 20, pady = 20)


#----------------------------tree_view-------------------------------------

#btn_print=tk.Button(root, text="print", command=print_vals).grid(row=9, column=1)

console_frame = ttk.LabelFrame(root, text="Console Output", padding="10")
console_frame.pack(fill = "both", padx = 5,pady = 5, expand = True)

console_frame.grid_rowconfigure(0,weight = 1)
console_frame.grid_columnconfigure(0,weight = 1)
# Text widget for displaying console output
text_widget = scrolledtext.ScrolledText(console_frame, wrap='word', height=10)
text_widget.grid(row=0, column=0, padx=10, pady=10)

analysis_frame = ttk.LabelFrame(root, text="Analysis", padding="10")
analysis_frame.pack(fill = "both", padx = 5,pady = 5, expand = True)

analysis_frame.grid_rowconfigure(1,weight = 1)
analysis_frame.grid_rowconfigure(0,weight = 1)
analysis_frame.grid_columnconfigure(0,weight = 1)
analysis_frame.grid_columnconfigure(1,weight = 1)
analysis_frame.grid_columnconfigure(2,weight = 1)

create_graph_button = tk.Button(analysis_frame, text = "Generate Graph", bg = "white", command = plot_graph)
create_graph_button.grid(row = 0, column = 1, sticky="w")

analysis_btn=tk.Button(analysis_frame, text="Analyse a single Point ID", command=analysis_csv)
analysis_btn.grid(row = 1, column = 2, sticky="w")
analysis_entry = tk.Entry(analysis_frame, textvariable=max_range)
analysis_entry.grid(row=1,column=1, sticky="w")
analysis_label=tk.Label(analysis_frame, text = "Enter the range: ").grid(row=1,column=0)

# Redirect stdout to the Text widget
sys.stdout = TextRedirector(text_widget)

root.protocol("WM_DELETE_WINDOW", on_close)


root.mainloop()
