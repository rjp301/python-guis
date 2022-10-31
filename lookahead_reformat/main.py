from transform_table import transform_table

import pandas as pd
import tkinter as tk
from tkinter import filedialog

def clear_printout():
  text_results.delete(1.0,tk.END)

def print_str(string):
  string = str(string)
  print(string)
  text_results.insert(tk.END,string+"\n")

def ask_path():
  clear_printout()
  entry_path.delete(0,tk.END)

  path = filedialog.askopenfilename(title="Select Lookahead")
  entry_path.insert(0,path)
  print(path)

def run():
  clear_printout()

  path = entry_path.get()
  if not path:
    text_results.insert(tk.END,"A folder must be selected before running\n")
    return

  try:
    result = transform_table(path)
    print_str("Lookahead has been converted!\nResult is in the same folder")

  except Exception as e:
    print_str("Could not convert lookahead\nError:")
    print_str(e)
    return


font_1 = 'Courier 18 bold'
font_2 = 'Courier 12 bold'
font_3 = 'Courier 8'

col_dark = "grey15"
col_light = "grey30"
col_text = "white"

window = tk.Tk()
window.title("Macro Lookahead Reformatter")

# Create the necessary frames
frame_all = tk.Frame(master=window)
frame_path = tk.Frame(master=frame_all)
frame_results = tk.Frame(master=window)
frame_credit = tk.Frame(master=window)

# Create objects
button_select = tk.Button(
  master=frame_all,
  text="SELECT LOOKAHEAD FILE",
  font=font_2,
  command=ask_path)

label_path = tk.Label(master=frame_path,text="You have selected:",font=font_3)

entry_path = tk.Entry(master=frame_path,font=font_3)

# Pack all that shizz up
frame_all.pack(fill=tk.BOTH)
button_select.pack(fill=tk.X,expand=True,padx=4,pady=4)

label_path.pack(side="left",padx=4)
entry_path.pack(side="left",fill=tk.X,pady=4,padx=4,expand=True)
frame_path.pack(fill=tk.X,expand=True)

(tk
  .Button(master=frame_all, text="RUN", font=font_2, command=run)
  .pack(fill=tk.X,side="top",anchor="nw",expand=True,padx=4,pady=4)
)

text_results = tk.Text(master=frame_results, height=15)
text_results.pack(fill=tk.BOTH,padx=4,pady=4,expand=True)
frame_results.pack(fill=tk.BOTH,expand=True)

## Footer
(tk
  .Label(master=frame_credit,text="By Riley Paul",font=font_3)
  .pack(side="left",padx=4)
)
(tk
  .Label(master=frame_credit, text="Version 1.1.0", font=font_3)
  .pack(side="right",padx=4)
)
frame_credit.pack(fill=tk.X)

# Run the loop
window.mainloop()