from tkinter.messagebox import YES
import streamlit as st
import pandas as pd
import datetime
import joblib
from parse_data import run
from PIL import Image

date_cache = dict()
DATAPATH = "data/data.bin"
TODAY = datetime.date.today().strftime("%d/%m/%Y")
YESTERDAY = (datetime.date.today() - datetime.timedelta(days=1)).strftime("%d/%m/%Y")
data = run()
icon = Image.open("assets/EGC_symbol_color_modern_png.ico")
st.set_page_config(page_icon=icon, page_title="EGC Stats")

def get24buys_sells(stats:dict) -> dict:
  """
  Provides buys and sells from the given data if available
  """
  if stats is not None:
    transactions = stats.get("txns")
    if transactions is not None:
      h24 = transactions.get("h24")
      return h24
  return None

st.image(
    "assets/EGC_logo_color_png.png",
    width=200,
)


_, summary_dict_today, stats_today = data.get(TODAY)
if YESTERDAY in data.keys():
  _, summary_dict_yesterday, stats_yesterday = data.get(YESTERDAY)
else:
  summary_dict_yesterday = None
  stats_yesterday = None


st.header("Distribution of tokens among holders")
st.table(pd.DataFrame(
  data={
      'Quantity  ': summary_dict_today.keys(),
      'Percentage': [f"{s*100:.2f}%" for s in list(summary_dict_today.values())],
      'Cumulative': [f"{sum(list(summary_dict_today.values())[idx:])*100:.2f}%" for idx in range(len(summary_dict_today))]
  }))

h24 = get24buys_sells(stats_today)
h24_yesterday = get24buys_sells(stats_yesterday)
if h24 is not None:
  st.header("Buys and sells in the last 24 hours")
  col1, col2, = st.columns(2)
  buys = h24.get("buys")
  sells = h24.get("sells")
  yes_buys = h24_yesterday.get("buys") if h24_yesterday is not None else None
  yes_sells = h24_yesterday.get("sells") if h24_yesterday is not None else None
  delta_buys = buys-yes_buys if yes_buys is not None else None
  delta_sells = sells-yes_sells if yes_sells is not None else None
  col1.metric("Buys ", buys, delta = delta_buys)
  col2.metric("Sells", sells, delta = delta_sells)
