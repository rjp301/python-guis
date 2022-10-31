def convert_chainage_string(string:str):
  if type(string) != str: return float(string)
  result = string.replace(" ","").split("+")
  try: result = [float(i) for i in result]
  except: return None
  result[0] *= 1000
  result = sum(result)
  return result