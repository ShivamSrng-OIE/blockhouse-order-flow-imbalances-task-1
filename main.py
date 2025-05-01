import subprocess
import pandas as pd
from time import time
from src.utils import *
from src.ofi_features import *
from argparse import ArgumentParser


def compute_ofi_features(
        df: pd.DataFrame, 
        levels: int = 10
    ) -> pd.DataFrame:
    """
    Compute OFI features and add them to the DataFrame.

    Args:
        - df (pd.DataFrame): Input order book data
        - levels (int): Depth of order book to use for multi-level and integrated OFI

    Returns:
        - pd.DataFrame: DataFrame with added OFI features
    """

    print(" -- Computing Best-Level OFI")
    df["best_level_ofi"] = compute_best_level_ofi(df)
    print(" -- Computing Multi-Level OFI")
    df["multi_level_ofi"] = compute_multi_level_ofi(df, levels=levels)
    print(" -- Computing Integrated OFI")
    df["integrated_ofi"] = compute_integrated_ofi(df, levels=levels)
    return df


def main_cli() -> None:
    """
    Main function for the CLI mode of the OFI feature pipeline. This function reads the input data, computes the OFI features, and saves the results to a CSV file.
    
    Args:
        - None
    
    Returns:
        - None
    """

    df = compute_ofi_features(
        df=pd.read_csv("data/first_25000_rows.csv"),
    )
    print(" -- Plotting features")
    plot_best_level_ofi(df)
    plot_multi_level_ofi(df)
    plot_integrated_ofi(df)

    print(" -- Saving features to CSV: output/ofi_features.csv")
    df = df[
        ["ts_event", "ts_event", "rtype", "publisher_id", "instrument_id", "action", "side", "depth", "price", "size", "flags", "ts_in_delta", "sequence", "symbol", "best_level_ofi", "multi_level_ofi", "integrated_ofi"]
    ]
    df.to_csv("output/ofi_features.csv", index=False)


def main_streamlit() -> None:
    print(" -- Starting Streamlit app")
    subprocess.run(["streamlit", "run", "src/streamlit_app.py"])


def main():
    """
    Main function to parse command line arguments and execute the appropriate mode (CLI or Streamlit).
    
    Args:
        - None
    
    Returns:
        - None
    """

    start_time = time()
    parser = ArgumentParser(
        description="OFI Feature Pipeline, a pipeline for computing order flow imbalance (OFI) features from order book data. This script can be run in two modes: CLI and Streamlit. The CLI mode is for command line usage, while the Streamlit mode is for web-based interaction.",
        usage="python main.py [cli|streamlit]"
    )
    subparsers = parser.add_subparsers(
        dest="subparser", 
        help="Subparser for different modes of operation, either `cli` or `streamlit`.", 
        required=True       
    )
    subparsers.add_parser(
        "cli", 
        help="Command Line Interface mode for OFI feature construction."
    )
    subparsers.add_parser(
        "streamlit", 
        help="Streamlit mode for OFI feature construction."
    )

    args = parser.parse_args()
    if args.subparser == "cli":
        args.mode = "cli"
    elif args.subparser == "streamlit":
        args.mode = "streamlit"
    
    print("-" * 100)
    print(f">> | OFI Feature Construction Mode: {args.mode.upper()} | <<")
    print("-" * 100)

    if args.mode == "cli":
        main_cli()
    elif args.mode == "streamlit":
        main_streamlit()

    end_time = time()
    hrs, mins = divmod(end_time - start_time, 3600)
    mins, secs = divmod(mins, 60)
    print("-" * 100)
    print(f">> | Execution time: {int(hrs)} hours, {int(mins)} minutes, {int(secs)} seconds | <<")
    print("-" * 100)


if __name__ == "__main__":
    main()