import os
import datetime as dt

def latest_file(
  path,
  date_format="%Y %m %d",
  prefix="",
  suffix="",
  silent=True,
  extension=None,
  ) -> tuple:

  def slice_text(string, prefix, suffix):
    i1 = string.index(prefix) if prefix and prefix in string else 0
    i2 = string.index(suffix) if suffix and suffix in string else None
    return string[i1 + len(prefix):i2]

  files = os.listdir(path)
  files = list(filter(lambda i: not (i.startswith(".") or i.startswith("~")), files))

  file_date = []
  for file in files:
    name,_ = os.path.splitext(file)
    date_str = slice_text(name, prefix, suffix)

    try:
      date = dt.datetime.strptime(date_str,date_format)
    except ValueError as e:
      if not silent: print(f"ERROR: {date_str} does not match the format of {date_format}")
      continue
    
    file_date.append((file,date))

  latest = max(file_date,key=lambda i: i[1])
  fname = os.path.join(path,latest[0])
  date = latest[1]

  print(f"{len(files)} files filtered - latest file is {latest[0]} from {date:%Y %m %d}")
  return fname,date
