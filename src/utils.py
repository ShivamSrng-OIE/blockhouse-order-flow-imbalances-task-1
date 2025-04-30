import pandas as pd
import matplotlib.pyplot as plt


def plot_best_level_ofi(df: pd.DataFrame):
  df["ts_event"] = pd.to_datetime(df["ts_event"])

  plt.figure(figsize=(12, 6))
  plt.plot(df["ts_event"], df["best_level_ofi"], label="Best-Level OFI", color='blue')

  plt.title("Best-Level Order Flow Imbalance (OFI) Over Time")
  plt.xlabel("Timestamp")
  plt.ylabel("OFI Value")
  plt.grid(True)
  plt.legend()
  plt.tight_layout()
  plt.savefig("output/best_level_ofi_plot.png")
  plt.close()