import joblib
import numpy as np
import requests
import os
import datetime

TODAY = datetime.date.today().strftime("%d/%m/%Y")
DATAPATH = "data/data.bin"

path = "data/export-tokenholders-for-contract-0xc001bbe2b87079294c63ece98bdd0a88d761434e.csv"
STEPS = np.logspace(3, 13, 11, base=10)
REST_API_URL = "https://api.dexscreener.com/latest/dex/tokens/0xc001bbe2b87079294c63ece98bdd0a88d761434e"

def quantity2Billions(quantity:float) -> str:
  if abs(quantity - 1E3) < 1:
    return "0    to 1K  "
  elif abs(quantity - 1E4) < 1:
    return "1K   to 10K "
  elif abs(quantity - 1E5) < 1:
    return "10K  to 100K"
  elif abs(quantity - 1E6) < 1:
    return "100K to 1M  "
  elif abs(quantity - 1E7) < 1:
    return "1M   to 10M "
  elif abs(quantity - 1E8) < 1:
    return "10M  to 100M"
  elif abs(quantity - 1E9) < 1:
    return "100M to 1G  "
  elif abs(quantity - 1E10) < 1:
    return "1G   to 10G "
  elif abs(quantity - 1E11) < 1:
    return "10G  to 100G"
  elif abs(quantity - 1E12) < 1:
    return "100G to 1T  "
  elif abs(quantity - 1E13) < 1:
    return "1T   to 10T "

def collect_today_data(data:dict) -> dict:
  with open(path, "r") as f:
    lines = f.readlines()

  lines = [line.split(",") for line in lines[2:]]
  lines = [(line[0], float(line[1].replace('"', ''))) for line in lines]
  lines_dict = dict(lines)
  num_addresses = len(lines_dict.keys())

  summary_dict = dict()
  array = np.asarray(list(lines_dict.values()))
  for idx in range(len(STEPS)):
    if idx == 0:
      lesser = len(np.where(array <= STEPS[idx])[0])
      amount = lesser
    else:
      lesser_prev = len(np.where(array <= STEPS[idx-1])[0])
      lesser_current = len(np.where(array <= STEPS[idx])[0])
      amount = lesser_current - lesser_prev
    summary_dict[quantity2Billions(STEPS[idx])] = amount/num_addresses
    # print(f"amount between {quantity2Billions(STEPS[idx])} ---> {amount}\t --> {amount/num_addresses*100:.2f}%")


  response = requests.get(REST_API_URL)
  stats = None
  if response.status_code == 200:
    stats = response.json().get("pairs")
    stats = [s for s in stats if "pancakeswap" in s.values()]
    if len(stats) < 1:
      stats = None
    else:
      stats = stats[0]

  data[TODAY] = (lines_dict, summary_dict, stats)
  return data
    
def run() -> dict:
  if os.path.exists(DATAPATH):
    data = joblib.load(DATAPATH)
  else:
    data = dict()
  data = collect_today_data(data)
  joblib.dump(data, DATAPATH) 
  return data

run()