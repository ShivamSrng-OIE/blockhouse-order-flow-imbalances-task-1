import pandas as pd
from time import time
from src.utils import *
from src.ofi_features import compute_best_level_ofi


def main():
  print("-" * 100)
  print(">> | Loading data | <<")
  input_path = "data/first_25000_rows.csv"
  df = pd.read_csv(input_path)

  print(f">> | Computing best-level OFI for {len(df)} rows | <<")
  best_ofi = compute_best_level_ofi(df)
  df["best_level_ofi"] = best_ofi
  plot_best_level_ofi(df)
  
  df = df[["ts_event", "bid_px_00", "bid_sz_00", "ask_px_00", "ask_sz_00", "best_level_ofi"]]

  output_path = "output/ofi_features.csv"
  df.to_csv(output_path, index=False)
  print("-" * 100)


if __name__ == "__main__":
  start_time = time() 
  main()
  end_time = time()
  hrs, mins = divmod(end_time - start_time, 3600)
  mins, secs = divmod(mins, 60)
  print(f">> | Time taken: {int(hrs)} hrs {int(mins)} mins {int(secs)} secs | <<")
  print(f">> | Output saved to: `output/ofi_features.csv` | <<")
  print("-" * 100)