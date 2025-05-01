import matplotlib.pyplot as plt
import pandas as pd

def plot_best_level_ofi(
        df: pd.DataFrame
    ) -> None:
    """
    Plot the best-level order flow imbalance (OFI) with smoothed values.
    
    Args:
        - df (pd.DataFrame): DataFrame containing the OFI data.
    
    Returns:
        - None
    """

    df["ts_event"] = pd.to_datetime(df["ts_event"])
    smoothed = df["best_level_ofi"].rolling(window=30, min_periods=1).mean()
    plt.figure(figsize=(48, 24))
    plt.plot(df["ts_event"], smoothed, color='blue', label="Smoothed Best-Level OFI")
    plt.fill_between(df["ts_event"], smoothed, 0, where=smoothed > 0, color='green', alpha=0.1)
    plt.fill_between(df["ts_event"], smoothed, 0, where=smoothed < 0, color='red', alpha=0.1)
    plt.title("Smoothed Best-Level Order Flow Imbalance")
    plt.xlabel("Timestamp")
    plt.ylabel("OFI Value")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("output/best_level_ofi_plot.png")
    plt.close()


def plot_multi_level_ofi(
        df: pd.DataFrame
    ) -> None:
    """
    Plot the multi-level order flow imbalance (OFI) with smoothed values.

    Args:
        - df (pd.DataFrame): DataFrame containing the OFI data.
    
    Returns:
        - None
    """

    df["ts_event"] = pd.to_datetime(df["ts_event"])
    smoothed = df["multi_level_ofi"].rolling(window=30, min_periods=1).mean()
    plt.figure(figsize=(48, 24))
    plt.plot(df["ts_event"], smoothed, color='purple', label="Smoothed Multi-Level OFI")
    plt.fill_between(df["ts_event"], smoothed, 0, where=smoothed > 0, color='green', alpha=0.1)
    plt.fill_between(df["ts_event"], smoothed, 0, where=smoothed < 0, color='red', alpha=0.1)
    plt.title("Smoothed Multi-Level Order Flow Imbalance")
    plt.xlabel("Timestamp")
    plt.ylabel("OFI Value")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("output/multi_level_ofi_plot.png")
    plt.close()


def plot_integrated_ofi(
        df: pd.DataFrame
    ) -> None:
    """
    Plot the integrated order flow imbalance (OFI) with smoothed values.
    
    Args:
        - df (pd.DataFrame): DataFrame containing the OFI data.
    
    Returns:
        - None
    """

    df["ts_event"] = pd.to_datetime(df["ts_event"])
    smoothed = df["integrated_ofi"].rolling(window=30, min_periods=1).mean()
    plt.figure(figsize=(48, 24))
    plt.plot(df["ts_event"], smoothed, color='teal', label="Smoothed Integrated OFI")
    plt.fill_between(df["ts_event"], smoothed, 0, where=smoothed > 0, color='green', alpha=0.1)
    plt.fill_between(df["ts_event"], smoothed, 0, where=smoothed < 0, color='red', alpha=0.1)
    plt.title("Smoothed Integrated OFI")
    plt.xlabel("Timestamp")
    plt.ylabel("Integrated OFI")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("output/integrated_ofi_plot.png")
    plt.close()