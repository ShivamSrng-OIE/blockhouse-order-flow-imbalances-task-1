import pandas as pd
from time import time
from src.utils import *
from src.ofi_features import *

def main():
    df = pd.read_csv("data/first_25000_rows.csv")

    print(" -- Computing Best-Level OFI")
    df["best_level_ofi"] = compute_best_level_ofi(df)
    print(" -- Computing Multi-Level OFI")
    df["multi_level_ofi"] = compute_multi_level_ofi(df)
    print(" -- Computing Integrated OFI")
    df["integrated_ofi"] = compute_integrated_ofi(df)

    print(" -- Plotting features")
    plot_best_level_ofi(df)
    plot_multi_level_ofi(df)
    plot_integrated_ofi(df)

    print(" -- Saving features to CSV: output/ofi_features.csv")
    df = df[["ts_event", "ts_event", "rtype", "publisher_id", "instrument_id", "action", "side", "depth", "price", "size", "flags", "ts_in_delta", "sequence", "symbol", "best_level_ofi", "multi_level_ofi", "integrated_ofi"]]
    df.to_csv("output/ofi_features.csv", index=False)
    

if __name__ == "__main__":
    start_time = time()
    print("-" * 100)
    print(">> | OFI Feature Construction | <<")
    print("-" * 100)
    main()
    end_time = time()
    hrs, mins = divmod(end_time - start_time, 3600)
    mins, secs = divmod(mins, 60)
    print("-" * 100)
    print(f">> | Execution time: {int(hrs)} hours, {int(mins)} minutes, {int(secs)} seconds | <<")
    print("-" * 100)