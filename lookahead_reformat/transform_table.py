import pandas as pd
import re
import os

from utils.format_KP import format_KP
from utils.latest_file import latest_file
from utils.convert_chainage_string import convert_chainage_string

roads = pd.read_csv(os.path.join("lookahead_reformat","data","roads.csv"))
re_chainage = r"[0-9]+\s*\+\s*[0-9]+"

def first_common_element(x,y):
  for i in x:
    if i in y:
      return i
  return None

def nearest_rd(chainage):
  temp = roads.copy()
  temp["sort_key"] = temp.chainage.apply(lambda i: abs(chainage - i))
  temp = temp.sort_values("sort_key")
  return temp.iloc[0]["id"]

def rd_chainage(name):
  name = re.search(r"[0-9]*[a-z]",name,flags=re.I)
  if not name: return None
  if name not in roads["id"]: return None
  return roads.copy().set_index("id").loc[name]["chainage"]

def get_chainage(string):
  chainages = re.findall(re_chainage,string)
  if not chainages: return None
  chainages = [int("".join(re.findall(r'\d+',i))) for i in chainages]
  chainages = (pd.Series(chainages)
    .drop_duplicates()
    .apply(format_KP)
    .tolist()
  )
  if len(chainages) == 1: return chainages[0]
  return f"{min(chainages)} - {max(chainages)}"

def format_rd(string):
  if not string: return None
  num = re.search(r"[0-9]*",string,flags=re.I)
  if not num: return None
  num = format(int(num.group()),"02") if num else ""
  letter = re.search(r"[a-z]",string,flags=re.I)
  letter = letter.group().upper() if letter else ""
  return f"Road {num}{letter}"

def get_road(string):
  roads = re.findall(r"(?:rd|road)\#?\.?\s*[0-9]+[a-zA-Z]?(?:\s*[\-\&\\\/to]\s*[0-9]+[a-zA-Z]?)?",string,flags=re.I)
  chainage = get_chainage(string)
  
  if not chainage and not roads: return None
  if not roads:
    chainages = re.findall(re_chainage,chainage,flags=re.I)
    chainages = [convert_chainage_string(i) for i in chainages]
    roads = [nearest_rd(i) for i in chainages]
  
  roads = [re.findall(r"[0-9]+[a-z]?",i,flags=re.I) for i in roads]
  roads = [item for sublist in roads for item in sublist]
  roads = (pd.Series(roads)
    .drop_duplicates()
    .apply(format_rd)
    .tolist()
  )
  if len(roads) == 1: return roads[0]
  return f"{min(roads)} - {max(roads)}"

def get_dpi_req(string,dpi_rd):
  dpi_rds = re.findall(r"[0-9]+[a-z]?",str(dpi_rd),flags=re.I)
  if not dpi_rds: return None

  all_rds = re.findall(r"[0-9]+[a-z]?",string,flags=re.I)
  if not all_rds: return None

  return format_rd(first_common_element(dpi_rds,all_rds))

def transform_table(fname):
  data = pd.read_excel(fname,header=3)
  data = data.drop(data.tail(2).index)
  data["FOREMAN"] = data["FOREMAN"].apply(lambda i: i.replace("\n"," ").strip())
  data["CREW"] = data["CREW"].apply(lambda i: re.sub(r"\([0-9]+\)|#\s*[0-9]+","",i).strip())
  print(data)

  dfs = []
  for _,row in data.iterrows():
    temp = pd.DataFrame()

    split = re.split(r"\n\n",str(row["PLANNED ACTIVITIES"]))
    split = [i.strip() for i in split]
    strings = pd.Series(split)

    temp[""] = ["" for _ in range(len(strings))]
    temp["Road"] = strings.apply(get_road).fillna("1.Full Spread")
    temp["Crew"] = re.sub(r"\s*\n\s*"," ",row["CREW"])
    temp["KP Range"] = strings.apply(get_chainage)
    temp["Construction Activities"] = strings
    temp["S/S"] = strings.apply(lambda i: get_dpi_req(i,row["S/S"]))
    temp["DPI Req"] = strings.apply(lambda i: get_dpi_req(i,row["DPI REQ"]))
    temp["Supervision"] = row["FOREMAN"]
    
    dfs.append(temp)

  fname = os.path.splitext(fname)[0] + "_processed.xlsx"
  result = pd.concat(dfs,ignore_index=True)
  result["Contractor"] = "Macro"
  result.to_excel(fname,index=False,encoding="utf-16")
  
  return result


if __name__ == "__main__":
  transform_table()
  