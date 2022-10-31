import os
import datetime as dt
import pandas as pd
import shapefile

import sys

from ACAD import *
from PIL import Image
from PIL.ExifTags import TAGS,GPSTAGS

from pyproj import CRS,Proj
crs = CRS.from_epsg(26910)
proj = Proj(crs)

import tkinter as tk
from tkinter import filedialog

projects = {
  "TM5B": {
    "name": "Trans Mountain Expansion - Spread 5B",
    "folder": "TMEP_S5_5.24.002",
    "version": "5.24.002",
    "symbol": "TMEP",
  },
  "TML1": {
    "name": "Trans Mountain Pipeline",
    "folder": "TMPL_ED41.35628",
    "version": "ED41.35628",
    "symbol": "TMPL",
  },
  "CGL34": {
    "name": "Coastal Gaslink - Spreads 3 & 4",
    "folder": "CGL_S34_R10",
    "version": "R10",
    "symbol": "CGL",
  },
}

project = "TML1"
test = False

if not test: os.chdir(sys._MEIPASS)

def import_CL(path) -> Polyline:
  fname = os.path.join(path,"points")
  with shapefile.Reader(fname) as shp:
    KP_index = [i[0] for i in shp.fields].index("KP") - 1
    KPs = []
    for shp_rcd in shp.iterShapeRecords():
      coords_x = shp_rcd.shape.points[0][0]
      coords_y = shp_rcd.shape.points[0][1]
      label = float(shp_rcd.record[KP_index])
      KPs.append(Point(coords_x,coords_y,label=label))
    KPs.sort(key = lambda i: i.label)

  fname = os.path.join(path,"line")
  with shapefile.Reader(fname) as shp:
    points = [Point(i[0],i[1]) for i in shp.shapes()[0].points]
  
  return Polyline(points,KPs)

def decimal_from_dms(dms,ref):
  value = dms[0] + dms[1]/60 + dms[2]/3600
  if ref in ["S","W"]: value = -value
  return round(value,5)

def print_str(string):
  string = str(string)
  print(string)
  text_results.insert(tk.END,string+"\n")

def ask_path():
  text_results.delete(1.0,tk.END)
  entry_path.delete(0,tk.END)

  path = filedialog.askdirectory(title="Where are your photos?")
  entry_path.insert(0,path)
  print(path)

def run():
  text_results.delete(1.0,tk.END)

  path = entry_path.get()
  if not path:
    text_results.insert(tk.END,"A folder must be selected before running\n")
    return

  try:
    files = os.listdir(path)
    files = [i for i in files if ".jpg" in i.lower()]
    print_str(f"{len(files)} JPG files in directory")
  except Exception as e:
    print_str(e)
    return

  try:
    CL_path = os.path.join("project_data",projects[project]["folder"])
    CL = import_CL(CL_path)
  except Exception as e:
    print_str(e)
    return

  data = pd.DataFrame()
  data["ORIG FILENAME"] = files

  num_renamed = 0
  for index,file in enumerate(files):
    image = Image.open(os.path.join(path,file))
    image.verify()
    exif = image._getexif()
    exif_lab = {TAGS.get(key):val for (key,val) in exif.items()}

    # Get exif data from image
    try:
      exif_geo = exif_lab["GPSInfo"]
      exif_geo = {GPSTAGS.get(key):val for (key,val) in exif_geo.items()}
      coord_x = decimal_from_dms(exif_geo["GPSLongitude"],exif_geo["GPSLongitudeRef"])  
      coord_y = decimal_from_dms(exif_geo["GPSLatitude"],exif_geo["GPSLatitudeRef"])
      coords = proj(coord_x,coord_y)
      point = Point(coords[0],coords[1])
    except Exception as e:
      data.at[index,"ISSUE"] = "GPS information unavailable"
      data.at[index,"ERROR"] = e
      print_str(f"Cannot get GPS data from {file}")
      continue

    # Find chainage of location
    try:
      chainage = CL.find_KP(point)
      data.at[index,"CHAINAGE"] = chainage
      data.at[index,"DISTANCE FROM CL"] = CL.dist_to_ln(point)
      chainage = format_KP(chainage)
    except Exception as e:
      data.at[index,"ISSUE"] = "Chainage not determined"
      data.at[index,"ERROR"] = e
      print_str(f"Cannot find chainage of {file} at ({float(coord_y):.05f}, {float(coord_x):.05f})")
      continue

    # Find time image was taken
    try:
      date_str = exif_lab['DateTime']
      date = dt.datetime.strptime(date_str,"%Y:%m:%d %H:%M:%S")
    except Exception as e:
      data.at[index,"ISSUE"] = "Datetime information unavailable"
      data.at[index,"ERROR"] = e
      print_str(f"Cannot get date from {file}")
      continue

    # Rename image file
    new_name = f"{chainage} {projects[project]['symbol']} - {date:%Y-%m-%d %H.%M.%S}.jpg"
    data.at[index,"NEW FILENAME"] = new_name
    try:
      os.rename(os.path.join(path,file),os.path.join(path,new_name))
    except Exception as e:
      data.at[index,"ISSUE"] = "File not able to be renamed"
      data.at[index,"ERROR"] = e
      print_str(f"Cannot rename {file} to {new_name}")
      continue
    
    num_renamed += 1
    print_str(f"{file} --> {new_name}")
  
  KP_beg = min(data["CHAINAGE"])
  KP_end = max(data["CHAINAGE"])

  print(data)
  print_str(f"{num_renamed}/{len(files)} JPG files have been renamed")
  print_str(f"Chainage Range: {format_KP(KP_beg)} to {format_KP(KP_end)}".replace("+"," "))

font_1 = 'Courier 18 bold'
font_2 = 'Courier 12 bold'
font_3 = 'Courier 8'

col_dark = "grey15"
col_light = "grey30"
col_text = "white"

window = tk.Tk()
window.title("Image Chainage Renamer")

# Create the necessary frames
frame_all = tk.Frame(master=window,bg=col_dark)
frame_path = tk.Frame(master=frame_all,bg=col_dark)
frame_results = tk.Frame(master=window,bg=col_dark)
frame_credit = tk.Frame(master=window,bg=col_dark)

# Create objects
button_select = tk.Button(
  master=frame_all,
  text="SELECT FOLDER CONTAINING IMAGES",
  bg=col_light,
  fg=col_text,
  font=font_2,
  command=ask_path)

label_path = tk.Label(
  master=frame_path,
  text="You have selected:",
  bg=col_dark,
  fg=col_text,
  font=font_3)

entry_path = tk.Entry(
  master=frame_path,
  bg=col_light,
  fg=col_text,
  font=font_3)

label_CL = tk.Label(
  master=frame_all,
  text="Centerline: " + projects[project]["name"],
  bg=col_dark,
  fg=col_text,
  font=font_3)

button_run = tk.Button(
  master=frame_all,
  text="RUN",
  bg="indian red",
  fg=col_text,
  font=font_2,
  command=run)

text_results = tk.Text(
  master=frame_results,
  bg=col_light,
  fg=col_text,
  height=15)

label_credit = tk.Label(
  master=frame_credit,
  text="By Riley Paul",
  font=font_3,
  bg=col_dark,
  fg=col_text)

label_version = tk.Label(
  master=frame_credit,
  text="Version 1.1.0",
  font=font_3,
  bg=col_dark,
  fg=col_text)

# Pack all that shizz up
frame_all.pack(fill=tk.BOTH)
label_CL.pack(side="top",anchor="nw",expand=True)
button_select.pack(fill=tk.X,expand=True,padx=4,pady=4)

label_path.pack(side="left",padx=4)
entry_path.pack(side="left",fill=tk.X,pady=4,padx=4,expand=True)
frame_path.pack(fill=tk.X,expand=True)

button_run.pack(fill=tk.X,side="top",anchor="nw",expand=True,padx=4,pady=4)

text_results.pack(fill=tk.BOTH,padx=4,pady=4,expand=True)
frame_results.pack(fill=tk.BOTH,expand=True)

label_credit.pack(side="left",padx=4)
label_version.pack(side="right",padx=4)
frame_credit.pack(fill=tk.X)

# Run the loop
window.mainloop()